from random import sample, random

from Attributes import Suit, REGULAR_SUITS
from Cards import Card
from Nations import Nation, ALL_NATIONS


class Player:
    suit: Suit

    def __init__(self, suit: Suit):
        self.suit = suit

    def _select_from_catalogue(self, catalogue: list, quantity: int) -> list:
        _possible_max_quantity = len(catalogue)
        return sample(catalogue, quantity if _possible_max_quantity > quantity else _possible_max_quantity)

    def make_a_decision(self) -> bool:
        return random() > 0.5

    def aim_a_nation(self) -> Nation:
        return self._select_from_catalogue(catalogue=[_nation for _nation in ALL_NATIONS if _nation.suit != self.suit],
                                           quantity=1)[0]

    def aim_a_nation_for_a_diplomacy(self) -> Nation:
        return self._select_from_catalogue(catalogue=[_nation for _nation in ALL_NATIONS
                                                      if (_nation.suit != self.suit) & bool(_nation.people)],
                                           quantity=1)[0]

    def select_quantity(self, minimum: int, maximum: int, quantity: int) -> list[int]:
        return sample(list(range(minimum, maximum + 1)), quantity)

    def select_cards(self, cards: list[Card], quantity: int) -> list[Card]:
        return self._select_from_catalogue(catalogue=cards, quantity=quantity)


class Players(list[Player]):
    def __init__(self, players: list[Player]):
        super().__init__(players)

    def search_players(self, suits: list[Suit]) -> list[Player]:
        return [_player for _player in self if _player.suit in suits]


ALL_PLAYERS: Players = Players([Player(suit=_suit) for _suit in REGULAR_SUITS])
