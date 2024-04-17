from Attributes import Suit, ALL_SUITS, Letter, ALL_LETTERS
from Cards import Card


class Field(list[Card]):
    suit: Suit
    _is_visible: bool

    def __init__(self, suit: Suit, cards: list[Card], is_visible: bool):
        super().__init__(cards)
        self.suit = suit
        self._is_visible = is_visible

    def __str__(self, seen_by_suit: Suit = ALL_SUITS[0]) -> str:
        return str([_card.__str__(visible=True) for _card in self]) \
            if seen_by_suit == ALL_SUITS[0] or seen_by_suit == self.suit \
            else str([_card.__str__(visible=self._is_visible) for _card in self])

    def __bool__(self):
        return False if len(self) == 0 else True

    def search_cards(self, suits: list[Suit] = ALL_SUITS, letters: list[Letter] = ALL_LETTERS) -> list[Card]:
        return [_card for _card in self if (_card.suit in suits) & (_card.letter in letters)]


def move_cards(from_field: Field, cards: list[Card], to_field: Field) -> None:
    to_field += cards
    [from_field.remove(_card) for _card in cards]
