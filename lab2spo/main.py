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
    tilda ='``'
    count = 0
    kloop = 0
    kop2 = 0
    for line in lines:
        line = line.lstrip()
        line = line.split()
        for i in line:
            if kloop == 0:
                if i in op1:
                    file.write(i + '\n')
                if i in op2:
                    if i[-1] == ':':
                        file.write(tilda * (count + 1) + i[:-1] + '\n')
                    else:
                        file.write(tilda * (count + 1) + i + '\n')
                    kop2 = 1
            if kloop != 0:
                if i in op1:
                    file.write(tilda * count + i + '\n')
                if i in op2:
                    file.write(tilda * (count + 1) + i+'\n')
                    kop2 = 1
        for i in line:
            if len(line) == 1:
                if i == 'break\n' or i == 'break':
                    file.write(tilda * (count + 1) + 'break'+'\n')
                else:
                    file. write(tilda * count + 'print'+'\n')
                    file.write(tilda * count + '('+'\n')
                    file.write(tilda * count + ')'+'\n')
                    k = 0
                    for j in i:
                        if j == ')':
                            k = 0
                        if k == 1:
                            file.write(tilda * (count + 1) + j+'\n')
                        if j == '(':
                            k = 1
            else:
                if i not in op1 and i not in op2:
                    if i[-1] == ':':
                        file.write(tilda * (count + 1 + kop2) + i[:-1] + '\n')
                    elif i[-1] == '\n':
                        file.write(tilda * (count + 1 + kop2) + i[:-1] + '\n')
                    else:
                        file.write(tilda * (count + 1 + kop2) + i+'\n')
        for i in line:
            if len(i) >= 2:
                if i[-1] == ':':
                    file.write(tilda * (count + 1) + ':'+'\n')
        if line[0] == 'while' or line[0] == 'if':
            count += 2
            kloop += 1
            kop2 = 0


kwords = {'while', 'While', 'Print', 'print', 'if', 'If', 'elif', 'Elif', 'Else', 'else', 'True', 'True:\n', 'break', 'Break'}
operators = {'=', '<=', '>=', '>', '<', '==', ')', '(', '+', '-', '*', '/', ':', }
file = open('input.txt', 'r')
lines = file.readlines()
if ErorrCheck(lines, kwords):
    file.close()
    file = open('output.txt', 'w')
    Tree(lines)
    print('fine')
else:
    file.close()
    file = open('output.txt', 'w')
    file.write('Sorry but your program is broken')
    print('Sorry but your program is broken')

