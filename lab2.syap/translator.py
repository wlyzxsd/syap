def translate_cpp_if(cpp_code):
    lines = cpp_code.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if line.startswith('//'):
            i += 1
            continue

        if line.startswith('/*'):
            while i < len(lines) and '*/' not in lines[i]:
                i += 1
            i += 1
            continue

        if line.startswith('if ('):
            start = line.find('(') + 1
            end = line.find(')')
            if start > 0 and end > start:
                condition = line[start:end]
                condition = condition.replace('&&', 'and')
                condition = condition.replace('||', 'or')
                condition = condition.replace('!', 'not ')
                condition = condition.replace('true', 'True')
                condition = condition.replace('false', 'False')
                result.append(f'if {condition}:')

                i += 1
                brace_count = 1
                while i < len(lines) and brace_count > 0:
                    next_line = lines[i].strip()
                    if '{' in next_line:
                        brace_count += 1
                    if '}' in next_line:
                        brace_count -= 1
                    if brace_count > 0 and next_line and not next_line.startswith('//'):
                        translated = translate_simple_line(next_line)
                        if translated:
                            result.append('    ' + translated)
                    i += 1

        elif line.startswith('else if ('):
            start = line.find('(') + 1
            end = line.find(')')
            if start > 0 and end > start:
                condition = line[start:end]
                condition = condition.replace('&&', 'and')
                condition = condition.replace('||', 'or')
                condition = condition.replace('!', 'not ')
                condition = condition.replace('true', 'True')
                condition = condition.replace('false', 'False')
                result.append(f'elif {condition}:')

                i += 1
                brace_count = 1
                while i < len(lines) and brace_count > 0:
                    next_line = lines[i].strip()
                    if '{' in next_line:
                        brace_count += 1
                    if '}' in next_line:
                        brace_count -= 1
                    if brace_count > 0 and next_line and not next_line.startswith('//'):
                        translated = translate_simple_line(next_line)
                        if translated:
                            result.append('    ' + translated)
                    i += 1

        elif line.startswith('else'):
            result.append('else:')

            i += 1
            brace_count = 1
            while i < len(lines) and brace_count > 0:
                next_line = lines[i].strip()
                if '{' in next_line:
                    brace_count += 1
                if '}' in next_line:
                    brace_count -= 1
                if brace_count > 0 and next_line and not next_line.startswith('//'):
                    translated = translate_simple_line(next_line)
                    if translated:
                        result.append('    ' + translated)
                i += 1

        else:
            i += 1

    return '\n'.join(result) if result else "# Нет if конструкций"


def translate_cpp_for(cpp_code):
    lines = cpp_code.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if line.startswith('//'):
            i += 1
            continue

        if line.startswith('/*'):
            while i < len(lines) and '*/' not in lines[i]:
                i += 1
            i += 1
            continue

        if line.startswith('for ('):
            start = line.find('(') + 1
            end = line.find(')')
            if start > 0 and end > start:
                for_parts = line[start:end]
                parts = for_parts.split(';')

                if len(parts) == 3:
                    init, condition, increment = parts
                    init = init.strip()
                    condition = condition.strip()
                    increment = increment.strip()

                    if 'int i=' in init and 'i++' in increment:
                        eq_pos = init.find('=')
                        lt_pos = condition.find('<')
                        if eq_pos != -1 and lt_pos != -1:
                            start_num = init[eq_pos+1:].strip()
                            end_num = condition[lt_pos+1:].strip()
                            if start_num.isdigit() and end_num.isdigit():
                                result.append(f'for i in range({start_num}, {end_num}):')

                                i += 1
                                brace_count = 1
                                while i < len(lines) and brace_count > 0:
                                    next_line = lines[i].strip()
                                    if '{' in next_line:
                                        brace_count += 1
                                    if '}' in next_line:
                                        brace_count -= 1
                                    if brace_count > 0 and next_line and not next_line.startswith('//'):
                                        translated = translate_simple_line(next_line)
                                        if translated:
                                            result.append('    ' + translated)
                                    i += 1
                            else:
                                result.append(f'# for {init}; {condition}; {increment}')
                                i += 1
                        else:
                            result.append(f'# for {init}; {condition}; {increment}')
                            i += 1
                    elif 'int j=' in init and 'j++' in increment:
                        eq_pos = init.find('=')
                        lt_pos = condition.find('<')
                        if eq_pos != -1 and lt_pos != -1:
                            start_num = init[eq_pos+1:].strip()
                            end_num = condition[lt_pos+1:].strip()
                            if start_num.isdigit() and end_num.isdigit():
                                result.append(f'for j in range({start_num}, {end_num}):')

                                i += 1
                                brace_count = 1
                                while i < len(lines) and brace_count > 0:
                                    next_line = lines[i].strip()
                                    if '{' in next_line:
                                        brace_count += 1
                                    if '}' in next_line:
                                        brace_count -= 1
                                    if brace_count > 0 and next_line and not next_line.startswith('//'):
                                        translated = translate_simple_line(next_line)
                                        if translated:
                                            result.append('    ' + translated)
                                    i += 1
                            else:
                                result.append(f'# for {init}; {condition}; {increment}')
                                i += 1
                        else:
                            result.append(f'# for {init}; {condition}; {increment}')
                            i += 1
                    else:
                        result.append(f'# for {init}; {condition}; {increment}')
                        i += 1
                else:
                    result.append(f'# for: {for_parts}')
                    i += 1
            else:
                i += 1
        else:
            i += 1

    return '\n'.join(result) if result else "# Нет for циклов"


