import sys

from src import StackMachine


def main() -> None:
    if len(sys.argv) >= 2:
        if sys.argv[-1] == "-h" or sys.argv[-1] == "--help":
            print("""
                Стек-машина для вычисления выражений в постфиксной нотации

                Доступные операции:
                    +: Сложение
                    -: Вычитание
                    *: Умножение
                    /: Деление
                    ~: Тильда

                Принцип работы оператора "Тильда":
                    Если оба операнда не равны 0: вычислить модуль разницы `|x - y|` и положить результат обратно в стек.
                    Если хотя бы один из операндов равен 0: вычисляет сумму всех значений в стеке, включая извлеченные операнды, возводит её в квадрат и кладет результат обратно в стек

                Использование:
                    python main.py "выражение"

                Поддерживается передача выражения без кавычек. Для операторов "*" и "~" требуется экранирование (\\* и \\~ соответственно)
                    python main.py 3.12 5.45 -
                    python main.py 3 3 * -> ОШИБКА! Правильно: python main.py 3 3 \\*
                """)
        else:
            expr = sys.argv[1:]
            processed_expr = expr[0] if len(expr) == 1 else " ".join(expr)
            machine = StackMachine()
            try:
                machine.expression = processed_expr
                machine.calculate()
                print(machine.traceback)
                print(f"{processed_expr} = {machine.result}")
            except Exception as e:
                print(f"Ошибка. {e}")

    elif len(sys.argv) == 1:
        print("Не передано выражение.\nЗапуск программы: python main.py 'выражение'")
    elif len(sys.argv) > 2:
        print(
            "Передано слишком много аргументов.\nЗапуск программы: python main.py 'выражение'"
        )


if __name__ == "__main__":
    main()
