from random import shuffle

from Attributes import Letter, KING, ALL_SUITS, NONE_SUIT, QUEEN, ZOKER, ACE, TEN, NUMBER_LETTERS
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


def mulligan_for_each_nation() -> None:
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
    shuffle(NATURE.deck)
    [draw(nation=_nation, quantity=5) for _nation in ALL_NATIONS]
    while not check_can_start_game():
        mulligan_for_each_nation()


def activate_specialists(special_letters: list[Letter], nation: Nation, player: Player) -> bool:
    specialists = nation.shadow_cabinet.search_cards(suits=[NONE_SUIT, nation.suit], letters=special_letters)
    if specialists:
        if player.make_a_decision():
            move_cards(from_field=nation.shadow_cabinet, cards=specialists, to_field=nation.opened_cabinet)
            return True
    return False


def queen_activated(nation: Nation, player: Player) -> bool:
    return activate_specialists(special_letters=[QUEEN], nation=nation, player=player)


def clear_opened_cabinet(nation: Nation) -> None:
    move_cards(from_field=nation.opened_cabinet, cards=nation.opened_cabinet, to_field=NATURE.deck)


def spring() -> None:
    for _nation in ALL_NATIONS:
        draw(nation=_nation, quantity=1)

        # _player = search_player_by_nation(nation=_nation)
        if queen_activated(nation=_nation, player=search_player_by_nation(nation=_nation)):
            draw(nation=_nation, quantity=1)
            clear_opened_cabinet(nation=_nation)


def clear_cabinet(nation: Nation) -> None:
    move_cards(from_field=nation.shadow_cabinet, cards=nation.shadow_cabinet, to_field=nation.people)
    clear_opened_cabinet(nation=nation)


def assign_cabinet(nation: Nation, cards: list[Card]) -> None:
    move_cards(from_field=nation.people, cards=cards, to_field=nation.shadow_cabinet)


def summer() -> None:
    for _nation in ALL_NATIONS:
        clear_cabinet(nation=_nation)

        _player = search_player_by_nation(nation=_nation)

        _candidates = _nation.people.search_cards(suits=[NONE_SUIT, _nation.suit])
        _quantity = _player.select_quantity(minimum=0, maximum=min(2, len(_candidates)), quantity=1)[0]
        assign_cabinet(nation=_nation, cards=_player.select_cards(cards=_candidates, quantity=_quantity))


def show_people(nation: Nation, people: list[Card]) -> None:
    move_cards(from_field=nation.people, cards=people, to_field=nation.drafted_people)


def suggest_a_card(nation: Nation, player: Player) -> None:
    show_people(nation=nation, people=player.select_cards(cards=nation.people, quantity=1))


def suggest_and_response(nation: Nation, player: Player,
                         target_nation: Nation, target_player: Player) -> None:
    suggest_a_card(nation=nation, player=player)
    suggest_a_card(nation=target_nation, player=target_player)


def negotiation_agreed(player: Player, target_player: Player) -> bool:
    return player.make_a_decision() & target_player.make_a_decision()


def clear_suggested_cards(nation: Nation) -> None:
    move_cards(from_field=nation.drafted_people, cards=nation.drafted_people, to_field=nation.people)


def clear_suggestion_and_response(nation: Nation, target_nation: Nation) -> None:
    clear_suggested_cards(nation=nation)
    clear_suggested_cards(nation=target_nation)


def give_card_to_target(nation: Nation, target_nation: Nation) -> None:
    move_cards(from_field=nation.drafted_people, cards=nation.drafted_people, to_field=target_nation.people)


def get_card_from_target(nation: Nation, target_nation: Nation) -> None:
    move_cards(from_field=target_nation.drafted_people, cards=target_nation.drafted_people, to_field=nation.people)


def exchange_cards(nation: Nation, target_nation: Nation) -> None:
    give_card_to_target(nation=nation, target_nation=target_nation)
    get_card_from_target(nation=nation, target_nation=target_nation)


def specialists_activated_during_diplomacy(nation: Nation, player: Player,
                                           target_nation: Nation, target_player: Player) -> bool:
    _diplomacy_specialists_letters = [ZOKER, ACE, TEN]
    return True if activate_specialists(special_letters=_diplomacy_specialists_letters,
                                        nation=nation, player=player) or \
                   activate_specialists(special_letters=_diplomacy_specialists_letters,
                                        nation=target_nation, player=target_player) else False


