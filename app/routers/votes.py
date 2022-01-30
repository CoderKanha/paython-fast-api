from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import VotesModel, Posts
from oauth2 import get_current_user
from schema import UserBaseSchema, VoteBaseSchema
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Votes']
)


@router.get('')
def get_votes(db: Session = Depends(get_db), get_current_user: UserBaseSchema = Depends(get_current_user)):
    user_id = get_current_user.id
    vote_query = db.query(
        VotesModel
    ).filter(
        VotesModel.user_id == user_id
    ).all()
    return vote_query


@router.post('')
def add_vote(payload: VoteBaseSchema, db: Session = Depends(get_db), get_current_user: UserBaseSchema = Depends(get_current_user)):
    user_id = get_current_user.id

    post = db.query(Posts).filter(Posts.id == payload.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Request post doesn\'t exist')

    vote_query = db.query(
        VotesModel
    ).filter(
        VotesModel.user_id == user_id,
        VotesModel.post_id == payload.post_id
    )
    vote_result = vote_query.first()

    if payload.vote_dir == 1:
        if vote_result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='User already voted this post')
        else:
            new_vote = VotesModel(post_id=payload.post_id, user_id=user_id)
            db.add(new_vote)
            db.commit()
            return {"message": "Vote added successfully"}
    else:
        if not vote_result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='User not voted for this post')
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote removed successfully"}
