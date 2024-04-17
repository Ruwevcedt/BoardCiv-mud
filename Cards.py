from Attributes import Suit, Letter, REGULAR_SUITS, REGULAR_LETTERS, NONE_SUIT, ZOKER


class Card:
    suit: Suit
    letter: Letter

    def __init__(self, suit: Suit, letter: Letter):
        self.suit = suit
        self.letter = letter

    def __str__(self, visible: bool = False) -> str:
        return f"{self.suit} {self.letter}" if visible else "<Card>"


def generate_deck() -> list[Card]:
    return ([Card(NONE_SUIT, ZOKER)] * 2 +
            [Card(suit=_suit, letter=_letter) for _suit in REGULAR_SUITS
             for _letter in REGULAR_LETTERS])
