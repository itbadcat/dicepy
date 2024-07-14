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

        # Just for fun if this ever gets min'd to 3.10
        #match keep_type:
        #    case None: # KeepType.all?
        #        self.value = sum(self.dice)
        #    case KeepType.keep | KeepType.highest:
        #        self.value = sum(sorted(self.dice)[-self.keep_amount:])
        #    case KeepType.lowest:
        #        self.value=sum(sorted(self.dice)[:self.keep_amount])

    def __repr__(self):
        return f"Roll(keep_type='{self.keep_type}' keep_amount='{self.keep_amount}' dice='{self.dice}' value='{self.value}')"

def roll_math(tokens):
    # '2d20k + (4d6kl2+6)*2' => [13, '+', [[2, '+', 6], '*', 2]]
    if isinstance(tokens, int): # it's just a single int
        return tokens
    total = None
    next_operation = None
    for token in tokens:
        if isinstance(token, int):
            if total is None:
                total = token
                continue

            if next_operation == MathType.multiply:
                total *= token
            elif next_operation == MathType.divide:
                total //= token
            elif next_operation == MathType.add:
                total += token
            elif next_operation == MathType.subtract:
                total -= token
            else:
                raise Exception('What the heck did you even DO?')
        elif isinstance(token, MathType):
            next_operation = token
        elif isinstance(token, ParseResults): # essentially a nested list
            result = roll_math(token[0])
            if total is None:
                total = result
                continue

            if next_operation == MathType.multiply:
                total *= token
            elif next_operation == MathType.divide:
                total //= token
            elif next_operation == MathType.add:
                total += token
            elif next_operation == MathType.subtract:
                total -= token
            else:
                raise Exception('what the heck did you do?')

    return total
            

def perform_roll(dice_count: int, sides: int, keep_type: OptionalType[KeepType] = None, keep_amount: int = 1) -> Roll:
    if dice_count > 100 or sides > 100 or keep_amount > dice_count:
        raise Exception('you wot mate?')
    return Roll(sides, dice_count, keep_type, keep_amount)


muldiv = oneOf(['*', '/'])('muldiv').setParseAction(lambda token: MathType(token[0]))
addsub = oneOf(['+', '-'])('addsub').setParseAction(lambda token: MathType(token[0]))

dice = Optional(pyparsing_common.integer, default=1)('dice')
d = Suppress('d')
sides = pyparsing_common.integer('sides')

keep_type = oneOf([e.value for e in KeepType])('keep_type').setParseAction(lambda token: KeepType(token[0]))
amount = Optional(pyparsing_common.integer, default=1)('keep_amount')
keep = Optional(keep_type + amount)

single_roll = (dice + d + sides + keep).setParseAction(lambda tokens: perform_roll(*tokens))
roll = infixNotation(
    single_roll | pyparsing_common.integer,
    [
        (muldiv, 2, opAssoc.LEFT),
        (addsub, 2, opAssoc.LEFT),
    ]
).setParseAction(lambda tokens: roll_math(tokens[0]))
