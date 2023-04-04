#!/usr/bin/python3
import argparse
import csv
import cffi
import functools
import itertools
import logging
import os.path
import re
import subprocess
import sys
import tempfile

logger = logging.getLogger(__name__)

VALGRIND_PRELOAD_PATH = "/usr/lib/x86_64-linux-gnu/valgrind/vgpreload_core-amd64-linux.so"

cached_realpath = functools.lru_cache()(os.path.realpath)

def canonical_path(path):
    if path == '???':
        return '???'
    else:
        return cached_realpath(path)

callgrind_field_to_type = {
    'ob': 'object-file',
    'cob': 'object-file',
    'fn': 'function',
    'cfn': 'function',
    'fi': 'source-file',
    'cfi': 'source-file',
    'fl': 'source-file',
    'fe': 'source-file',
}

def process_callgrind_output(fh):
    global callgrind_field_to_type
    cols_positions = ['line']
    cols_events = ['count']
    value_map = {}
    id_map = {}
    last_entry = {}
    instr_counts = {}
    objects = set()
    last_was_calls = False
    for line in fh:
        if last_was_calls:
            last_was_calls = False
            continue
        line = line.strip()
        if line.startswith('#'):
            continue
        if ': ' in line:
            kv = line.split(': ', 1)
            key = kv[0]
            value = kv[1]
            key = key.strip()
            value = value.strip()
            if key == 'desc' or key == 'summary':
                continue
            elif key == 'positions':
                cols_positions = value.split()
            elif key == 'events':
                cols_events = value.split()
            else:
                pass
        elif '=' in line:
            key, value = line.split('=', 1)
            if key == 'calls':
                last_was_calls = True
            m = re.match(r'\((\d+)\)(.*)', value)
            if m == None:
                value_map[key] = value
            else:
                id_key = (callgrind_field_to_type.get(key, 'unknown'), m.group(1))
                if m.group(2) == '':
                    value_map[key] = id_map[id_key]
                else:
                    id_map[id_key] = m.group(2)[1:]
                    value_map[key] = id_map[id_key]
        else:
            parts = line.split()
            cols = cols_positions + cols_events
            cur_entry = {}
            for col_name, part in zip(cols, parts):
                if part.startswith('+') or part.startswith('-'):
                    assert(col_name in last_entry)
                    cur_entry[col_name] = last_entry[col_name] + int(part)
                elif part == '*':
                    assert(col_name in last_entry)
                    cur_entry[col_name] = last_entry[col_name]
                elif part.startswith('0x'):
                    cur_entry[col_name] = int(part, 16)
                else:
                    cur_entry[col_name] = int(part)
            if 'Ir' in cur_entry and 'instr' in cur_entry:
                key = (canonical_path(value_map['ob']), cur_entry['instr'])
                objects.add(value_map['ob'])
                if key not in instr_counts:
                    instr_counts[key] = 0
                instr_counts[key] += cur_entry['Ir']
            last_entry = cur_entry
    return {
        'instr_counts': instr_counts,
        'objects': objects,
    }

def merge_callgrind_outputs(outputs):
    instr_counts = {}
    objects = set()
    for output in outputs:
        for k, v in output['instr_counts'].items():
            if k not in instr_counts:
                instr_counts[k] = 0
            instr_counts[k] += v
        objects |= output['objects']
    return {
        'instr_counts': instr_counts,
        'objects': objects,
    }

@functools.lru_cache()
def extract_assembly_from(binary, offset=0):
    if binary == '???':
        return {}
    disasm = subprocess.check_output([
        'objdump', '-d', binary
    ], encoding='UTF-8')
    result = {}
    for line in disasm.split('\n'):
        m = re.search(r'^ \s*(?P<pc>[0-9a-f]+):\s+(?:[0-9a-f]{2} )+\s*(?P<instr>[^\n#<]+)', line)
        if m != None:
            if len(m.group('instr').strip()) == 2 and re.match(r'[0-9a-f]+', m.group('instr').strip()):
                continue
            addr = int(m.group('pc'), 16)
            instr = re.sub(r'\s+', ' ', m.group('instr').strip())
            label_instruction(instr)
            key = (canonical_path(binary), addr + offset)
            result[key] = instr
    return result

def extract_assembly_from_objects(objects):
    result = {}
    for object_file in objects:
        result.update(extract_assembly_from(object_file))
    return result

