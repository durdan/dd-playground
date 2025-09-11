import React from 'react';
import { EventCard, SportEvent } from '../EventCard/EventCard';
import './UpcomingEvents.css';

interface UpcomingEventsProps {
  events: SportEvent[];
  title?: string;
  maxEvents?: number;
  loading?: boolean;
  onEventClick?: (event: SportEvent) => void;
  onViewAll?: () => void;
}

export const UpcomingEvents: React.FC<UpcomingEventsProps> = ({
  events,
  title = 'Upcoming Events',
  maxEvents,
  loading = false,
  onEventClick,
  onViewAll
}) => {
  const sortEventsByDate = (events: SportEvent[]): SportEvent[] => {
    return [...events].sort((a, b) => a.date.getTime() - b.date.getTime());
  };

  const filterUpcomingEvents = (events: SportEvent[]): SportEvent[] => {
    const now = new Date();
    return events.filter(event => 
      event.status === 'upcoming' && event.date > now
    );
  };

  const getDisplayEvents = (): SportEvent[] => {
    const upcomingEvents = filterUpcomingEvents(events);
    const sortedEvents = sortEventsByDate(upcomingEvents);
    
    if (maxEvents && maxEvents > 0) {
      return sortedEvents.slice(0, maxEvents);
    }
    
    return sortedEvents;
  };

  const displayEvents = getDisplayEvents();
  const hasMoreEvents = maxEvents && events.length > maxEvents;

  if (loading) {
    return (
      <div className="upcoming-events">
        <h3 className="upcoming-events-title">{title}</h3>
        <div className="upcoming-events-loading">
          <div className="loading-spinner"></div>
          <span>Loading events...</span>
        </div>
      </div>
    );
  }

  if (!displayEvents.length) {
    return (
      <div className="upcoming-events">
        <h3 className="upcoming-events-title">{title}</h3>
        <div className="upcoming-events-empty">
          <span>No upcoming events scheduled</span>
        </div>
      </div>
    );
  }

  return (
    <div className="upcoming-events">
      <div className="upcoming-events-header">
        <h3 className="upcoming-events-title">{title}</h3>
        {hasMoreEvents && onViewAll && (
          <button 
            className="view-all-button"
            onClick={onViewAll}
          >
            View All
          </button>
        )}
      </div>
      
      <div className="events-list">
        {displayEvents.map(event => (
          <EventCard
            key={event.id}
            event={event}
            onClick={onEventClick}
          />
        ))}
      </div>
      
      {hasMoreEvents && !onViewAll && (
        <div className="events-count">
          Showing {displayEvents.length} of {events.length} events
        </div>
      )}
    </div>
  );
};