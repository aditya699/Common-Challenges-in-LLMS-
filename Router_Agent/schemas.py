from pydantic import BaseModel

class UserQuery(BaseModel):
    """
    Route the user query to the right tool
    """
    output_type: int
