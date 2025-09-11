import React from 'react';
import { EventCard } from './EventCard';
import './UpcomingEvents.css';

export const UpcomingEvents = ({ events }) => {
  if (!events || events.length === 0) {
    return (
      <div className="upcoming-events">
        <h2>Upcoming Events</h2>
        <div className="no-events">No upcoming events scheduled</div>
      </div>
    );
  }

  return (
    <div className="upcoming-events">
      <h2>Upcoming Events</h2>
      <div className="events-list">
        {events.map(event => (
          <EventCard 
            key={event.id} 
            event={event} 
            showCountdown={true}
          />
        ))}
      </div>
    </div>
  );
};