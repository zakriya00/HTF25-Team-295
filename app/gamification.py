# app/gamification.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from app import models

class GamificationService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_user_profile(self, user_id: int) -> models.UserProfile:
        """Get or create user profile for gamification."""
        profile = self.db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()
        if not profile:
            profile = models.UserProfile(user_id=user_id)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        return profile

    def update_study_streak(self, user_id: int) -> int:
        """Update study streak based on last active date."""
        profile = self.get_or_create_user_profile(user_id)
        today = datetime.utcnow().date()
        last_active = profile.last_active_date.date() if profile.last_active_date else None
        
        if last_active is None:
            # First time user
            profile.study_streak = 1
        elif last_active == today:
            # Already active today, no change
            pass
        elif last_active == today - timedelta(days=1):
            # Consecutive day
            profile.study_streak += 1
        else:
            # Streak broken
            profile.study_streak = 1
        
        profile.last_active_date = datetime.utcnow()
        self.db.commit()
        
        # Check for streak badges
        self.check_streak_badges(user_id, profile.study_streak)
        
        return profile.study_streak

    def award_message_points(self, user_id: int, message_content: str) -> int:
        """Award points for sending a message."""
        profile = self.get_or_create_user_profile(user_id)
        points = 1  # Base points for message
        
        # Bonus points for helpful content
        helpful_keywords = ['help', 'explain', 'solution', 'answer', 'understand', 'clarify']
        if any(keyword in message_content.lower() for keyword in helpful_keywords):
            points += 2
            profile.total_helpful_answers += 1
        
        profile.total_messages += 1
        profile.points += points
        self.update_level(profile)
        self.db.commit()
        
        # Check for message badges
        self.check_message_badges(user_id, profile.total_messages)
        
        return points

    def award_file_share_points(self, user_id: int) -> int:
        """Award points for sharing a file."""
        profile = self.get_or_create_user_profile(user_id)
        points = 3  # Points for file sharing
        
        profile.total_files_shared += 1
        profile.points += points
        self.update_level(profile)
        self.db.commit()
        
        # Check for file sharing badges
        self.check_file_badges(user_id, profile.total_files_shared)
        
        return points

    def award_mention_points(self, user_id: int) -> int:
        """Award points for being mentioned."""
        profile = self.get_or_create_user_profile(user_id)
        points = 2  # Points for being mentioned
        
        profile.total_mentions += 1
        profile.points += points
        self.update_level(profile)
        self.db.commit()
        
        return points

    def update_level(self, profile: models.UserProfile):
        """Update user level based on points."""
        # Level progression: 100, 250, 500, 1000, 2000, 5000, 10000, etc.
        level_thresholds = [100, 250, 500, 1000, 2000, 5000, 10000, 20000, 50000]
        new_level = 1
        
        for threshold in level_thresholds:
            if profile.points >= threshold:
                new_level += 1
            else:
                break
        
        if new_level > profile.level:
            profile.level = new_level
            # Check for level badges
            self.check_level_badges(profile.user_id, new_level)

    def check_streak_badges(self, user_id: int, streak: int):
        """Check and award streak-related badges."""
        streak_badges = [
            (3, "Early Bird", "🔥", "3-day study streak"),
            (7, "Week Warrior", "⚡", "7-day study streak"),
            (14, "Study Master", "🏆", "14-day study streak"),
            (30, "Study Legend", "👑", "30-day study streak"),
        ]
        
        for required_streak, name, icon, description in streak_badges:
            if streak >= required_streak:
                self.award_badge(user_id, name, icon, description)

    def check_message_badges(self, user_id: int, message_count: int):
        """Check and award message-related badges."""
        message_badges = [
            (10, "Chatter", "💬", "10 messages sent"),
            (50, "Social Butterfly", "🦋", "50 messages sent"),
            (100, "Conversation Starter", "🗣️", "100 messages sent"),
            (500, "Chat Master", "💭", "500 messages sent"),
        ]
        
        for required_messages, name, icon, description in message_badges:
            if message_count >= required_messages:
                self.award_badge(user_id, name, icon, description)

    def check_file_badges(self, user_id: int, file_count: int):
        """Check and award file-sharing badges."""
        file_badges = [
            (5, "Resource Sharer", "📁", "5 files shared"),
            (20, "Knowledge Keeper", "📚", "20 files shared"),
            (50, "Content Creator", "🎨", "50 files shared"),
        ]
        
        for required_files, name, icon, description in file_badges:
            if file_count >= required_files:
                self.award_badge(user_id, name, icon, description)

    def check_level_badges(self, user_id: int, level: int):
        """Check and award level-based badges."""
        level_badges = [
            (5, "Rising Star", "⭐", "Reached level 5"),
            (10, "Study Champion", "🥇", "Reached level 10"),
            (20, "Academic Hero", "🦸", "Reached level 20"),
        ]
        
        for required_level, name, icon, description in level_badges:
            if level >= required_level:
                self.award_badge(user_id, name, icon, description)

    def award_badge(self, user_id: int, name: str, icon: str, description: str):
        """Award a badge to a user if they don't already have it."""
        # Check if badge exists
        badge = self.db.query(models.Badge).filter(models.Badge.name == name).first()
        if not badge:
            badge = models.Badge(
                name=name,
                description=description,
                icon=icon,
                points_required=0
            )
            self.db.add(badge)
            self.db.commit()
            self.db.refresh(badge)
        
        # Check if user already has this badge
        existing_user_badge = self.db.query(models.UserBadge).filter(
            models.UserBadge.user_id == user_id,
            models.UserBadge.badge_id == badge.id
        ).first()
        
        if not existing_user_badge:
            user_badge = models.UserBadge(
                user_id=user_id,
                badge_id=badge.id,
                earned_at=datetime.utcnow()
            )
            self.db.add(user_badge)
            self.db.commit()
            return True
        
        return False

    def get_user_badges(self, user_id: int) -> List[Dict]:
        """Get all badges earned by a user."""
        user_badges = self.db.query(models.UserBadge, models.Badge).join(
            models.Badge, models.UserBadge.badge_id == models.Badge.id
        ).filter(models.UserBadge.user_id == user_id).all()
        
        return [
            {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon,
                "earned_at": user_badge.earned_at.isoformat()
            }
            for user_badge, badge in user_badges
        ]

    def get_leaderboard(self, room_id: Optional[int] = None, limit: int = 10) -> List[Dict]:
        """Get leaderboard for a room or globally."""
        query = self.db.query(models.UserProfile, models.User).join(
            models.User, models.UserProfile.user_id == models.User.id
        )
        
        if room_id:
            # Get users who have messages in this room
            room_user_ids = self.db.query(models.Message.user_id).filter(
                models.Message.room_id == room_id
            ).distinct().subquery()
            query = query.filter(models.UserProfile.user_id.in_(room_user_ids))
        
        leaderboard = query.order_by(
            models.UserProfile.points.desc(),
            models.UserProfile.study_streak.desc()
        ).limit(limit).all()
        
        return [
            {
                "username": user.username,
                "points": profile.points,
                "level": profile.level,
                "study_streak": profile.study_streak,
                "total_messages": profile.total_messages,
                "total_files_shared": profile.total_files_shared,
                "total_helpful_answers": profile.total_helpful_answers
            }
            for profile, user in leaderboard
        ]

    def get_user_stats(self, user_id: int) -> Dict:
        """Get comprehensive stats for a user."""
        profile = self.get_or_create_user_profile(user_id)
        badges = self.get_user_badges(user_id)
        
        return {
            "points": profile.points,
            "level": profile.level,
            "study_streak": profile.study_streak,
            "total_messages": profile.total_messages,
            "total_files_shared": profile.total_files_shared,
            "total_mentions": profile.total_mentions,
            "total_helpful_answers": profile.total_helpful_answers,
            "badges": badges,
            "last_active": profile.last_active_date.isoformat() if profile.last_active_date else None
        }

    def create_daily_challenge(self, room_id: int, title: str, description: str, 
                             challenge_type: str, points_reward: int = 10) -> models.DailyChallenge:
        """Create a daily challenge for a room."""
        challenge = models.DailyChallenge(
            room_id=room_id,
            title=title,
            description=description,
            challenge_type=challenge_type,
            points_reward=points_reward,
            expires_at=datetime.utcnow() + timedelta(days=1)
        )
        self.db.add(challenge)
        self.db.commit()
        self.db.refresh(challenge)
        return challenge

    def submit_challenge(self, user_id: int, challenge_id: int, submission_data: str, 
                        is_correct: bool = False) -> models.ChallengeSubmission:
        """Submit a challenge response."""
        challenge = self.db.query(models.DailyChallenge).filter(
            models.DailyChallenge.id == challenge_id
        ).first()
        
        if not challenge:
            raise ValueError("Challenge not found")
        
        points_earned = challenge.points_reward if is_correct else 0
        
        submission = models.ChallengeSubmission(
            user_id=user_id,
            challenge_id=challenge_id,
            submission_data=submission_data,
            is_correct=1 if is_correct else 0,
            points_earned=points_earned
        )
        
        self.db.add(submission)
        
        if is_correct:
            profile = self.get_or_create_user_profile(user_id)
            profile.points += points_earned
            self.update_level(profile)
        
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def get_active_challenges(self, room_id: int) -> List[Dict]:
        """Get active challenges for a room."""
        challenges = self.db.query(models.DailyChallenge).filter(
            models.DailyChallenge.room_id == room_id,
            models.DailyChallenge.is_active == 1,
            models.DailyChallenge.expires_at > datetime.utcnow()
        ).all()
        
        return [
            {
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "challenge_type": challenge.challenge_type,
                "points_reward": challenge.points_reward,
                "expires_at": challenge.expires_at.isoformat() if challenge.expires_at else None
            }
            for challenge in challenges
        ]
