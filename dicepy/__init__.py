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
                raise Exception('what the heck did you do?')
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
            

def perform_roll(dice: int, sides: int, keep_type: OptionalType[KeepType] = None, keep_amount: int = 1) -> int:
    if dice > 100 or sides > 100 or keep_amount > dice:
        raise Exception('you wot mate?')
    rolls = [randint(1, sides) for _ in range(dice)]

    if keep_type == None:
        return sum(rolls)
    elif keep_type == KeepType.highest or keep_type == KeepType.keep:
        return sum(sorted(rolls)[-keep_amount:])
    else: # KeepType.lowest
        return sum(sorted(rolls)[:keep_amount])

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
