from pydantic import BaseModel, Field, field_validator

class RecipeQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Search query must not be empty.")

    @field_validator("query", mode="before")
    def validate_query(value: str) -> str:
        if not value.strip():
            raise ValueError("Search query must not be empty or whitespace.")
        return value
