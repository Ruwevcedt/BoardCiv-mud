class Suit(str):
    code: int

    def __new__(cls, suit: str, code: int):
        _object = str.__new__(cls, suit)
        _object.code = code
        return _object

    def __int__(self):
        return self.code


class Letter(str):
    rank: int

    def __new__(cls, letter: str, rank: int):
        _object = str.__new__(cls, letter)
        _object.rank = rank
        return _object

    def __int__(self):
        return self.rank


class AllSuits(list):
    def __init__(self):
        super().__init__([Suit(suit=_suit, code=_code) for _code, _suit in
                          enumerate(['none', 'spade', 'heart', 'diamond', 'club'])])


class AllLetters(list):
    def __init__(self):
        super().__init__([Letter(letter=_letter, rank=_rank) for _rank, _letter in
                          enumerate(['Z', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])])


ALL_SUITS: list[Suit] = AllSuits()
ALL_LETTERS: list[Letter] = AllLetters()

REGULAR_SUITS: list[Suit] = ALL_SUITS[1:]
REGULAR_LETTERS: list[Letter] = ALL_LETTERS[1:]
NUMBER_LETTERS: list[Letter] = ALL_LETTERS[2:11]

NONE_SUIT: Suit = ALL_SUITS[0]
ZOKER: Letter = ALL_LETTERS[0]
ACE: Letter = ALL_LETTERS[1]
TEN: Letter = ALL_LETTERS[10]
JACK: Letter = ALL_LETTERS[11]
QUEEN: Letter = ALL_LETTERS[12]
KING: Letter = ALL_LETTERS[13]
