const mongoose = require('mongoose');

const eventSchema = new mongoose.Schema({
  homeTeam: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Team',
    required: true
  },
  awayTeam: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Team',
    required: true
  },
  sport: {
    type: String,
    required: true,
    enum: ['football', 'basketball', 'baseball', 'hockey', 'soccer'],
    lowercase: true
  },
  league: {
    type: String,
    required: true,
    trim: true,
    maxlength: 50
  },
  season: {
    type: String,
    required: true,
    match: /^\d{4}(-\d{4})?$/  // 2023 or 2023-2024
  },
  week: {
    type: Number,
    min: 1,
    max: 52
  },
  scheduledDate: {
    type: Date,
    required: true
  },
  actualStartTime: Date,
  venue: {
    name: String,
    city: String,
    capacity: Number
  },
  status: {
    type: String,
    enum: ['scheduled', 'in_progress', 'completed', 'postponed', 'cancelled'],
    default: 'scheduled'
  },
  score: {
    home: {
      type: Number,
      min: 0,
      default: 0
    },
    away: {
      type: Number,
      min: 0,
      default: 0
    }
  },
  attendance: {
    type: Number,
    min: 0
  }
}, {
  timestamps: true
});

// Validation: teams must be different
eventSchema.pre('save', function(next) {
  if (this.homeTeam.equals(this.awayTeam)) {
    next(new Error('Home team and away team cannot be the same'));
  }
  next();
});

// Indexes for efficient queries
eventSchema.index({ scheduledDate: 1 });
eventSchema.index({ homeTeam: 1, scheduledDate: 1 });
eventSchema.index({ awayTeam: 1, scheduledDate: 1 });
eventSchema.index({ league: 1, season: 1, scheduledDate: 1 });
eventSchema.index({ sport: 1, status: 1, scheduledDate: 1 });
eventSchema.index({ season: 1, week: 1 });

module.exports = mongoose.model('Event', eventSchema);