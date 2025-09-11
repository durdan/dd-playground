import React from 'react';
import './EventCard.css';

export interface Team {
  name: string;
  logo?: string;
  score?: number;
}

export interface SportEvent {
  id: string;
  homeTeam: Team;
  awayTeam: Team;
  date: Date;
  status: 'upcoming' | 'live' | 'finished';
  sport: string;
  venue?: string;
}

interface EventCardProps {
  event: SportEvent;
  onClick?: (event: SportEvent) => void;
}

export const EventCard: React.FC<EventCardProps> = ({ event, onClick }) => {
  const formatDate = (date: Date): string => {
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'live': return 'status-live';
      case 'finished': return 'status-finished';
      default: return 'status-upcoming';
    }
  };

  const handleClick = () => {
    if (onClick) {
      onClick(event);
    }
  };

  return (
    <div 
      className={`event-card ${onClick ? 'clickable' : ''}`}
      onClick={handleClick}
    >
      <div className="event-header">
        <span className="sport-type">{event.sport}</span>
        <span className={`event-status ${getStatusColor(event.status)}`}>
          {event.status.toUpperCase()}
        </span>
      </div>
      
      <div className="teams-container">
        <div className="team">
          {event.homeTeam.logo && (
            <img src={event.homeTeam.logo} alt={event.homeTeam.name} className="team-logo" />
          )}
          <span className="team-name">{event.homeTeam.name}</span>
          {event.homeTeam.score !== undefined && (
            <span className="team-score">{event.homeTeam.score}</span>
          )}
        </div>
        
        <div className="vs-divider">VS</div>
        
        <div className="team">
          {event.awayTeam.logo && (
            <img src={event.awayTeam.logo} alt={event.awayTeam.name} className="team-logo" />
          )}
          <span className="team-name">{event.awayTeam.name}</span>
          {event.awayTeam.score !== undefined && (
            <span className="team-score">{event.awayTeam.score}</span>
          )}
        </div>
      </div>
      
      <div className="event-footer">
        <span className="event-date">{formatDate(event.date)}</span>
        {event.venue && <span className="event-venue">{event.venue}</span>}
      </div>
    </div>
  );
};