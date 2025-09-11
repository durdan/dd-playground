const mongoose = require('mongoose');

const teamSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Team name is required'],
    trim: true,
    maxlength: [100, 'Team name cannot exceed 100 characters']
  },
  sport: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Sport',
    required: [true, 'Sport is required']
  },
  league: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'League'
  },
  coach: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  players: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Player'
  }],
  details: {
    founded: {
      type: Date,
      validate: {
        validator: function(date) {
          return date <= new Date();
        },
        message: 'Founded date cannot be in the future'
      }
    },
    city: {
      type: String,
      trim: true,
      maxlength: [100, 'City name cannot exceed 100 characters']
    },
    stadium: {
      type: String,
      trim: true,
      maxlength: [100, 'Stadium name cannot exceed 100 characters']
    },
    logo: {
      type: String,
      match: [/^https?:\/\/.+/, 'Logo must be a valid URL']
    }
  },
  stats: {
    wins: {
      type: Number,
      default: 0,
      min: [0, 'Wins cannot be negative']
    },
    losses: {
      type: Number,
      default: 0,
      min: [0, 'Losses cannot be negative']
    },
    draws: {
      type: Number,
      default: 0,
      min: [0, 'Draws cannot be negative']
    }
  },
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes
teamSchema.index({ name: 1, sport: 1 }, { unique: true });
teamSchema.index({ sport: 1 });
teamSchema.index({ league: 1 });
teamSchema.index({ coach: 1 });

// Virtual for total games
teamSchema.virtual('totalGames').get(function() {
  return this.stats.wins + this.stats.losses + this.stats.draws;
});

// Virtual for win percentage
teamSchema.virtual('winPercentage').get(function() {
  const total = this.totalGames;
  return total > 0 ? ((this.stats.wins / total) * 100).toFixed(2) : 0;
});

module.exports = mongoose.model('Team', teamSchema);