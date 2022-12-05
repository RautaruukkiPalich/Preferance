from pprint import pprint
import time


def check_digit(number: str) -> bool:
    """проверка введёного значения на то, что это число типа int, а не какого либо другого"""
    if number.isdigit():
        if not float(number) % 1:
            return True
    return False


def choose_act_batch(actual_pas: int) -> int:
    """валидация выбора игры"""
    available = [1, 2, 8, 9, 10, 15] + [7 if actual_pas in [1, 2] else 1] + [6 if actual_pas in [1] else 1]
    act_batch = input(
        f"Укажите тип игры, которая будет сыграна на основании торгов:\n"
        f"1 - Мизер\n"
        f"2 - Распасы\n"
        f"{'6 - Шестерная' if actual_pas in [1] else '---'}\n"
        f"{'7 - Семерная' if actual_pas in [1, 2] else '---'}\n"
        f"8 - Восьмерная\n"
        f"9 - Девятерная\n"
        f"10 - Десятерная\n"
        f"15 - Показать промежуточные результаты\n"
    )
    if check_digit(act_batch):
        if int(act_batch) in available:
            return int(act_batch)
    print("Указано невалидное число\n")
    time.sleep(1)
    return choose_act_batch(actual_pas)


def choose_player(players: list) -> str:
    """выбор играющего"""
    text = f'Выберите играющего:\n'+"\n".join(f"{pos} - {player}" for pos, player in enumerate(players, start=1))+'\n'
    pos = input(text)
    if check_digit(pos):
        if 0 < int(pos) < len(players)+1:
            return players[int(pos)-1]
    print("Указано невалидное число\n")
    time.sleep(1)
    return choose_player(players)


def choose_act_input(text: str) -> str:
    """вопрос с Да/Нет"""
    available = ['да', 'нет']
    choose = input(text)
    if choose.isalpha():
        if choose.lower() in available:
            return choose.lower()
    print("Указано невалидное значение")
    time.sleep(1)
    return choose_act_input(text)


def check_played(bid: int) -> list:
    """проверка, взял ли играющий своё"""
    result = choose_act_input("Играющий взял своё? (Да / Нет)")
    match result:
        case 'да':
            return ['Пуля', bid]
        case 'нет':
            amount = check_mt("Сколько не добрал?", "")
            return ['Гора', bid * amount]


def check_mt(text: str, player: str) -> int:
    """начисление горы, вистов + проверка на валидность"""
    bid = input(f'{text} {player}: ')
    if check_digit(bid):
        if 0 <= int(bid) <= 10:
            return int(bid)
    print("Указано невалидное число\n")
    return check_mt(text, player)


def print_result(users_info: dict):
    """вывод на печать текущей таблицы"""
    pprint(users_info)
    print('- - - - - - - - - - - - - - - - -')


def check_mount_20(users_info: dict, players: list) -> dict:
    """проверка горы на превышение значения 20"""
    vacant_users = list()
    overbul = list()

    for i in players:
        actual_bul = users_info[i][0]['Пуля']
        if actual_bul < 20:
            vacant_users.append((i, actual_bul))
        if actual_bul > 20:
            overbul = (i, actual_bul)
    vacant_users = sorted(vacant_users,
                          key=lambda x: x[1],
                          reverse=True
                          )
    if overbul and vacant_users:
        vacant_score = overbul[1] - 20
        if vacant_score > 20 - vacant_users[0][1]:
            vacant_score = 20 - vacant_users[0][1]
        user_nedobul = vacant_users[0][0]
        user_overbul = overbul[0]
        users_info[user_nedobul][0]['Пуля'] += vacant_score
        users_info[user_overbul][0]['Пуля'] -= vacant_score
        users_info[user_overbul][0]['Висты'][0][f'Висты на {user_nedobul}'] += vacant_score * 10

    return users_info


def check_final(users_info: dict, players: list) -> bool:
    """проверка на окончание игры"""
    return sum(users_info[player][0]['Пуля'] for player in players) >= len(players)*20


def calculation(users_info: dict, players: list) -> dict:
    """финальный расчёт"""

    print_result(users_info)

    result = {f"{x}": 0 for x in players}

    for player in players:
        tmp = users_info[player][0]
        users_info[player][0]['Гора'] = tmp['Гора'] - ((tmp['Пуля'] - 20) if tmp['Пуля'] >= 20 else 0)
        users_info[player][0]['Пуля'] = 20

    for player in players:
        pl_mount = users_info[player][0]['Гора']
        set_players = list(set(players) - {player, })
        for gamer in set_players:
            users_info[gamer][0]['Висты'][0][f'Висты на {player}'] += pl_mount * 10

    for i in range(len(players) - 1):
        for j in range(i + 1, len(players)):
            tmp1 = users_info[players[i]][0]['Висты'][0][f'Висты на {players[j]}']
            tmp2 = users_info[players[j]][0]['Висты'][0][f'Висты на {players[i]}']

            result1, result2 = tmp1 - tmp2, tmp2 - tmp1

            result[players[i]] += result1
            result[players[j]] += result2

    print_result(users_info)

    return result
