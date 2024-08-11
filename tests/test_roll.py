from dicepy import roll

from unittest import TestCase
import random

class TestRoll(TestCase):
    def setUp(self):
        random.seed(242)

    def test_single_roll_in_roll(self):
        _simple_roll = roll.parseString('5d6kl2')
