export class EventsService {
  static async fetchLatestEvents(limit = 5) {
    try {
      const response = await fetch(`/api/events/latest?limit=${limit}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch latest events: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      throw new Error(`Error fetching latest events: ${error.message}`);
    }
  }

  static async fetchUpcomingEvents(limit = 5) {
    try {
      const response = await fetch(`/api/events/upcoming?limit=${limit}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch upcoming events: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      throw new Error(`Error fetching upcoming events: ${error.message}`);
    }
  }

  static async fetchStatistics() {
    try {
      const response = await fetch('/api/events/statistics');
      if (!response.ok) {
        throw new Error(`Failed to fetch statistics: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      throw new Error(`Error fetching statistics: ${error.message}`);
    }
  }

  static formatEventDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  static getTimeUntilEvent(dateString) {
    const eventDate = new Date(dateString);
    const now = new Date();
    const diffMs = eventDate - now;
    
    if (diffMs < 0) return 'Past event';
    
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    
    if (days > 0) return `${days} days`;
    if (hours > 0) return `${hours} hours`;
    return 'Soon';
  }
}