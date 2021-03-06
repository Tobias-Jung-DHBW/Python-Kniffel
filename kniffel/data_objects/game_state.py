"""
The game_state module contains all classes for holding and storing a games current state
"""
from json import JSONEncoder
from typing import List, Dict

from kniffel.data_objects.game_kind import EnumGameKind
from kniffel.data_objects.point import Point, PointEncoder
from kniffel.data_objects.dice import Dice, DiceEncoder


class GameState:
    """
    The GameState class is supposed to be the main container class for a games state,
    it should withold all information to restore a canceled game
    """

    @staticmethod
    def from_json(data):
        """
        Marshals a GameState object from dict
        """
        game_state = GameState()
        if not isinstance(data, Dict):
            return game_state
        if "game_kind" in data:
            game_state.game_kind = EnumGameKind(data["game_kind"])
        if "active_player" in data:
            game_state.active_player = data["active_player"]
        if "roll_count" in data:
            game_state.roll_count = data["roll_count"]
        if "dice" in data:
            dice = []
            for die in data["dice"]:
                dice.append(Dice.from_json(die))
            game_state.dice = dice
        if "points" in data:
            points_decoded = []
            for column_encoded in data["points"]:
                column_decoded = []
                for point in column_encoded:
                    column_decoded.append(Point.from_json(point))
                points_decoded.append(column_decoded)
            game_state.points = points_decoded
        return game_state

    def __init__(self):
        self.active_player = 0
        self.roll_count = 0
        self.game_kind = EnumGameKind.GAME_AGAINST_HUMAN
        self.__points = None
        self.__dice = None

    @property
    def points(self) -> List[List[Point]]:
        """
        A getter for the combinations within a GameState
        """
        return self.__points

    @points.setter
    def points(self, value: List[List[Point]]):
        self.__points = value

    @property
    def dice(self) -> List[Dice]:
        """
        A getter for the dice within a GameState
        """
        return self.__dice

    @dice.setter
    def dice(self, value: List[Dice]):
        self.__dice = value

    def __eq__(self, other) -> bool:
        """
        checks if two GameState objects are equal
        """
        if not isinstance(other, GameState):
            return False
        if self.active_player != other.active_player or self.roll_count != other.roll_count:
            return False
        if self.game_kind != other.game_kind and self.game_kind.value != other.game_kind.value:
            return False

        if not self.dice_equal(other):
            return False

        return self.points_equal(other)

    def dice_equal(self, other) -> bool:
        """
        checks if the passed object has the same dices
        """
        if len(self.dice) != len(other.dice):
            return False
        iteration = 0
        for dice in self.dice:
            if dice != other.dice[iteration]:
                return False
            iteration += 1
        return True

    def points_equal(self, other) -> bool:
        """
        checks if the passed object has the same point entries
        """
        if len(self.points) != len(other.points):
            return False
        col_nr = 0
        for column in self.points:
            if len(column) != len(other.points[col_nr]):
                return False
            row_nr = 0
            for point in column:
                if point != other.points[col_nr][row_nr]:
                    return False
                row_nr += 1
            col_nr += 1
        return True


class GameStateEncoder(JSONEncoder):
    """
    GameStateEncoder is used for encoding a game_state to json
    """

    def default(self, o):
        """
        used for decoding GameState to json
        """
        if not isinstance(o, GameState):
            return None

        points_encoded = []
        for column in o.points:
            col_encoded = []
            for point in column:
                col_encoded.append(PointEncoder().default(point))
            points_encoded.append(col_encoded)
        dice_encoded = []
        for die in o.dice:
            dice_encoded.append(DiceEncoder().default(die))

        return {
            "active_player": o.active_player,
            "roll_count": o.roll_count,
            "game_kind": o.game_kind.value,
            "points": points_encoded,
            "dice": dice_encoded
        }
