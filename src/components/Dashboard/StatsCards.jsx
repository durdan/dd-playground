import React from 'react';
import './StatsCards.css';

export const StatsCards = ({ statistics }) => {
  const stats = [
    {
      key: 'totalEvents',
      label: 'Total Events',
      value: statistics.totalEvents || 0,
      icon: '📅'
    },
    {
      key: 'activeEvents',
      label: 'Active Events',
      value: statistics.activeEvents || 0,
      icon: '🟢'
    },
    {
      key: 'totalAttendees',
      label: 'Total Attendees',
      value: statistics.totalAttendees || 0,
      icon: '👥'
    },
    {
      key: 'upcomingEvents',
      label: 'Upcoming Events',
      value: statistics.upcomingEvents || 0,
      icon: '⏰'
    }
  ];

  return (
    <div className="stats-cards">
      {stats.map(stat => (
        <div key={stat.key} className="stat-card">
          <div className="stat-icon">{stat.icon}</div>
          <div className="stat-content">
            <div className="stat-value">{stat.value.toLocaleString()}</div>
            <div className="stat-label">{stat.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
};