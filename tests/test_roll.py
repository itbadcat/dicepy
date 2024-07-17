from dicepy import roll, KeepType, Roll

from unittest import TestCase
import random

class TestRoll(TestCase):
    def setUp(self):
        random.seed(242)

    def test_single_roll_in_roll(self):
        simple_roll = roll.parseString('5d6kl2')
