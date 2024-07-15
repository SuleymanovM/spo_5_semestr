def ErorrCheck(lines, kwords):
    check_while = 0
    while_space = 0
    check_break = 0
    last_letter = 0
    last_count_spaces = 0
    # проверка табуляции
    for line in lines:
        check_line = line.lstrip()
        if check_line[0] != '#':
            spaces = len(line)-len(check_line)
            if check_while == 1 and check_break == 0 and spaces <= while_space:
                return False
            check_line_split = check_line.split(' ')
            if check_line_split[0] == 'while' or check_line_split[0] == 'While':
                while_space = spaces
                check_while = 1
            if spaces % 4 != 0:
                return False
            elif last_letter == 1:
                if spaces <= last_count_spaces:
                    return False
                elif (spaces - last_count_spaces) > 4:
                    return False
                else:
                    last_count_spaces = spaces
            if last_letter != 1:
                if spaces > last_count_spaces:
                    return False
            if check_line[-2] == ':':
                last_letter = 1
            else:
                last_letter = 0
            if check_line_split[-1] == 'break\n' or check_line_split[-1] == 'Break\n' or check_line_split[-1] == 'break' or check_line_split[-1] == 'Break':
                check_break = 1
    # проверка наличия ':'
    for line in lines:
        check_line = line.lstrip()
        if check_line[0] in kwords and check_line[-2] != ':' and check_line[0] != 'break':
            return False
    # проверка закрытия цикла While
    if check_while == 1 and check_break == 0:
        return False
    # проверка на инициализацию переменных
    variables = []
    for line in lines:
        check_line = line.lstrip()
        check_line_split = check_line.split(' ')
        if len(check_line_split) > 1:
            if check_line_split[1] == '=':
                variables.append(check_line_split[0])
                word = check_line_split[2]
                word = word[:-1]
                if not word.isdigit():
                    if word not in variables:
                        return False
            if check_line_split[1] == '+=' and check_line_split[0] not in variables:
                return False
            if check_line_split[0] in kwords and check_line_split[1] not in kwords:
                if check_line_split[1] not in variables:
                    return False
        # проверка скобок в print()
        if len(check_line_split) == 1:
            bracket_open = 0
            bracket_close = 0
            for i in check_line_split[0]:
                if i == '(':
                    bracket_open += 1
                elif i == ')':
                    bracket_close += 1
                    if bracket_close > bracket_open:
                        return False
            if bracket_close != bracket_open:
                return False
    return True


def Tree(lines):
    op1 = {'if', 'while', '=', '+='}
    op2 = {'>=', 'True:', 'True'}
    tilda = []
    tilda_check = 0
    staples = 0
    count = 0
    kloop = 0
    kop2 = 0
    sentence = []
    file.write('#include <iostream>\n')
    file.write('\n')
    file.write('int main() {\n')
    for line in lines:
        tilda_check = 0
        for i in line:
            if i == '`':
                tilda_check += 1
        word = line[tilda_check:-1]
        if word == '=' or word == '+=':
            sentence.append(word)
        elif word == 'while':
            sentence.append(word)
        elif word == 'print':
            sentence.append('std::cout')
        elif word == 'if':
            sentence.append(word + ' (')
        elif word == 'break':
            sentence.append('    ')
            sentence.append(word+';')
            if kloop == 1:
                sentence.insert(1, '    ')
            if kloop == 2:
                sentence.insert(1, '        ')
            for i in sentence:
                file.write(i)
            file.write('\n')
            sentence.clear()
        elif len(sentence) > 0 and (sentence[0] == '=' or sentence[0] == '+='):
            tilda.clear()
            for i in line:
                if i == '`':
                    tilda += '`'
            if len(tilda) >= 8:
                sentence.insert(0, '        ')
            elif len(tilda) >= 4:
                sentence.insert(0, '    ')
            if sentence[-1] == '=':
                sentence.insert(0, 'int ')
            sentence.insert(1, word + ' ')
        elif len(sentence) > 0 and (sentence[-1] == '=' or sentence[-1] == '+='):
            tilda.clear()
            for i in line:
                if i == '`':
                    tilda += '`'
            sentence.append(' ' + word + ';')
            sentence.insert(0, '    ')
            for i in sentence:
                file.write(i)
            file.write('\n')
            sentence.clear()
        elif len(sentence) == 1 and sentence[0] == 'while':
            tilda.clear()
            for i in line:
                if i == '`':
                    tilda += '`'
            if len(tilda) >= 8:
                sentence.insert(0, '        ')
            elif len(tilda) >= 4:
                sentence.insert(0, '    ')
            sentence.append('(' + word + ')' + ' ')
        elif len(sentence) > 0 and sentence[0] == 'while':
            sentence.append('{')
            sentence.insert(0, '    ')
            for i in sentence:
                file.write(i)
            file.write('\n')
            sentence.clear()
            kloop += 1
        elif len(sentence) > 0 and sentence[0] == 'std::cout':
            tilda.clear()
            for i in line:
                if i == '`':
                    tilda += '`'
            if len(tilda) >= 8:
                sentence.insert(0, '        ')
            elif len(tilda) >= 4:
                sentence.insert(0, '    ')
            sentence.append('<<')
        elif len(sentence) > 0 and sentence[-1] == '<<' and staples == 1:
            tilda.clear()
            sentence.append(' ' + word + ' << std::endl;')
            if kloop == 1:
                sentence.insert(1, '    ')
            if kloop == 2:
                sentence.insert(1, '        ')
            for i in sentence:
                file.write(i)
            file.write('\n')
            sentence.clear()
            staples = 0
        elif len(sentence) > 0 and sentence[-1] == '<<':
            staples = 1
        elif len(sentence) > 0 and sentence[0] == 'if (':
            tilda.clear()
            for i in line:
                if i == '`':
                    tilda += '`'
            if len(tilda) >= 8:
                sentence.insert(0, '        ')
            elif len(tilda) >= 4:
                sentence.insert(0, '    ')
            sentence.append(word)
        elif len(sentence) > 1 and sentence[-2] == 'if (':
            sentence.insert(-1, word + ' ')
        elif len(sentence) > 2 and sentence[-3] == 'if (':
            sentence.append(' ' + word + ')')
        elif len(sentence) > 3 and sentence[-4] == 'if (':
            sentence.append(' {')
            sentence.insert(0, '    ')
            for i in sentence:
                file.write(i)
            file.write('\n')
            sentence.clear()
            kloop += 1
    while True:
        if kloop < 1:
            break
        file.write('    ' * kloop + '}\n')
        kloop -= 1
    file.write('    return 0;\n')
    file.write('}')



kwords = {'while', 'While', 'Print', 'print', 'if', 'If', 'elif', 'Elif', 'Else', 'else', 'True', 'True:\n', 'break', 'Break'}
operators = {'=', '<=', '>=', '>', '<', '==', ')', '(', '+', '-', '*', '/', ':', }
file = open('input.txt', 'r')
lines = file.readlines()
if True:
    file.close()
    file = open('output.txt', 'w')
    Tree(lines)
    print('fine')
else:
    file.close()
    file = open('output.txt', 'w')
    file.write('Sorry but your program is broken')
    print('Sorry but your program is broken')
