from pydantic import BaseModel


class Game(BaseModel):
    app_id: int
    name: int