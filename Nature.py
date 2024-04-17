from Attributes import Suit, NONE_SUIT
from Cards import generate_deck
from Field import Field


class Nature:
    suit: Suit

    deck: Field
    banned: Field

    def __init__(self):
        self.suit = NONE_SUIT

        self.deck = Field(suit=self.suit, cards=generate_deck(), is_visible=False)
        self.banned = Field(suit=self.suit, cards=[], is_visible=True)


NATURE: Nature = Nature()
