from random import randint
import os
import sys
score_holder = []
score_data = [1, 6, 6, 6, 6, 6]
year = 0
# 7 14
mother = 1

places = {'r': [10, 10], 'f': [15, 10], 'p': [20, 40], 'h': [5, 44]}
start_loc = {'@': [12, 24], 'M': [11, 24]}
moms = [0, 'p', 'h', 'r', 'f']


def make_map():
    draw_map = []
    for i in range(24):
        help_list = []
        if i in [0, 23]:
            for j in range(48): help_list.append('-')
        else:
            help_list.append('|')
            for j in range(46): help_list.append(' ')
            help_list.append('|')
        draw_map.append(help_list)

    text = ['Время года:', 'Здоровье:', 'Еда:', 'Вода:', 'Характер:', 'Настроение:']

    for i in range(len(text)):
        for j in range(len(text[i])):
            draw_map[i + 1][j + 1] = text[i][j]
    return draw_map


text = ['Время года:', 'Здоровье:', 'Еда:', 'Вода:', 'Характер:', 'Настроение:']
for i in text: score_holder.append(len(i) + 2)


def show_map(mp):
    global mother
    for i in mp:
        s = ''
        for j in i:
            if j == 'M' and not mother:
                s += ' '
            else:
                s += j
        print(s)


def add_data(mp, arr=score_data):
    for i in range(len(score_holder)):
        mp[i + 1][score_holder[i]] = str(arr[i])


def add_activity(mp, p=places):
    for i in p.keys():
        help = p[i]
        mp[help[0]][help[1]] = i



def mp_start(m):
    os.system('clear')
    mp_to_show = make_map()
    add_data(mp_to_show)
    add_activity(mp_to_show)
    add_activity(mp_to_show, m)
    show_map(mp_to_show)


def game():
    global year, mother
    local_year = year
    local_season = score_data[0]
    for i in range(local_year, 5):
        year += 1
        for j in range(local_season-1, 4):
            score_data[0] = j + 1
            mp_start(start_loc)
            location = start_loc.copy()
            location['M'] = places[moms[score_data[0]]].copy()
            location['M'][0] -= 1
            input('>напиши что нибудь для продолжения\n>')
            mp_start(location)
            s = input('>выбери куда направишься\n>')
            if s == 'SAVE':
                data_save = ''
                for i in score_data:
                    data_save += str(i) + ' '
                data_save += str(year)
                my_file = open("SAVE.txt", "w+")
                my_file.write(data_save)
                my_file.close()
                print('До встречи!')
                sys.exit()
            if s == moms[score_data[0]]:
                score_data[2] = min(score_data[2] + 2, 9)
                location['@'] = location['M'].copy()
                location['@'][1] -= 1
                for i in [3, 4, 5]:
                    score_data[i] -= 1
            else:
                location['@'] = places[s].copy()
                location['@'][0] -= 1

            if s == 'h':
                score_data[2] = score_data[2] - 1
                for i in [3, 4, 5]:
                    score_data[i] -= 1
            elif s == 'r':
                score_data[3] = min(score_data[3] + 2, 9)
                for i in [2, 4, 5]:
                    score_data[i] -= 1
            elif s == 'p':
                score_data[4] = min(score_data[4] + 1, 9)
                ans = randint(0, 10)
                if ans > score_data[4] + score_data[5]: score_data[1] -= 1
                for i in [2, 4, 3]:
                    score_data[i] -= 1
            else:
                score_data[5] = min(score_data[5] + 1, 9)
                for i in [3, 4, 2]:
                    score_data[i] -= 1
            if score_data[2] + score_data[3] >= 15:
                score_data[1] = min(score_data[1]+1, 9)

            for i in score_data:
                if i <= 0:
                    print('YOU LOSE')
                    sys.exit()

            mp_start(location)
            input('>напиши что нибудь для продолжения\n>')

        mother = 0
        local_season = 1

START = ['Привет! Это симулятор медведя, ты - медведь == @, у тебя есть мама - M, первый год жизни она будет тебя учить.',
         'Ты всегда стартуешь в центре, можешь пойти к реке(r), холму(h), пастбищу(p) или в лес(f)',
         'Каждое перемещение изменяет твои характеристики, если что то обнулится - ты умрешь(',
         'Напиши SAVE вместо хода чтобы сохранить прогресс',
         'Удачи!']


for i in START:
    print(i)

if os.path.exists('SAVE.txt'):
    load = input('Хочешь загрузить существующее сохранение? Y/N\n>')
    if load == 'Y':
        my_file = open('SAVE.txt')
        loaded = my_file.read()
        loaded = loaded.split()
        for i in range(len(score_data)):
            score_data[i] = int(loaded[i])
        year = int(loaded[-1])
        print('Сохранение загружено!')


input('>напиши что нибудь для продолжения\n>')

game()

sm = 0
for i in score_data: sm += i
print('WIN!\nScore:' + str(sm))
