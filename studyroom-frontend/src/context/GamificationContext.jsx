import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const GamificationContext = createContext();

export const useGamification = () => useContext(GamificationContext);

export const GamificationProvider = ({ children, username }) => {
  const [userStats, setUserStats] = useState(null);
  const [badges, setBadges] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchUserStats = async () => {
    if (!username) return;
    
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/gamification/user-stats/${username}`);
      setUserStats(response.data);
    } catch (error) {
      console.error("Error fetching user stats:", error);
      // Set default stats if API fails
      setUserStats({
        points: 0,
        level: 1,
        study_streak: 0,
        total_messages: 0,
        total_files_shared: 0,
        total_mentions: 0,
        total_helpful_answers: 0,
        badges: [],
        last_active: null
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchBadges = async () => {
    if (!username) return;
    
    try {
      const response = await axios.get(`http://localhost:8000/gamification/badges/${username}`);
      setBadges(response.data.badges || []);
    } catch (error) {
      console.error("Error fetching badges:", error);
      setBadges([]);
    }
  };

  const fetchLeaderboard = async (roomId) => {
    try {
      const response = await axios.get(`http://localhost:8000/gamification/leaderboard/${roomId}`);
      setLeaderboard(response.data.leaderboard || []);
    } catch (error) {
      console.error("Error fetching leaderboard:", error);
      setLeaderboard([]);
    }
  };

  const fetchChallenges = async (roomId) => {
    try {
      const response = await axios.get(`http://localhost:8000/gamification/challenges/${roomId}`);
      setChallenges(response.data.challenges || []);
    } catch (error) {
      console.error("Error fetching challenges:", error);
      setChallenges([]);
    }
  };

  const submitChallenge = async (challengeId, submissionData, isCorrect = false) => {
    try {
      const response = await axios.post(`http://localhost:8000/gamification/challenges/submit`, {
        username,
        challenge_id: challengeId,
        submission_data: submissionData,
        is_correct: isCorrect
      });
      
      // Refresh user stats after submission
      await fetchUserStats();
      
      return response.data;
    } catch (error) {
      console.error("Error submitting challenge:", error);
      throw error;
    }
  };

  const createChallenge = async (roomId, title, description, challengeType, pointsReward = 10) => {
    try {
      const response = await axios.post(`http://localhost:8000/gamification/challenges/${roomId}/create`, {
        title,
        description,
        challenge_type: challengeType,
        points_reward: pointsReward
      });
      
      // Refresh challenges after creation
      await fetchChallenges(roomId);
      
      return response.data;
    } catch (error) {
      console.error("Error creating challenge:", error);
      throw error;
    }
  };

  useEffect(() => {
    if (username) {
      fetchUserStats();
      fetchBadges();
    }
  }, [username]);

  const value = {
    userStats,
    badges,
    leaderboard,
    challenges,
    loading,
    fetchUserStats,
    fetchBadges,
    fetchLeaderboard,
    fetchChallenges,
    submitChallenge,
    createChallenge
  };

  return (
    <GamificationContext.Provider value={value}>
      {children}
    </GamificationContext.Provider>
  );
};
