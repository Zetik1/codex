import pytest

from app.schemas.article_type import validate_fields_schema

GOOD = [
    {"key": "level", "label": "Уровень", "type": "select", "options": ["низшая", "высшая"]},
    {"key": "power", "label": "Сила", "type": "number"},
    {"key": "is_dead", "label": "Погибла", "type": "bool"},
]

BAD = {
    "cyrillic_key": [{"key": "Сила", "label": "Сила", "type": "number"}],
    "unknown_type_ref": [{"key": "owner", "label": "Владелец", "type": "ref"}],
    "duplicate_key": [
        {"key": "power", "label": "Сила", "type": "number"},
        {"key": "power", "label": "Мощь", "type": "number"},
    ],
    "select_without_options": [{"key": "level", "label": "Уровень", "type": "select"}],
    "options_without_select": [
        {"key": "power", "label": "Сила", "type": "number", "options": ["a"]}
    ],
    "extra_key": [{"key": "power", "label": "Сила", "type": "number", "hack": 1}],
    "key_too_long": [{"key": "a" * 41, "label": "Длинный", "type": "number"}],
    "empty_label": [{"key": "power", "label": "", "type": "number"}],
    "too_many_fields": [{"key": f"f{i}", "label": "Поле", "type": "number"} for i in range(51)],
    "not_a_list": {"key": "power", "label": "Сила", "type": "number"},
}

def test_good_schema_accepted():
    fields = validate_fields_schema(GOOD)
    assert [field.key for field in fields] == ["level", "power", "is_dead"]
    assert fields[1].options is None


@pytest.mark.parametrize("schema", BAD.values(), ids=BAD.keys())
def test_bad_schema_rejected(schema):
    with pytest.raises(ValueError):
        validate_fields_schema(schema)


def test_bad_schema_rejected_by_model():
    from app.models import ArticleType 

    with pytest.raises(ValueError):
        ArticleType(
            library_id=1,
            slug="broken",
            name="Сломанный",
            fields_schema=[
                {"key": "power", "label": "Сила", "type": "number"},
                {"key": "power", "label": "Мощь", "type": "number"},
            ],
        )