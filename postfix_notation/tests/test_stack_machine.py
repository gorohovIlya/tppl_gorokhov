import pytest

from src import InvalidElementError, StackMachine
from src.exception import InvalidExpressionError


class TestStackMachine:
    def test_expression_setter(self):
        passed = True
        try:
            expr = "3 5 + 3 4 -"
            machine = StackMachine()
            machine.expression = expr
        except Exception as e:
            passed = False

        assert passed

    def test_expression_without_spaces(self):
        expr = "304~2~"
        machine = StackMachine()
        with pytest.raises(InvalidElementError):
            machine.expression = expr

    def test_expression_with_invalid_separator(self):
        expr = "3.27|0.27|4.27|+|2.27|+"
        machine = StackMachine()
        with pytest.raises(ValueError):
            machine.expression = expr

    def test_unbalanced_expression(self):
        expr = "2 ~ 2 2 +"
        machine = StackMachine()
        with pytest.raises(InvalidExpressionError):
            machine.expression = expr
            machine.calculate()

    def test_empty_expression(self):
        expr = ""
        machine = StackMachine()
        with pytest.raises(InvalidExpressionError):
            machine.expression = expr

    def test_plus(self):
        expr = "2 3 +"
        machine = StackMachine()
        machine.expression = expr
        machine.calculate()
        assert machine.result == 5

    def test_mul(self):
        expr = "2 3 *"
        machine = StackMachine()
        machine.expression = expr
        machine.calculate()
        assert machine.result == 6

    def test_div(self):
        expr = "4 2 /"
        machine = StackMachine()
        machine.expression = expr
        machine.calculate()
        assert int(machine.result) == 2

    def test_sub(self):
        expr = "3 2 -"
        machine = StackMachine()
        machine.expression = expr
        machine.calculate()
        assert machine.result == 1

    def test_tilda_with_zero(self):
        expr = "0 3 ~"
        machine = StackMachine()
        machine.expression = expr
        machine.calculate()
        assert machine.result == 9

    def test_tilda_without_zero(self):
        expr = "3 4 ~"
        machine = StackMachine()
        machine.expression = expr
        machine.calculate()
        assert machine.result == 1