def tag_constant(constant):
    result = set()
    result.add('constant')
    if constant < 0:
        result.add('negative')
    if constant == 0:
        result.add('zero')
    constant_as_signed = constant
    # heuristic guess about signed numbers
    if constant > 2**31 and constant < 2**32:
        constant_as_signed = -(constant^0xFFFFFFFF + 1)
    if constant > 2**63 and constant < 2**64:
        constant_as_signed = -(constant^0xFFFFFFFFFFFFFFFF + 1)
    for i in range(8, 64):
        if constant_as_signed < 2**(i-1) and constant_as_signed >= -2**(i-1):
            result.add('constant-fits-in-signed-' + str(i))
        if constant > 0 and constant < 2**(i):
            result.add('constant-fits-in-unsigned-' + str(i))
    return result

def operand_types(operand):
    result = set()
    if operand.startswith('%') and ':' not in operand:
        # %eax, but not %fs:0x1234
        result.add('register')
    if '(' in operand:
        result.add('memory')
    if '(%' in operand:
        result.add('memory-base')
    if ',%' in operand:
        result.add('memory-index')
    if ',2' in operand or ',4' in operand or ',8' in operand:
        result.add('memory-scale')
    if '(' in operand and operand.startswith('0x'):
        result.add('memory-offset')
        constant, _ = operand.split('(', 1)
        result |= tag_constant(int(constant[2:], 16))
    if '(' in operand and operand.startswith('-0x'):
        result.add('memory-offset')
        constant, _ = operand.split('(', 1)
        result |= tag_constant(-int(constant[3:], 16))
    if '*' in operand:
        result.add('indirect-jump')
    if '$' in operand:
        result.add('immediate')
        if operand.startswith('$0x'):
            result |= tag_constant(int(operand[3:], 16))
        elif operand.startswith('$-0x'):
            result |= tag_constant(-int(operand[3:], 16))
        elif operand.startswith('$'):
            result |= tag_constant(int(operand[1:], 10))
    if re.match(r'^[0-9a-fx]+$', operand) != None:
        logger.debug('constant pointer from %s', operand)
        result.add('constant-pointer')
    if '%rip' in operand:
        result.add('rip-offset')
    return result

def split_operands(operands):
    operands = operands.strip()
    parts = re.findall(r'(\*?[0-9xa-f]*\([^)]+\)|\*?%[a-z0-9]+|\$[0-9xa-f]+|[0-9a-f]+)(?:,|$)', operands)
    return parts

def _any_variant_in(target, lst):
    for ext in ['', 'b', 'w', 'l', 'q']:
        if target + ext in lst:
            return True
    return False

@functools.lru_cache(maxsize=1024 * 32)
def label_instruction(assembly):
    assembly = assembly.strip()
    parts = assembly.split()
    mnemonics = []
    operands = []
    seen_mnemonic = False
    for part in parts:
        if part.startswith('<'):
            continue
        if seen_mnemonic and (re.match(r'[-()*$%$0-9].*|[a-f][0-9a-f]*(?:,|$)', part) != None):
            operands += split_operands(part)
        else:
            seen_mnemonic = True
            mnemonics.append(part)
    operand_tags = list(map(operand_types, operands))
    tags = set()
    if len(operand_tags) == 2 and 'register' in operand_tags[0] and 'register' in operand_tags[1]:
        tags.add('two-registers')
    if len(operand_tags) == 2:
        tags.add('two-operands')
    for item in operand_tags:
        tags |= item
    if _any_variant_in('mov', mnemonics):
        tags.add('mov')
        tags.add('mov-or-pushpop')
    if _any_variant_in('lea', mnemonics):
        tags.add('lea')
    if _any_variant_in('nop', mnemonics):
        tags.add('nop')
    if _any_variant_in('endbr64', mnemonics):
        tags.add('nop')
    if _any_variant_in('call', mnemonics):
        tags.add('call')
    for mnemonic in mnemonics:
        if mnemonic.startswith('cmov'):
            tags.add('cmov')
    if len(operand_tags) > 0 and 'nop' not in tags and 'lea' not in tags:
        if 'memory' in operand_tags[-1]:
            tags.add('to-memory')
        if 'memory' in operand_tags[0] and len(operand_tags) > 1:
            tags.add('from-memory')
        if 'memory' in operand_tags[-1] and 'mov' not in tags:
            tags.add('from-memory')
        if 'constant' in operand_tags[0]:
            tags.add('from-constant')
    if 'push' in mnemonics or 'call' in mnemonics or 'callq' in mnemonics:
        tags.add('to-memory')
        tags.add('push')
        tags.add('mov-or-pushpop')
    if 'pop' in mnemonics or 'retq' in mnemonics or 'ret' in mnemonics:
        tags.add('from-memory')
        tags.add('pop')
        tags.add('mov-or-pushpop')
    if len(set(['j', 'jmpq', 'jmp']) & set(mnemonics)) > 0:
        if len(operand_tags) == 0:
            logger.debug('jump with no operand tags? %s', assembly)
        if 'indirect-jump' in operand_tags[0]:
            tags.add('indirect-jump')
        else:
            tags.add('uncond-jump')
    if len(set(['je', 'jz', 'jnz', 'js', 'jns', 'jle', 'jl',
                'jge', 'jg', 'jne', 'ja', 'jae', 'jb', 'jbe']) & set(mnemonics)) > 0:
        tags.add('cond-jump')
    return tags

