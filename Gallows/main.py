import random

themes = {
    'еда': ["бутерброд", "булочка", "чай", "кофе", "сахар", "каша", "сыр", "колбаса", "сосиски", "соль", "перец",
            "салат",
            "суп", "мясо", "курица", "рыба", "котлета", "картошка", "помидор", "овощь", "суп", "хлеб", "масло",
            "напиток",
            "молоко", "сок", 'фрукт'
            ],
    'спорт': ["спорт", "спортсмен", "футболист", "болельщик", "победитель", "матч", "соревнование"],
    'архитектура': ['апсида', 'архитектура', 'веранда', 'выставка', 'баптистерий', 'дизайнер', 'конструкция',
                    'известь', 'кузница', 'купол', 'мрамор', 'особенность', 'особняк', 'подмастерье',
                    'подпорка', 'тротуар', 'фасад'
                    ]
}
step = [
    '''


      O
     /|\\
      |
     / \\


''', '''


      O
     /|\\
      |
     / \\

=============
''',
    '''

|     
|     O
|    /|\\
|     |
|    / \\
|
=============
''',
    '''
===========  
| /   
|/    O
|    /|\\
|     |
|    / \\
|
=============
''',
    '''
===========  
| /   |
|/    O
|    /|\\
|     |
|    / \\
|
=============
''', '''
===========  
| /   |
|/   (X)
|    /|\\
|     |
|    / \\
|
=============
'''
]

while True:
    alf = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    tries = 0
    list_theme = ', '.join([i[0].upper() + i[1:] for i in themes.keys()])
    th = input("Выберите тему (" + list_theme + "): ").lower().strip()

    if th in themes:
        word = themes[th][random.randrange(0, len(themes[th]))].upper()
    else:
        print('Ну как хотеите)')
        break
    # print(word)
    hide = ['_'] * len(word)
    while True:
        # print('Осталось попыток:', tries, end='\n\n')
        print(step[tries] if '_' in hide else step[0])
        print(' '.join(hide) if tries != len(step) - 1 else ' '.join(word), end='\n\n')

        if '_' not in hide:
            print('Вы не повелисиль)')
            break
        elif tries == len(step) - 1:
            print('Увы вы повесились(')
            break
        else:
            print('Доступные буквы:')
            print(' '.join(alf))
            while True:
                letter = input('Ваша буква: ').upper().strip()
                if letter == '':
                    pass
                elif letter in alf:
                    break
                else:
                    if len(letter) > 1 or letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                        print('Неверный ввод')
                    else:
                        print('Вы уже её использовали')

            flag = True
            for i in range(len(word)):
                if word[i] == letter:
                    hide[i] = letter
                    flag = False
            if flag:
                tries += 1
            alf.remove(letter)
