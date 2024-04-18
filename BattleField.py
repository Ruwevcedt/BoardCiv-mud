from Field import Field

from Nations import Nation
from Players import Player


class BattleField():
    offensive_nation: Nation
    defensive_nation: Nation
    engaged_nations: list[Nation]

    offensive_player: Player
    defensive_player: Player
    engaged_players: list[Player]

    offensive_camp: Field
    defensive_camp: Field

    offensive_divisions: list[Field]
    defensive_divisions: list[Field]

    offensive_battlefield: list[Field]
    defensive_battlefield: list[Field]

    def __init__(self, offensive_nation: Nation, defensive_nation: Nation,
                 offensive_player: Player, defensive_player: Player):
        self.offensive_nation = offensive_nation
        self.defensive_nation = defensive_nation
        self.engaged_nations = [self.offensive_nation, self.defensive_nation]

        self.offensive_player = offensive_player
        self.defensive_player = defensive_player
        self.engaged_players = [self.offensive_player, self.defensive_player]

        self.offensive_camp = Field(suit=offensive_nation.suit, cards=[], is_visible=False)
        self.defensive_camp = Field(suit=defensive_nation.suit, cards=[], is_visible=False)

        self.offensive_divisions = [
            Field(suit=offensive_nation.suit, cards=[], is_visible=False),
            Field(suit=offensive_nation.suit, cards=[], is_visible=False),
            Field(suit=offensive_nation.suit, cards=[], is_visible=False)
        ]
        self.defensive_divisions = [
            Field(suit=defensive_nation.suit, cards=[], is_visible=False),
            Field(suit=defensive_nation.suit, cards=[], is_visible=False),
            Field(suit=defensive_nation.suit, cards=[], is_visible=False)
        ]

        self.offensive_battlefield = [
            Field(suit=offensive_nation.suit, cards=[], is_visible=True),
            Field(suit=offensive_nation.suit, cards=[], is_visible=True),
            Field(suit=offensive_nation.suit, cards=[], is_visible=True)
        ]
        self.defensive_battlefield = [
            Field(suit=defensive_nation.suit, cards=[], is_visible=True),
            Field(suit=defensive_nation.suit, cards=[], is_visible=True),
            Field(suit=defensive_nation.suit, cards=[], is_visible=True)
        ]