def extract_constants(assembly):
    assembly = assembly.strip()
    parts = assembly.split()
    operands = []
    for part in parts:
        if part.startswith('<'):
            continue
        if re.match(r'[*$%$0-9].*', part) != None:
            operands += split_operands(part)
    result = []
    for operand in operands:
        m = re.search(r'\$?0x?([0-9a-f]+)', operand)
        if m != None:
            result.append(int(m.group(1), 16))
    return result

def matches(match_tag_string, tags):
    parts = match_tag_string.split('+')
    is_match = True
    for part in parts:
        if len(part) == 0:
            continue
        if part.startswith('!'):
            is_match = is_match and (part[1:] not in tags)
        else:
            is_match = is_match and (part in tags)
    return is_match

interesting_categories = [
    ('', 'total instructions'),
    ('!mov+!cmov+two-operands', 'non-mov instructions with two operands'),
    ('!mov+!cmov+two-registers', 'non-mov instructions with two register operands'),
    ('mov+!to-memory+!from-memory+!from-constant', 'register-to-register unconditional movs'),
    ('cmov+!to-memory+!from-memory', 'register-to-register conditional movs'),
    ('to-memory', 'instructions that write memory'),
    ('!cmov+!mov-or-pushpop+to-memory', 'non-mov/cmov/push instructions that write memory'),
    ('from-memory', 'instructions that read memory'),
    ('!cmov+!mov-or-pushpop+from-memory', 'non-mov/cmov/pop instructions that read memory'),
    ('to-memory+from-memory', 'instructions that both read AND write memory'),
    ('cond-jump', 'conditional jumps'),
    ('indirect-jump', 'indirect (computed) jumps (including virtual calls)'),
    ('uncond-jump', 'unconditional jumps (including calls)'),
    ('memory-base+memory-index', 'instructions with disp(rXX,rYY) or disp(rXX,rYY,scale) addressing'),
    ('memory-scale+memory-base+memory-index', 'instructions with disp(rXX,rYY,scale) addressing where scale != 1'),
    ('!memory-scale+memory-base+memory-index', 'instructions with disp(rXX,rYY) (or disp(rXX,rYY,scale) with scale = 1) addressing'),
    ('memory-scale+memory-index+!memory-base', 'instructions with disp(,rYY,scale) addressing (where scale is not 1)'),
    ('memory-scale', 'instructions with disp(rXX,rYY,scale) or disp(,rYY,scale) addressing (where scale is not 1)'),
    #('constant-pointer+!memory-offset+!memory-base+!memory-index', 'instructions with constant addresses'),
    ('!zero+constant', 'instructions with non-zero immediate'),
    ('!zero+constant-fits-in-signed-8', 'instructions with non-zero immediate that fits in signed byte'),
    ('!zero+constant-fits-in-unsigned-8', 'instructions with non-zero immediate that fits in unsigned byte'),
    ('!zero+constant-fits-in-signed-10', 'instructions with non-zero immediate that fits in 10 bit (or smaller) signed number'),
    ('!zero+constant-fits-in-unsigned-10', 'instructions with non-zero immediate that fits in 10 bit (or smaller) unsigned number'),
    ('!zero+constant-fits-in-signed-13', 'instructions with non-zero immediate that fits in 13 bit (or smaller)signed number'),
    ('!zero+constant-fits-in-unsigned-13', 'instructions with non-zero immediate that fits in 13 bit (or smaller) unsigned number'),
    ('!zero+constant-fits-in-signed-16', 'instructions with non-zero immediate that fits in 16 bit (or smaller) signed number'),
    ('!zero+constant-fits-in-signed-18', 'instructions with non-zero immediate that fits in 18 bit (or smaller) signed number'),
    ('!zero+constant-fits-in-signed-20', 'instructions with non-zero immediate that fits in 20 bit (or smaller) signed number'),
    ('!zero+constant-fits-in-signed-32', 'instructions with non-zero immediate that fits in 32 bit (or smaller) signed number'),
    ('!zero+constant-fits-in-signed-48', 'instructions with non-zero immediate that fits in 48 bit (or smaller) signed number'),
]

