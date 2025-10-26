import React, { useState, useEffect } from "react";
import { FiAward, FiStar, FiTrendingUp, FiZap } from "react-icons/fi";

export default function GamificationNotification({ notification, onClose }) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (notification) {
      setIsVisible(true);
      const timer = setTimeout(() => {
        setIsVisible(false);
        setTimeout(() => onClose(), 300);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [notification, onClose]);

  if (!notification || !isVisible) return null;

  const getNotificationIcon = (type) => {
    switch (type) {
      case "badge":
        return <FiAward className="text-yellow-400" size={24} />;
      case "level":
        return <FiTrendingUp className="text-blue-400" size={24} />;
      case "streak":
        return <FiStar className="text-green-400" size={24} />;
      case "points":
        return <FiZap className="text-purple-400" size={24} />;
      default:
        return <FiAward className="text-yellow-400" size={24} />;
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case "badge":
        return "bg-yellow-900 border-yellow-700";
      case "level":
        return "bg-blue-900 border-blue-700";
      case "streak":
        return "bg-green-900 border-green-700";
      case "points":
        return "bg-purple-900 border-purple-700";
      default:
        return "bg-gray-900 border-gray-700";
    }
  };

  return (
    <div
      className={`fixed top-4 right-4 z-50 transform transition-all duration-300 ${
        isVisible ? "translate-x-0 opacity-100" : "translate-x-full opacity-0"
      }`}
    >
      <div
        className={`${getNotificationColor(notification.type)} border rounded-lg p-4 shadow-lg max-w-sm`}
      >
        <div className="flex items-start space-x-3">
          {getNotificationIcon(notification.type)}
          <div className="flex-1">
            <h4 className="text-white font-semibold text-sm mb-1">
              {notification.title}
            </h4>
            <p className="text-gray-200 text-sm">
              {notification.message}
            </p>
            {notification.points && (
              <p className="text-yellow-400 text-xs mt-1 font-medium">
                +{notification.points} points earned!
              </p>
            )}
          </div>
          <button
            onClick={() => {
              setIsVisible(false);
              setTimeout(() => onClose(), 300);
            }}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
}
