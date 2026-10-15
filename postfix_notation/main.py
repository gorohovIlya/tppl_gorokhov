import sys

from src import StackMachine


def main() -> None:
    if len(sys.argv) == 2:
        expr = sys.argv[1]
        machine = StackMachine()
        try:
            machine.expression = expr
            machine.calculate()
            print(machine.traceback)
            print(f"Выражение = {machine.result}")
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
