# Postfix Notation Stack Machine
Python-реализация Стек-машины для вычисления выражения, записанного в постфиксной нотации

## Использование

```bash
python main.py <expression>
```

## Тестирование

```bash
python -m pytest
```

## Покрытие

```bash
pytest --cov=src tests/

# Или

PYTHONPATH=. pytest --cov=src tests/
```
