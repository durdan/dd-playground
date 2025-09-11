const mongoose = require('mongoose');

const teamSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
    maxlength: 100
  },
  shortName: {
    type: String,
    required: true,
    trim: true,
    maxlength: 10,
    uppercase: true
  },
  league: {
    type: String,
    required: true,
    trim: true,
    maxlength: 50
  },
  sport: {
    type: String,
    required: true,
    enum: ['football', 'basketball', 'baseball', 'hockey', 'soccer'],
    lowercase: true
  },
  city: {
    type: String,
    required: true,
    trim: true,
    maxlength: 50
  },
  country: {
    type: String,
    required: true,
    trim: true,
    maxlength: 50,
    default: 'USA'
  },
  founded: {
    type: Number,
    min: 1800,
    max: new Date().getFullYear()
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// Indexes for efficient queries
teamSchema.index({ league: 1, sport: 1 });
teamSchema.index({ shortName: 1 }, { unique: true });
teamSchema.index({ name: 1 });
teamSchema.index({ sport: 1, isActive: 1 });

module.exports = mongoose.model('Team', teamSchema);