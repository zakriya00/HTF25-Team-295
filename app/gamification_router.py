# app/gamification_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.gamification import GamificationService

router = APIRouter(prefix="/gamification", tags=["Gamification"])

@router.get("/leaderboard/{room_id}")
def get_leaderboard(room_id: str, db: Session = Depends(get_db)):
    """Get leaderboard for a room."""
    try:
        room = db.query(models.Room).filter(models.Room.name == room_id).first()
        if not room:
            return {"leaderboard": []}
        
        gamification = GamificationService(db)
        leaderboard = gamification.get_leaderboard(room.id, limit=20)
        return {"leaderboard": leaderboard}
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        return {"leaderboard": []}

@router.get("/user-stats/{username}")
def get_user_stats(username: str, db: Session = Depends(get_db)):
    """Get user statistics and badges."""
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        gamification = GamificationService(db)
        stats = gamification.get_user_stats(user.id)
        return stats
    except Exception as e:
        print(f"Error fetching user stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user stats")

@router.get("/badges/{username}")
def get_user_badges(username: str, db: Session = Depends(get_db)):
    """Get user badges."""
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        gamification = GamificationService(db)
        badges = gamification.get_user_badges(user.id)
        return {"badges": badges}
    except Exception as e:
        print(f"Error fetching badges: {e}")
        return {"badges": []}

@router.get("/challenges/{room_id}")
def get_active_challenges(room_id: str, db: Session = Depends(get_db)):
    """Get active challenges for a room."""
    try:
        room = db.query(models.Room).filter(models.Room.name == room_id).first()
        if not room:
            return {"challenges": []}
        
        gamification = GamificationService(db)
        challenges = gamification.get_active_challenges(room.id)
        return {"challenges": challenges}
    except Exception as e:
        print(f"Error fetching challenges: {e}")
        return {"challenges": []}

@router.post("/challenges/{room_id}/create")
def create_daily_challenge(
    room_id: str,
    title: str,
    description: str,
    challenge_type: str,
    points_reward: int = 10,
    db: Session = Depends(get_db)
):
    """Create a daily challenge for a room (admin only)."""
    try:
        room = db.query(models.Room).filter(models.Room.name == room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        gamification = GamificationService(db)
        challenge = gamification.create_daily_challenge(
            room.id, title, description, challenge_type, points_reward
        )
        
        return {
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "challenge_type": challenge.challenge_type,
            "points_reward": challenge.points_reward,
            "expires_at": challenge.expires_at.isoformat() if challenge.expires_at else None
        }
    except Exception as e:
        print(f"Error creating challenge: {e}")
        raise HTTPException(status_code=500, detail="Error creating challenge")

@router.post("/challenges/submit")
def submit_challenge(
    username: str,
    challenge_id: int,
    submission_data: str,
    is_correct: bool = False,
    db: Session = Depends(get_db)
):
    """Submit a challenge response."""
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        gamification = GamificationService(db)
        submission = gamification.submit_challenge(
            user.id, challenge_id, submission_data, is_correct
        )
        
        return {
            "id": submission.id,
            "points_earned": submission.points_earned,
            "is_correct": bool(submission.is_correct),
            "submitted_at": submission.submitted_at.isoformat()
        }
    except Exception as e:
        print(f"Error submitting challenge: {e}")
        raise HTTPException(status_code=500, detail="Error submitting challenge")
