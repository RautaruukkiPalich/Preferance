from helpers import check_mt, check_played, choose_player, choose_act_batch, choose_act_input, print_result
import time


def check_butch_result_mizer(users_info: dict, gambler: str) -> dict:
    """мизер"""
    bid = check_played(10)
    users_info[gambler][0][bid[0]] += bid[1]
    return users_info


def check_butch_result_pas(users_info: dict, players: list, actual_pas: int) -> (dict, int):
    """распасы"""
    bid_value = actual_pas*2
    for player in players:
        users_info[player][0]['Гора'] += check_mt('Сколько взяток взял', player) * bid_value
    actual_pas += 1
    return users_info, actual_pas


def check_butch_result(users_info: dict, gambler: str, players: list, amount: int) -> dict:
    """6, 7, 8, 9, 10"""
    bid_value = {6: 2, 7: 4, 8: 6, 9: 8, 10: 10}[amount]
    bid = check_played(bid_value)
    users_info[gambler][0][bid[0]] += bid[1]
    check_vist = choose_act_input('Вистующие взяли своё?')
    set_players = list(set(players) - {gambler, })
    if check_vist == 'нет':
        for player in set_players:
            count = check_mt('Сколько взяток не добрал', player)
            users_info[player][0]['Гора'] += bid_value * count
    for player in set_players:
        count = check_mt('Сколько взяток взял', player)
        users_info[player][0]['Висты'][0][f'Висты на {gambler}'] += bid_value * count
    return users_info


def batch(users_info: dict, players: list, actual_pas: int) -> (dict, list, int):
    """"""

    print(f"Раздачу ведёт {players[0]}\n")
    time.sleep(2)

    act_batch = choose_act_batch(actual_pas)
    match act_batch:
        case 1:
            gambler = choose_player(players if len(players) == 3 else players[1:])
            users_info, actual_pas = check_butch_result_mizer(users_info,
                                                              gambler,
                                                              ), 1

        case 2:
            users_info, actual_pas = check_butch_result_pas(users_info,
                                                            players,
                                                            actual_pas,
                                                            )

        case 15:
            print_result(users_info)
            return batch(
                users_info,
                players,
                actual_pas,
            )

        case _:
            gambler = choose_player(players if len(players) == 3 else players[1:])
            users_info, actual_pas = check_butch_result(users_info,
                                                        gambler,
                                                        players,
                                                        act_batch,
                                                        ), 1

    if actual_pas in [1, 4]:
        if actual_pas == 4:
            users_info[players[0]][0]['Гора'] += 2
        players.insert(-1, players.pop(0))
        actual_pas = 1

    return users_info, players, actual_pas
