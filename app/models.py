from pydantic import BaseModel, Field, field_validator


class RecipeQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Search query must not be empty.")

    @field_validator("query", mode="before")
    def validate_query(value: str) -> str:
        """
        Validates the 'query' field to ensure it is not empty or consists only of whitespace.

        :param value: The query string provided by the user.
        :return: The trimmed query string if valid.
        :raises ValueError: If the query is empty or contains only whitespace.
        """
        if not value.strip():
            raise ValueError("Search query must not be empty or whitespace.")
        return value
