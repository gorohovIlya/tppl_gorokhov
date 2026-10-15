class InvalidElementError(ValueError):
    """Исключение для некорректного элемента в выражении"""

    pass


class InvalidExpressionError(ValueError):
    """Исключение для некорректного выражения (Пустое / Несбалансированное)"""

    pass
