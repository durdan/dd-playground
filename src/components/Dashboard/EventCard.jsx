import React from 'react';
import { EventsService } from '../../services/EventsService';
import './EventCard.css';

export const EventCard = ({ event, showTimeAgo = false, showCountdown = false }) => {
  const getStatusColor = (status) => {
    const colors = {
      'active': '#4caf50',
      'upcoming': '#2196f3',
      'completed': '#9e9e9e',
      'cancelled': '#f44336'
    };
    return colors[status] || '#9e9e9e';
  };

  return (
    <div className="event-card">
      <div className="event-header">
        <h3 className="event-title">{event.title}</h3>
        <span 
          className="event-status"
          style={{ backgroundColor: getStatusColor(event.status) }}
        >
          {event.status}
        </span>
      </div>

      <div className="event-details">
        <div className="event-date">
          📅 {EventsService.formatEventDate(event.date)}
        </div>
        
        {event.location && (
          <div className="event-location">
            📍 {event.location}
          </div>
        )}

        {event.attendeeCount && (
          <div className="event-attendees">
            👥 {event.attendeeCount} attendees
          </div>
        )}

        {showCountdown && (
          <div className="event-countdown">
            ⏰ {EventsService.getTimeUntilEvent(event.date)}
          </div>
        )}

        {showTimeAgo && (
          <div className="event-time-ago">
            🕒 {EventsService.getTimeUntilEvent(event.date)}
          </div>
        )}
      </div>

      {event.description && (
        <div className="event-description">
          {event.description.length > 100 
            ? `${event.description.substring(0, 100)}...`
            : event.description
          }
        </div>
      )}
    </div>
  );
};