def run_and_get_callgrind_output(binary, arguments, hide_program_output=False):
    callgrind_out_dir = tempfile.TemporaryDirectory()
    callgrind_out_pattern = os.path.join(callgrind_out_dir.name, 'callgrind.out.%p')
    logfile_out = tempfile.NamedTemporaryFile()
    logger.debug('running %s / %s', binary, arguments)
    # FIXME: multiple programs?
    subprocess.call([
        'valgrind',
        '--tool=callgrind',
        '--dump-instr=yes',
        '--trace-children=yes',
        '--log-file={}'.format(logfile_out.name),
        '--callgrind-out-file={}'.format(callgrind_out_pattern),
        binary] + arguments,
        stdout=subprocess.DEVNULL if hide_program_output else None,
    )
    outputs = []
    for name in filter(lambda x: x.startswith('callgrind.out.'), os.listdir(callgrind_out_dir.name)):
        path = os.path.join(callgrind_out_dir.name, name)
        logger.debug('using generated file %s', path)
        with open(path, 'r') as fh:
            outputs.append(process_callgrind_output(fh))
    return merge_callgrind_outputs(outputs)

def count_categories(addr_to_instruction, frequencies=None):
    categories = {}
    for k, v in addr_to_instruction.items():
        count = 1
        if frequencies:
            count = frequencies.get(k, 0)
        tags = label_instruction(v)
        for match_string, category in interesting_categories:
            if category not in categories:
                categories[category] = 0
            if matches(match_string, tags):
                categories[category] += count
    return categories

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--callgrind-output',
        type=argparse.FileType('r'),
        help='File containing output from valgrind --tool=callgrind for the program specified with --binary.'
    )
    parser.add_argument('--binary', type=str,
        help='Executable program to analyze.')
    parser.add_argument('command', nargs='*', default=[])
    parser.add_argument('--mode',
        choices=(
            'list',
            'categories',
            'constants'
        ),
        default='categories',
    )
    parser.add_argument('--identify-unknown', action='store_true')
    parser.add_argument('--hide-program-output', action='store_true')
    args = parser.parse_args()
    if len(args.command) > 0:
        args.binary = args.command[0]
    if len(args.command) > 0:
        print("Running command {}".format(" ".join(args.command)))
        result = run_and_get_callgrind_output(
            args.command[0], args.command[1:],
            hide_program_output=args.hide_program_output
        )
    else:
        result = process_callgrind_output(args.callgrind_output)
    frequencies = result['instr_counts']
    objects = result['objects']
    addrs = extract_assembly_from_objects(objects)
    if args.mode == 'list':
        for k in sorted(frequencies.keys(), key=lambda k: frequencies[k], reverse=True):
            if k in addrs:
                print(hex(k), frequencies[k], addrs[k], label_instruction(addrs[k]))
    elif args.mode == 'categories':
        max_category_name_width = max(map(len, map(lambda k: k[1], interesting_categories)))
        seen_files = set(map(lambda x: x[0], addrs.keys()))
        unknown_retired = 0
        unknown_in_program = 0
        for key, count in frequencies.items():
            if key not in addrs:
                unknown_retired += count
                unknown_in_program += 1
                if args.identify_unknown:
                    logger.error("unknown instruction at {} offset {:x}".format(
                        key[0],
                        key[1],
                    ))
        categories_freqs = count_categories(addrs, frequencies)
        categories_counts = count_categories(addrs)
        total_retired = sum(frequencies.values())
        total_count = len(addrs)
        writer = csv.DictWriter(sys.stdout,
            ['category', 'retired', '% retired', 'in program', '% in program']
        )
        writer.writeheader()
        if unknown_retired > 0:
            writer.writerow({
                'category': 'unknown/ignored instructions',
                'retired': unknown_retired,
                '% retired': unknown_retired * 100.0 / total_retired,
                'in program': unknown_in_program,
                '% in program': unknown_in_program * 100.0 / total_count,
            })
        for k in map(lambda k: k[1], interesting_categories):
            v = categories_freqs[k]
            writer.writerow({
                'category': k,
                'retired': categories_freqs[k],
                '% retired': categories_freqs[k] * 100.0 / total_retired,
                'in program': categories_counts[k],
                '% in program': categories_counts[k] * 100.0 / total_count,
            })
