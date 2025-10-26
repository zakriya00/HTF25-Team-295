import React, { useState, useEffect } from "react";
import { FiAward, FiStar, FiTarget, FiUsers, FiTrendingUp, FiZap } from "react-icons/fi";
import { useGamification } from "../context/GamificationContext";

export default function GamificationSidebar({ room, isOpen, onClose }) {
  const { 
    userStats, 
    badges, 
    leaderboard, 
    challenges, 
    fetchLeaderboard, 
    fetchChallenges 
  } = useGamification();
  
  const [activeTab, setActiveTab] = useState("stats");

  useEffect(() => {
    if (room && isOpen) {
      fetchLeaderboard(room);
      fetchChallenges(room);
    }
  }, [room, isOpen, fetchLeaderboard, fetchChallenges]);

  if (!isOpen) return null;

  const getLevelColor = (level) => {
    if (level >= 20) return "text-purple-400";
    if (level >= 10) return "text-blue-400";
    if (level >= 5) return "text-green-400";
    return "text-yellow-400";
  };

  const getStreakEmoji = (streak) => {
    if (streak >= 30) return "👑";
    if (streak >= 14) return "🏆";
    if (streak >= 7) return "⚡";
    if (streak >= 3) return "🔥";
    return "📚";
  };

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50">
      <div className="fixed right-0 top-0 h-full w-96 bg-gray-900 border-l border-gray-800 overflow-y-auto">
        {/* Header */}
        <div className="p-4 border-b border-gray-800">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white flex items-center">
              <FiAward className="mr-2 text-yellow-400" />
              Gamification
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-gray-800">
          {[
            { id: "stats", label: "Stats", icon: FiTrendingUp },
            { id: "badges", label: "Badges", icon: FiAward },
            { id: "leaderboard", label: "Leaderboard", icon: FiAward },
            { id: "challenges", label: "Challenges", icon: FiTarget }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex-1 flex items-center justify-center py-3 px-4 text-sm font-medium transition-colors ${
                activeTab === id
                  ? "text-blue-400 border-b-2 border-blue-400 bg-blue-900/20"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              <Icon className="mr-1" size={16} />
              {label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Stats Tab */}
          {activeTab === "stats" && userStats && (
            <div className="space-y-6">
              {/* User Level & Points */}
              <div className="bg-gray-800 rounded-lg p-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-white">Your Progress</h3>
                  <span className={`text-2xl font-bold ${getLevelColor(userStats.level)}`}>
                    Level {userStats.level}
                  </span>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Points</span>
                    <span className="text-yellow-400 font-semibold">{userStats.points}</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Study Streak</span>
                    <span className="text-green-400 font-semibold flex items-center">
                      {getStreakEmoji(userStats.study_streak)} {userStats.study_streak} days
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Messages</span>
                    <span className="text-blue-400 font-semibold">{userStats.total_messages}</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Files Shared</span>
                    <span className="text-purple-400 font-semibold">{userStats.total_files_shared}</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Helpful Answers</span>
                    <span className="text-green-400 font-semibold">{userStats.total_helpful_answers}</span>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="bg-gray-800 rounded-lg p-4">
                <h4 className="text-sm font-medium text-gray-300 mb-2">Level Progress</h4>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(userStats.points % 1000) / 10}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  {userStats.points % 1000} / 1000 points to next level
                </p>
              </div>
            </div>
          )}

          {/* Badges Tab */}
          {activeTab === "badges" && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white mb-4">Your Badges</h3>
              
              {badges.length === 0 ? (
                <div className="text-center py-8">
                  <FiAward className="mx-auto text-gray-600 mb-2" size={48} />
                  <p className="text-gray-400">No badges earned yet</p>
                  <p className="text-sm text-gray-500">Keep participating to earn badges!</p>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-4">
                  {badges.map((badge, index) => (
                    <div key={index} className="bg-gray-800 rounded-lg p-4 text-center">
                      <div className="text-3xl mb-2">{badge.icon}</div>
                      <h4 className="text-sm font-semibold text-white mb-1">{badge.name}</h4>
                      <p className="text-xs text-gray-400">{badge.description}</p>
                      <p className="text-xs text-gray-500 mt-2">
                        Earned {new Date(badge.earned_at).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Leaderboard Tab */}
          {activeTab === "leaderboard" && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white mb-4">Room Leaderboard</h3>
              
              {leaderboard.length === 0 ? (
                <div className="text-center py-8">
                  <FiUsers className="mx-auto text-gray-600 mb-2" size={48} />
                  <p className="text-gray-400">No participants yet</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {leaderboard.map((user, index) => (
                    <div key={index} className={`flex items-center justify-between p-3 rounded-lg ${
                      index === 0 ? "bg-yellow-900/30 border border-yellow-500/30" :
                      index === 1 ? "bg-gray-700/50 border border-gray-600/30" :
                      index === 2 ? "bg-orange-900/30 border border-orange-500/30" :
                      "bg-gray-800 border border-gray-700/30"
                    }`}>
                      <div className="flex items-center">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold mr-3 ${
                          index === 0 ? "bg-yellow-500 text-black" :
                          index === 1 ? "bg-gray-400 text-black" :
                          index === 2 ? "bg-orange-500 text-black" :
                          "bg-gray-600 text-white"
                        }`}>
                          {index + 1}
                        </div>
                        <div>
                          <p className="text-white font-medium">{user.username}</p>
                          <p className="text-xs text-gray-400">Level {user.level}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-yellow-400 font-semibold">{user.points} pts</p>
                        <p className="text-xs text-gray-400">{user.study_streak} day streak</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Challenges Tab */}
          {activeTab === "challenges" && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white mb-4">Daily Challenges</h3>
              
              {challenges.length === 0 ? (
                <div className="text-center py-8">
                  <FiTarget className="mx-auto text-gray-600 mb-2" size={48} />
                  <p className="text-gray-400">No active challenges</p>
                  <p className="text-sm text-gray-500">Check back later for new challenges!</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {challenges.map((challenge, index) => (
                    <div key={index} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                      <div className="flex items-start justify-between mb-2">
                        <h4 className="text-white font-semibold">{challenge.title}</h4>
                        <span className="text-yellow-400 text-sm font-medium">
                          +{challenge.points_reward} pts
                        </span>
                      </div>
                      <p className="text-gray-300 text-sm mb-3">{challenge.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-400 capitalize">
                          {challenge.challenge_type} challenge
                        </span>
                        <span className="text-xs text-gray-500">
                          Expires {new Date(challenge.expires_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
