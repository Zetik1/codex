from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

MAX_FIELDS = 50
MAX_OPTIONS = 50
KEY_PATTERN = r"^[a-z][a-z0-9_]*$"


class FieldDef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(pattern=KEY_PATTERN, max_length=40)
    label: str = Field(min_length=1, max_length=100)
    type: Literal["string", "number", "bool", "date", "select"]
    options: list[str] | None = None

    @model_validator(mode="after")
    def check_options(self) -> "FieldDef":
        if self.type != "select":
            if self.options is not None:
                raise ValueError(f"options разрешен только при type='select', а здесь type='{self.type}'")
            return self
        
        if not self.options:
            raise ValueError("type='select' требует непустой список options")
        if len(self.options) > MAX_OPTIONS:
            raise ValueError(f"вариантов не больше {MAX_OPTIONS}, пришло {len(self.options)}")
        if len(set(self.options)) != len(self.options):
            raise ValueError("варианты в options повторяются")
        return self


FIELDS_ADAPTER = TypeAdapter(list[FieldDef])


def validate_fields_schema(raw: object) -> list[FieldDef]:
    if not isinstance(raw, list):
        raise ValueError("схема полей должна быть списком")
    if len(raw) > MAX_FIELDS:
        raise ValueError(f"полей не больше {MAX_FIELDS}, пришло {len(raw)}")

    fields = FIELDS_ADAPTER.validate_python(raw)

    seen: set[str] = set()
    for field in fields:
        if field.key in seen:
            raise ValueError(f"ключ '{field.key}' повторяется")
        seen.add(field.key)

    return fields