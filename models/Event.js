class Event {
  constructor({ id, title, description, startDate, endDate, location, createdAt }) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.startDate = new Date(startDate);
    this.endDate = new Date(endDate);
    this.location = location;
    this.createdAt = createdAt ? new Date(createdAt) : new Date();
  }

  static validate(eventData) {
    const errors = [];
    
    if (!eventData.title || typeof eventData.title !== 'string') {
      errors.push('Title is required and must be a string');
    }
    
    if (!eventData.startDate || isNaN(new Date(eventData.startDate))) {
      errors.push('Valid start date is required');
    }
    
    if (!eventData.endDate || isNaN(new Date(eventData.endDate))) {
      errors.push('Valid end date is required');
    }
    
    if (eventData.startDate && eventData.endDate && 
        new Date(eventData.startDate) >= new Date(eventData.endDate)) {
      errors.push('End date must be after start date');
    }
    
    return errors;
  }
}

module.exports = Event;