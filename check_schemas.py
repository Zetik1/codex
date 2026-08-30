from app.schemas.article_type import validate_fields_schema

GOOD = [
    {"key": "level", "label": "Уровень", "type": "select", "options": ["низшая", "высшая"]},
    {"key": "power", "label": "Сила", "type": "number"},
    {"key": "is_dead", "label": "Погибла", "type": "bool"},
]

BAD = {
    "ключ кириллицей": [{"key": "Сила", "label": "Сила", "type": "number"}],
    "тип ref": [{"key": "owner", "label": "Владелец", "type": "ref"}],
    "дубль ключа": [
        {"key": "power", "label": "Сила", "type": "number"},
        {"key": "power", "label": "Мощь", "type": "number"},
    ],
    "select без options": [{"key": "level", "label": "Уровень", "type": "select"}],
    "лишний ключ": [{"key": "power", "label": "Сила", "type": "number", "hack": 1}],
    "ключ в 41 символ": [{"key": "a" * 41, "label": "Длинный", "type": "number"}],
    "51 поле": [{"key": f"f{i}", "label": "Поле", "type": "number"} for i in range(51)],
    "не список": {"key": "power", "label": "Сила", "type": "number"},
    "пустой label": [{"key": "power", "label": "", "type": "number"}],
}

print("--- хорошая схема ---")
for field in validate_fields_schema(GOOD):
    print(f"принято: {field.key:10} | {field.type}")

print("\n--- плохие схемы ---")
for title, schema in BAD.items():
    try:
        validate_fields_schema(schema)
    except ValueError as error:
        message = " ".join(str(error).split())
        print(f"  отклонено: {title:18} -> {message[:110]}")
    else:
        print(f"  !!! ПРОПУЩЕНО: {title}")