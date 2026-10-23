import re
from collections import deque
from types import MethodType

from src.exception import InvalidElementError, InvalidExpressionError


class StackMachine:
    """
    Класс, реализующий Стек-машину.
    Поля:
        __body: deque[float,] - Тело стека. Использует deque из библиотеки collections
        __operations: dict[str, MethodType] - Словарь методов, определённых в стек-машине.
        __result: float - Результат вычислений
        __expression: str - Выражение, значение которого необходимо вычислить
        __traceback: str - Последовательность шагов вычисления. Хранит информацию вида "Шаг n. Cтек: ..."
    """

    def __init__(self):
        self.__body: deque[float,] = deque()
        self.__operations: dict[str, MethodType] = {
            "+": self.__plus,
            "-": self.__sub,
            "/": self.__div,
            "*": self.__mul,
            "~": self.__tilda,
            "!": self.__power
        }
        self.__result = 0
        self.__expression = ""
        self.__traceback = ""

    def __validate_expression(self, expr: str):
        """Валидация выражения, перед его записью в поле __expression для последующей работы"""
        if len(expr) == 0:
            raise InvalidExpressionError("Пустое выражение!")
        splitted_expression: list[str,] = expr.split(" ")
        pattern = r"\d+([.]\d+)?"
        for el in splitted_expression:
            if not re.fullmatch(pattern, el) and el not in self.__operations:
                raise InvalidElementError(f"Некорректный элемент в выражении: `{el}`")

    @property
    def body(self) -> deque[float,]:
        """Геттер. Возвращает выражение"""
        return self.__body

    @property
    def operations(self) -> dict[str, MethodType]:
        """Геттер. Возвращает операции"""
        return self.__operations

    @property
    def expression(self) -> str:
        """Геттер. Возвращает выражение"""
        return self.__expression

    @property
    def traceback(self) -> str:
        """Геттер. Возвращает последовательность состояний стека на разных шагах"""
        return self.__traceback

    @property
    def result(self) -> float:
        """Геттер. Возвращает результат работы стек-машины"""
        return self.__result

    @expression.setter
    def expression(self, expr: str):
        """Сеттер. Задаёт выражение"""
        self.__validate_expression(expr)
        self.__expression = expr

    def __plus(self, op1: float, op2: float) -> None:
        """Операция сложения"""
        res = op1 + op2
        self.__body.append(res)

    def __mul(self, op1: float, op2: float) -> None:
        """Операция умножения"""
        res = op1 * op2
        self.__body.append(res)

    def __div(self, op1: float, op2: float) -> None:
        """Операция деления"""
        res = op1 / op2
        self.__body.append(res)

    def __sub(self, op1: float, op2: float) -> None:
        """Операция вычитания"""
        res = op1 - op2
        self.__body.append(res)

    def __tilda(self, op1: float, op2: float) -> None:
        """Операция ~"""
        if op1 != 0 and op2 != 0:
            res = abs(op1 - op2)
            self.__body.append(res)
        else:
            res = op1 + op2
            while len(self.body) > 0:
                res += self.__body.pop()
            self.__body.append(res**2)
    
    def __power(self, op1: float, op2: float) -> None:
        """Операция !"""
        res = op1 ** op2
        self.__body.append(res)

    def calculate(self) -> None:
        """Вычисление результата"""
        operations = self.__operations.keys()
        for idx, el in enumerate(self.expression.split()):
            if el in operations:
                if len(self.__body) < 2:
                    raise InvalidExpressionError(
                        f"Оператору `{el}` не хватает операндов"
                    )
                op2 = self.__body.pop()
                op1 = self.__body.pop()
                self.__operations[el](op1, op2)
            else:
                self.__body.append(float(el))
            self.__traceback += f"Шаг: {idx + 1}. Стек: {list(self.__body)}\n"
        if len(self.__body) != 1:
            raise InvalidExpressionError(
                f"После вычислений в стеке {len(self.__body)} элементов, ожидался 1"
            )
        self.__result = self.__body[-1]
