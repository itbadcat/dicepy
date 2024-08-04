from __future__ import annotations
from enum import Enum
from random import randint
from typing import Union, List, Optional as OptionalType
from pyparsing import Suppress, Optional, pyparsing_common, oneOf, infixNotation, opAssoc, ParseResults
from functools import cached_property
from numbers import Real

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

    def __init__(self, sides: int, dice_count: int, initial_rolls: OptionalType[List[int]] = None, keep_type: OptionalType[KeepType] = None, keep_amount: int = 1):
        if initial_rolls is None:
            self.dice = [randint(1, sides) for _ in range(dice_count)]
        else:
            self.dice = sorted(initial_rolls)
        self.keep_type = keep_type
        self.keep_amount = keep_amount

    def __repr__(self):
        amount = ' '
        if self.keep_type:
            amount = f" keep_amount='{self.keep_amount}' "
        return f"Roll(keep_type='{self.keep_type}'{amount}dice='{self.dice}' value='{self.value}')"

    @cached_property
    def value(self):
        if self.keep_type == None:
            return sum(self.dice)
        elif self.keep_type == KeepType.highest or self.keep_type == KeepType.keep:
            return sum(sorted(self.dice)[-self.keep_amount:])
        else: #KeepType.lowest
            return sum(sorted(self.dice)[:self.keep_amount])

    def __add__(self, other: Union[Real, Roll]) -> Real:
        if isinstance(other, Real):
            return self.value + other
        elif isinstance(other, Roll):
            return self.value + other.value
        else:
            raise Exception("Bad addition operand type")

    def __sub__(self, other: Union[Real, Roll]) -> Real:
        if isinstance(other, Real):
            return self.value - other
        elif isinstance(other, Roll):
            return self.value - other.value
        else:
            raise Exception("Bad subtraction operand type")

    def __mul__(self, other: Union[Real, Roll]) -> Real:
        if isinstance(other, Real):
            return self.value * other
        elif isinstance(other, Roll):
            return self.value * other.value
        else:
            raise Exception("Bad multiplication operand type")

    def __truediv__(self, other: Union[Real, Roll]) -> Real:
        if isinstance(other, Real):
            return self.value / other
        elif isinstance(other, Roll):
            return self.value / other.value
        else:
            raise Exception("Bad true division operand type")

    def __floordiv__(self, other: Union[Real, Roll]) -> Real:
        if isinstance(other, Real):
            return self.value // other
        elif isinstance(other, Roll):
            return self.value // other.value
        else:
            raise Exception("Bad floor division operand type")
