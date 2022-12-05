from helpers import calculation, check_mount_20, check_final, print_result
from batch import batch
import time
import random


def count_players() -> int:
    """запрашиваем число игроков. проверяем на валидность введёное число"""
    count = int(input('Укажите количество игроков в партии: '))
    if 2 < count < 5:
        return count
    print('В игре могут участвовать 3 или 4 человека')
    return count_players()


def create_vist_dict(players: list, player: list) -> list[dict]:
    """заполняем словари для вистов против других участников"""
    return [{f"Висты на {elem}": 0 for elem in set(players) - set(player)}]


def start_game() -> (dict, list):
    """начало игры. формируем json для последующего заполнения. формируем порядок игроков"""

    queue = ['первого', 'второго', 'третьего', 'четвёртого']
    max_players = count_players()
    users_info = dict()

    for i in range(max_players):
        name = input(f'Укажите имя {queue[i]} игрока: ')
        # поправить передачу одного имени
        users_info[name] = [{"Пуля": 0, "Гора": 0, "Висты": []}]

    players = list(users_info.keys())

    for player in players:
        users_info[player][0]['Висты'] = create_vist_dict(players, [player, ''])

    for i in range(random.randint(5, 20)):
        random.shuffle(players)

    print("Генерирую очередность ходов\n")

    time.sleep(1)

    for pos, name in enumerate(players, start=1):
        print(f"{pos}-{['', 'ый', 'ой', 'ий', 'ый'][pos]}: {name}")

    time.sleep(1)

    print(f"Начнём нашу игру\n")

    return users_info, players


def game():

    users_info, players = start_game()
    actual_pas = 1

    while True:
        users_info, players, actual_pas = batch(users_info, players, actual_pas)
        # поверка на необходимость перекидывать гору 3 раза (пока не эффективно)
        ## проверка на гору > 20
        for _ in range(3):
            for player in players:
                actual_bul = users_info[player][0]['Пуля']
                if actual_bul > 20:
                    users_info = check_mount_20(
                        users_info,
                        players,
                        )
        # проверка на окончание игры
        if check_final(
            users_info,
            players,
        ):
            break
        print_result(users_info)
    result = calculation(
        users_info,
        players,
        )

    print('\n'.join(f"{key:>8}: {value:>5} вистов" for key, value in sorted(
        result.items(),
        key=lambda item: item[1],
        reverse=True
        )
      )
    )


if __name__ == '__main__':
    game()


