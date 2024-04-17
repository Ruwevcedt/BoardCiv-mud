from random import shuffle

from Attributes import Letter, KING, ALL_SUITS, NONE_SUIT, QUEEN, ZOKER, ACE, TEN
from Cards import Card
from Field import move_cards
from Nations import ALL_NATIONS, Nation
from Nature import NATURE
from Players import ALL_PLAYERS, Player


def search_player_by_nation(nation: Nation) -> Player:
    return ALL_PLAYERS[ALL_NATIONS.index(nation)]


def distribute_king() -> None:
    [move_cards(from_field=NATURE.deck, cards=NATURE.deck.search_cards(suits=[_nation.suit], letters=[KING]),
                to_field=_nation.throne) for _nation in ALL_NATIONS]


def shuffle_deck() -> None:
    shuffle(NATURE.deck)


def draw(nation: Nation, quantity: int) -> None:
    # _possible_max_quantity = len(NATURE.deck)
    move_cards(from_field=NATURE.deck,
               cards=NATURE.deck[:min(quantity, len(NATURE.deck))],
               to_field=nation.people)


def check_can_start_game() -> bool:
    return True if sum([_nation.check_is_playable() for _nation in ALL_NATIONS]) == len(ALL_NATIONS) else False


def search_foreign_cards_from_hands(nation: Nation) -> list[Card]:
    return nation.people.search_cards(suits=[_suit for _suit in ALL_SUITS if _suit not in [NONE_SUIT, nation.suit]])


def send_foreign_cards_to_deck(nation: Nation) -> None:
    move_cards(from_field=nation.people,
               cards=search_foreign_cards_from_hands(nation=nation),
               to_field=NATURE.deck)


def draw_until_five_people(nation: Nation) -> None:
    draw(nation=nation, quantity=5 - len(nation.people))


def mulligan() -> None:
    """
    for _nation in ALL_NATIONS:
        if not _nation.check_is_playable():
            send_foreign_cards_to_deck(nation=_nation)
            draw_until_five_people(nation=_nation)
    """
    [(send_foreign_cards_to_deck(nation=_nation),
      draw_until_five_people(nation=_nation)) for _nation in ALL_NATIONS
     if not _nation.check_is_playable()]


def genesis() -> None:
    distribute_king()
    shuffle_deck()
    [draw(nation=_nation, quantity=5) for _nation in ALL_NATIONS]
    while not check_can_start_game():
        mulligan()


def activate_specialists(special_letters: list[Letter], nation: Nation, player: Player) -> bool:
    specialists = nation.shadow_cabinet.search_cards(suits=[NONE_SUIT, nation.suit], letters=special_letters)
    if specialists:
        if player.make_a_decision():
            move_cards(from_field=nation.shadow_cabinet, cards=specialists, to_field=nation.opened_cabinet)
            return True
    return False


def activate_queen_of_spring(nation: Nation, player: Player) -> None:
    if activate_specialists(special_letters=[QUEEN], nation=nation, player=player):
        draw(nation=nation, quantity=1)


def spring() -> None:
    for _nation in ALL_NATIONS:
        draw(nation=_nation, quantity=1)

        # _player = search_player_by_nation(nation=_nation)
        activate_queen_of_spring(nation=_nation, player=search_player_by_nation(nation=_nation))


def clear_cabinet(nation: Nation) -> None:
    move_cards(from_field=nation.shadow_cabinet, cards=nation.shadow_cabinet, to_field=nation.people)
    move_cards(from_field=nation.opened_cabinet, cards=nation.opened_cabinet, to_field=NATURE.deck)


def assign_cabinet(nation: Nation, cards: list[Card]) -> None:
    move_cards(from_field=nation.people, cards=cards, to_field=nation.shadow_cabinet)


def summer() -> None:
    for _nation in ALL_NATIONS:
        clear_cabinet(nation=_nation)

        _player = search_player_by_nation(nation=_nation)

        _candidates = _nation.people.search_cards(suits=[NONE_SUIT, _nation.suit])
        _quantity = _player.select_quantity(minimum=0, maximum=min(2, len(_candidates)), quantity=1)[0]
        assign_cabinet(nation=_nation, cards=_player.select_cards(cards=_candidates, quantity=_quantity))


def show_cards(nation: Nation, cards: list[Card]) -> None:
    move_cards(from_field=nation.people, cards=cards, to_field=nation.drafted_people)


def suggest_a_card(nation: Nation, player: Player) -> None:
    show_cards(nation=nation, cards=player.select_cards(cards=nation.people, quantity=1))


def clear_suggested_cards(nation: Nation) -> None:
    move_cards(from_field=nation.drafted_people, cards=nation.drafted_people, to_field=nation.people)


def give_card_to_target(nation: Nation, target_nation: Nation) -> None:
    move_cards(from_field=nation.drafted_people, cards=nation.drafted_people, to_field=target_nation.people)


def get_card_from_target(nation: Nation, target_nation: Nation) -> None:
    move_cards(from_field=target_nation.drafted_people, cards=target_nation.drafted_people, to_field=nation.people)


def exchange_cards(nation: Nation, target_nation: Nation) -> None:
    give_card_to_target(nation=nation, target_nation=target_nation)
    get_card_from_target(nation=nation, target_nation=target_nation)


def diplomacy_conflict(nation: Nation, player: Player,
                       target_nation: Nation, target_player: Player) -> bool:
    _diplomacy_specialists_letters = [ZOKER, ACE, TEN]
    return True if activate_specialists(special_letters=_diplomacy_specialists_letters,
                                        nation=nation, player=player) or \
                   activate_specialists(special_letters=_diplomacy_specialists_letters,
                                        nation=target_nation, player=target_player) else False


def cold_war(nation: Nation, target_nation: Nation) -> bool or None:
    _specialist_letter = nation.opened_cabinet[0].letter
    _target_specialist_letter = target_nation.opened_cabinet[0].letter

    if _specialist_letter == _target_specialist_letter:
        return None


def fall() -> None:
    for _nation in ALL_NATIONS:
        _player = search_player_by_nation(nation=_nation)

        _target_nation = _player.aim_a_nation_for_a_diplomacy()
        _target_player = search_player_by_nation(nation=_target_nation)

        _trial = 3
        while _trial > 0:
            suggest_a_card(nation=_nation, player=_player)
            suggest_a_card(nation=_target_nation, player=_target_player)

            if _player.make_a_decision() & _target_player.make_a_decision():
                if diplomacy_conflict(nation=_nation, player=_player,
                                      target_nation=_target_nation, target_player=_target_player):

                    pass  # todo
                else:
                    exchange_cards(nation=_nation, target_nation=_target_nation)
                break
            else:
                clear_suggested_cards(nation=_nation)
                clear_suggested_cards(nation=_target_nation)
                _trial -= 1


genesis()
spring()
summer()
fall()