def translate_cpp_cout(cpp_code):
    lines = cpp_code.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if line.startswith('//'):
            i += 1
            continue

        if line.startswith('/*'):
            while i < len(lines) and '*/' not in lines[i]:
                i += 1
            i += 1
            continue

        if line.startswith('cout <<'):
            parts = line.split('<<')
            output_parts = []
            for part in parts[1:]:
                part = part.strip().rstrip(';')
                if part == 'endl':
                    output_parts.append('"\\\\n"')
                else:
                    output_parts.append(part)
            if output_parts:
                result.append(f'print({", ".join(output_parts)})')
            i += 1

        elif line.startswith('std::cout <<'):
            parts = line.split('<<')
            output_parts = []
            for part in parts[1:]:
                part = part.strip().rstrip(';')
                if part == 'endl':
                    output_parts.append('"\\\\n"')
                else:
                    output_parts.append(part)
            if output_parts:
                result.append(f'print({", ".join(output_parts)})')
            i += 1

        elif line.startswith('cin >>'):
            parts = line.split('>>')
            if len(parts) >= 2:
                var_name = parts[1].strip().rstrip(';')
                result.append(f'{var_name} = input()')
            i += 1

        elif line.startswith('std::cin >>'):
            parts = line.split('>>')
            if len(parts) >= 2:
                var_name = parts[1].strip().rstrip(';')
                result.append(f'{var_name} = input()')
            i += 1

        else:
            i += 1

    return '\n'.join(result) if result else "# Нет cout/cin конструкций"


def translate_simple_line(line):
    line = line.strip()
    if not line or line.startswith('//') or line in ['{', '}']:
        return None

    line = line.rstrip(';')

    if line.startswith('cout <<'):
        parts = line.split('<<')
        output_parts = []
        for part in parts[1:]:
            part = part.strip()
            if part == 'endl':
                output_parts.append('"\\\\n"')
            else:
                output_parts.append(part)
        return f'print({", ".join(output_parts)})'

    elif line.startswith('cin >>'):
        parts = line.split('>>')
        if len(parts) >= 2:
            var_name = parts[1].strip()
            return f'{var_name} = input()'

    elif line and not line.startswith('//'):
        return line

    return None


def simple_cpp_to_python(cpp_code):
    result = []
    result.append("констркуции c if")
    result.append(translate_cpp_if(cpp_code))
    result.append("\nцикл for")
    result.append(translate_cpp_for(cpp_code))
    result.append("\nвывод/ввод")
    result.append(translate_cpp_cout(cpp_code))
    return '\n'.join(result)


if __name__ == "__main__":
    test_code = """
    if (x > 10) {
        cout << "x больше 10" << endl;
    }
    for (int i = 0; i < 3; i++) {
        cout << "i = " << i << endl;
    }
    cout << "Готово";
    """
    print("\nИсходный код C++:")
    print(test_code)
    print("\nРезультат трансляции:")
    result = simple_cpp_to_python(test_code)
    print(result)