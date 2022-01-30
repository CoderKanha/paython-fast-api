from pydantic import BaseModel, conint


class VoteBaseSchema(BaseModel):
    post_id: int
    vote_dir: conint(ge=0,le=1)