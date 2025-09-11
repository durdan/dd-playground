import React from 'react';
import { EventCard } from './EventCard';
import './LatestEvents.css';

export const LatestEvents = ({ events }) => {
  if (!events || events.length === 0) {
    return (
      <div className="latest-events">
        <h2>Latest Events</h2>
        <div className="no-events">No recent events found</div>
      </div>
    );
  }

  return (
    <div className="latest-events">
      <h2>Latest Events</h2>
      <div className="events-list">
        {events.map(event => (
          <EventCard 
            key={event.id} 
            event={event} 
            showTimeAgo={true}
          />
        ))}
      </div>
    </div>
  );
};