def check_specialists_compatibility(nation: Nation, target_nation: Nation) -> bool or None:
    try:
        _specialist_letter = nation.opened_cabinet[0].letter
    except IndexError:
        return False
    try:
        _target_specialist_letter = target_nation.opened_cabinet[0].letter
    except IndexError:
        return True

    if _specialist_letter == _target_specialist_letter:
        return None
    elif _specialist_letter == ZOKER:
        return True if _target_specialist_letter == ACE else False
    elif _specialist_letter == ACE:
        return True if _target_specialist_letter == TEN else False
    elif _specialist_letter == TEN:
        return True if _target_specialist_letter == ZOKER else False


def diplomatic_war(nation: Nation, target_nation: Nation, result: bool or None) -> None:
    if result:
        get_card_from_target(nation=nation, target_nation=target_nation)
    elif result is not None:
        give_card_to_target(nation=nation, target_nation=target_nation)
    clear_suggestion_and_response(nation=nation, target_nation=target_nation)


def clear_both_specialists(nation: Nation, target_nation: Nation) -> None:
    [clear_opened_cabinet(nation=_nation) for _nation in [nation, target_nation]]


def fall() -> None:
    for _nation in ALL_NATIONS:
        _player = search_player_by_nation(nation=_nation)

        _target_nation = _player.aim_a_nation_for_a_diplomacy()  # 손패 없는 상대는 제외됨
        _target_player = search_player_by_nation(nation=_target_nation)

        _negotiation_token = 3
        while _negotiation_token > 0:
            suggest_and_response(nation=_nation, player=_player,
                                 target_nation=_target_nation, target_player=_target_player)

            if negotiation_agreed(player=_player, target_player=_target_player):
                if specialists_activated_during_diplomacy(nation=_nation, player=_player,
                                                          target_nation=_target_nation, target_player=_target_player):
                    # _result_of_diplomatic_war =
                    #   check_specialists_compatibility(nation=_nation, target_nation=_target_nation)
                    diplomatic_war(nation=_nation, target_nation=_target_nation,
                                   result=check_specialists_compatibility(nation=_nation, target_nation=_target_nation))
                    clear_both_specialists(nation=_nation, target_nation=_target_nation)
                else:
                    exchange_cards(nation=_nation, target_nation=_target_nation)
                break
            else:
                clear_suggestion_and_response(nation=_nation, target_nation=_target_nation)
                _negotiation_token -= 1


def hire_mercenary(nation: Nation):
    move_cards(from_field=NATURE.deck, cards=[NATURE.deck[0]], to_field=nation.drafted_people)
    nation.hired_mercenary_token += 1


def draft_card(nation: Nation, player: Player) -> None:
    move_cards(from_field=nation.people,
               cards=player.select_cards(cards=nation.people, quantity=1), to_field=nation.drafted_people) \
        if nation.people else hire_mercenary(nation=nation)


def draft_cards(nation: Nation, player: Player,
                target_nation: Nation, target_player: Player) -> None:
    [draft_card(nation=_nation, player=_player) for _nation, _player
     in zip([nation, target_nation] * 3, [player, target_player] * 3)]


def call_guard(nation: Nation, guards: list[Card]) -> None:
    move_cards(from_field=nation.opened_cabinet, cards=guards, to_field=nation.drafted_people)


def guard_activated(nation: Nation, player: Player) -> None:
    activate_specialists(special_letters=NUMBER_LETTERS, nation=nation, player=player)
    call_guard(nation=nation, guards=nation.opened_cabinet)


def winter() -> None:
    for _nation in ALL_NATIONS:
        _player = search_player_by_nation(nation=_nation)

        _target_nation = _player.aim_a_nation()
        _target_player = search_player_by_nation(nation=_target_nation)

        # _engaged_nations: list[Nation] = [_nation, _target_nation]
        # _engaged_players: list[Player] = [_player, _target_player]

        draft_cards(nation=_nation, player=_player,
                    target_nation=_target_nation, target_player=_target_player)

        # shadow cabinet의 letter in number_letters 인 카드를 activate해 1장까지 추가로 draft 가능
        # if activate specialist(special letters=num_letters): draft spsecialist

        # battlefield의 camp로 drafted people을 이동해 감춤
        # move cards(from nation.drafted people to battlefield.camp) for each nation

        # offensive nation부터 stragety 설정
        # move


genesis()
spring()
summer()
fall()
winter()
