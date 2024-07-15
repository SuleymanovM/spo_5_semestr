def ErorrCheck(lines, kwords):
    stack = []
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
            if bracket_close != bracket_open:
                return False
    return True


def Analysis(lines, kwords, operators):
    for line in lines:
        line = line.lstrip()
        line = line[:-1]
        line_split = line.split(' ')
        key = 0
        word = ''
        for i in line_split:
            if len(line_split) == 1 and i != 'break':
                for j in i:
                    if j == ')':
                        key = 0
                    if key == 1:
                        word += j
                    if j == '(':
                        key = 1
                file.write('print -> kword\n')
                file.write('( -> operator\n')
                print('print -> kword')
                print('( -> operator')
                if word.isdigit():
                    file.write(word + ' -> number\n')
                    print(word, ' -> number')
                else:
                    file.write(word + ' -> variable\n')
                    print(word, ' -> variable')
                file.write(') -> operator\n')
                print(') -> operator')
            elif i in kwords:
                file.write(i + ' -> kword\n')
                print(i, ' -> kword')
            elif i in operators:
                file.write(i + ' -> operator\n')
                print(i, ' -> operator')
            elif i[-1] == ':':
                a = i[:-1]
                if a in kwords:
                    file.write(a + ' -> kword\n')
                    print(a, ' -> kword')
                elif a in operators:
                    file.write(a + ' -> operator\n')
                    print(a, ' -> operator')
                elif a.isdigit():
                    file.write(a + ' -> number\n')
                    print(a, ' -> number')
                else:
                    file.write(a + ' -> variable\n')
                    print(a, ' -> variable')
                file.write(': -> operator\n')
                print(': -> operator')
            elif i.isdigit():
                file.write(i + ' -> number\n')
                print(i, ' -> number')
            else:
                file.write(i + ' -> variable\n')
                print(i, ' -> variable')



kwords = {'while', 'While', 'Print', 'print', 'if', 'If', 'elif', 'Elif', 'Else', 'else', 'True', 'True:\n', 'break', 'Break'}
operators = {'=', '<=', '>=', '>', '<', '==', ')', '(', '+', '-', '*', '/', ':', }
file = open('input.txt', 'r')
lines = file.readlines()
if ErorrCheck(lines, kwords):
    file.close()
    file = open('output.txt', 'w')
    Analysis(lines, kwords, operators)
    print('fine')
else:
    file.close()
    file = open('output.txt', 'w')
    file.write('Sorry but your program is broken')
    print('Sorry but your program is broken')
