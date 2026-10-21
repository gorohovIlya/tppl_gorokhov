# Postfix Notation Stack Machine
Python-реализация Стек-машины для вычисления выражения, записанного в постфиксной нотации

## Установка
```bash
python install -e .
```

## Использование

```bash
python main.py "2 3 +"

# Результат
# Шаг: 1. Стек: [2.0]
# Шаг: 2. Стек: [2.0, 3.0]
# Шаг: 3. Стек: [5.0]

# Выражение = 5.0
```

## Тестирование

```bash
python -m pytest tests/ -v
```

## Покрытие

```bash
pytest --cov=src tests/

# Или

PYTHONPATH=. pytest --cov=src tests/
```
