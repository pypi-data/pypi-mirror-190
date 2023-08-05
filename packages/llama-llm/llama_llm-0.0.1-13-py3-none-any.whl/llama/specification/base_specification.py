from pydantic import BaseModel, validator
from pydantic.fields import ModelField

class BaseSpecification(BaseModel):
    @validator('*', pre=True, always=True)
    def has_description(cls, v, field: ModelField):
        if field.field_info.description is None:
            raise ValueError(
                f"Description missing for field {field.name} in Spec {cls.__name__}. Import Context from llama and use it to describe the field with natural language."
            )
        return v
