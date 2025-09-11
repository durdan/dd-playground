import React, { useState, useEffect } from 'react';
import { EventsService } from '../../services/EventsService';
import { StatsCards } from './StatsCards';
import { LatestEvents } from './LatestEvents';
import { UpcomingEvents } from './UpcomingEvents';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';
import './Dashboard.css';

export const Dashboard = () => {
  const [data, setData] = useState({
    latestEvents: [],
    upcomingEvents: [],
    statistics: {}
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [latestEvents, upcomingEvents, statistics] = await Promise.all([
        EventsService.fetchLatestEvents(),
        EventsService.fetchUpcomingEvents(),
        EventsService.fetchStatistics()
      ]);

      setData({
        latestEvents,
        upcomingEvents,
        statistics
      });
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={loadDashboardData} />;

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Event Dashboard</h1>
        <button onClick={loadDashboardData} className="refresh-btn">
          Refresh
        </button>
      </header>

      <div className="dashboard-content">
        <section className="stats-section">
          <StatsCards statistics={data.statistics} />
        </section>

        <div className="events-grid">
          <section className="latest-section">
            <LatestEvents events={data.latestEvents} />
          </section>

          <section className="upcoming-section">
            <UpcomingEvents events={data.upcomingEvents} />
          </section>
        </div>
      </div>
    </div>
  );
};