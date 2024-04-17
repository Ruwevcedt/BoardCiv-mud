from Attributes import Suit, REGULAR_SUITS, NONE_SUIT
from Field import Field


class Nation:
    suit: Suit

    throne: Field
    shadow_cabinet: Field
    opened_cabinet: Field

    people: Field
    drafted_people: Field

    def __init__(self, suit: Suit):
        self.suit = suit

        self.throne = Field(suit=self.suit, cards=[], is_visible=True)
        self.shadow_cabinet = Field(suit=self.suit, cards=[], is_visible=False)
        self.opened_cabinet = Field(suit=self.suit, cards=[], is_visible=True)

        self.people = Field(suit=self.suit, cards=[], is_visible=False)
        self.drafted_people = Field(suit=self.suit, cards=[], is_visible=True)

    def check_is_playable(self) -> bool:
        return True if len(self.people.search_cards(suits=[NONE_SUIT, self.suit])) > 1 else False


class Nations(list[Nation]):
    def __init__(self, nations: list[Nation]):
        super().__init__(nations)

    def search_nations(self, suits: list[Suit]) -> list[Nation]:
        return [_nation for _nation in self if _nation.suit in suits]


ALL_NATIONS: Nations = Nations([Nation(suit=_suit) for _suit in REGULAR_SUITS])
