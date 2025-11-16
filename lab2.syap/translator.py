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
                condition = line[start:end].strip()
                condition = condition.replace('&&', ' and ')
                condition = condition.replace('||', ' or ')
                condition = condition.replace('!', 'not ')
                condition = condition.replace('true', 'True')
                condition = condition.replace('false', 'False')
                condition = ' '.join(condition.split())
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
                condition = line[start:end].strip()
                condition = condition.replace('&&', ' and ')
                condition = condition.replace('||', ' or ')
                condition = condition.replace('!', 'not ')
                condition = condition.replace('true', 'True')
                condition = condition.replace('false', 'False')
                condition = ' '.join(condition.split())
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
                parts = [part.strip() for part in for_parts.split(';')]

                if len(parts) == 3:
                    init, condition, increment = parts

                    condition = condition.replace(' ', '')

                    if 'int' in init and '++' in increment:
                        var_name = init.split('=')[0].replace('int', '').strip()

                        if '<' in condition:
                            parts_cond = condition.split('<')
                            if len(parts_cond) == 2:
                                var_cond, end_val = parts_cond
                                if var_cond == var_name and end_val.isdigit():
                                    start_val = init.split('=')[1].strip()
                                    if start_val.isdigit():
                                        result.append(f'for {var_name} in range({start_val}, {end_val}):')

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

        if line.startswith('cout <<') or line.startswith('std::cout <<'):
            parts = line.split('<<')
            output_parts = []
            for part in parts[1:]:
                part = part.strip().rstrip(';')
                if part != 'endl':
                    cleaned_part = part.strip()
                    output_parts.append(cleaned_part)
            if output_parts:
                result.append(f'print({", ".join(output_parts)})')
            i += 1

        elif line.startswith('cin >>') or line.startswith('std::cin >>'):
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

    if line.startswith('cout <<') or line.startswith('std::cout <<'):
        parts = line.split('<<')
        output_parts = []
        for part in parts[1:]:
            part = part.strip()
            if part != 'endl':
                output_parts.append(part)
        return f'print({", ".join(output_parts)})'

    elif line.startswith('cin >>') or line.startswith('std::cin >>'):
        parts = line.split('>>')
        if len(parts) >= 2:
            var_name = parts[1].strip()
            return f'{var_name} = input()'

    elif line and not line.startswith('//'):
        return line

    return None


def simple_cpp_to_python(cpp_code):
    result = []
    result.append("конструкции c if:")
    result.append(translate_cpp_if(cpp_code))
    result.append("\nциклы for:")
    result.append(translate_cpp_for(cpp_code))
    result.append("\nвывод/ввод:")
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