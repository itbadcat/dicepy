from enum import Enum
from random import randint
from typing import Optional as OptionalType
from pyparsing import Suppress, Optional, pyparsing_common, oneOf, infixNotation, opAssoc, ParseResults

class KeepType(Enum):
    keep = 'k'
    highest = 'kh'
    lowest = 'kl'

class MathType(Enum):
    multiply = '*'
    divide = '/'
    add = '+'
    subtract = '-'

class Roll:
    keep_type = None
    keep_amount = 1
    dice = None
    value = None

    def __init__(self, sides: int, dice_count: int, keep_type: OptionalType[KeepType] = None, keep_amount: int = 1):
        self.dice = [randint(1, sides) for _ in range(dice_count)]
        self.keep_type = keep_type
        self.keep_amount = keep_amount
        if keep_type == None:
            self.value = sum(self.dice)
        # 3d6k2 and 3d6kh2
        elif keep_type == KeepType.highest or keep_type == KeepType.keep:
            self.value = sum(sorted(self.dice)[-self.keep_amount:])
        else: # KeepType.lowest
            self.value = sum(sorted(self.dice)[:self.keep_amount])

    def __repr__(self):
        amount = ' '
        if self.keep_type:
            amount = f" keep_amount='{self.keep_amount}' "
        return f"Roll(keep_type='{self.keep_type}'{amount}dice='{self.dice}' value='{self.value}')"
