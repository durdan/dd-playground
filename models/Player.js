const mongoose = require('mongoose');

const playerSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'User reference is required']
  },
  sport: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Sport',
    required: [true, 'Sport is required']
  },
  team: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Team'
  },
  profile: {
    jerseyNumber: {
      type: Number,
      min: [1, 'Jersey number must be at least 1'],
      max: [999, 'Jersey number cannot exceed 999']
    },
    position: {
      type: String,
      trim: true,
      maxlength: [50, 'Position cannot exceed 50 characters']
    },
    height: {
      type: Number, // in cm
      min: [100, 'Height must be at least 100cm'],
      max: [300, 'Height cannot exceed 300cm']
    },
    weight: {
      type: Number, // in kg
      min: [30, 'Weight must be at least 30kg'],
      max: [300, 'Weight cannot exceed 300kg']
    },
    dateOfBirth: {
      type: Date,
      validate: {
        validator: function(date) {
          const age = (new Date() - date) / (365.25 * 24 * 60 * 60 * 1000);
          return age >= 16 && age <= 50;
        },
        message: 'Player must be between 16 and 50 years old'
      }
    }
  },
  stats: {
    gamesPlayed: {
      type: Number,
      default: 0,
      min: [0, 'Games played cannot be negative']
    },
    points: {
      type: Number,
      default: 0,
      min: [0, 'Points cannot be negative']
    },
    // Sport-specific stats can be added dynamically
    customStats: {
      type: Map,
      of: Number,
      default: new Map()
    }
  },
  status: {
    type: String,
    enum: ['active', 'injured', 'suspended', 'retired'],
    default: 'active'
  },
  joinedTeamAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes
playerSchema.index({ user: 1, sport: 1 }, { unique: true });
playerSchema.index({ team: 1 });
playerSchema.index({ sport: 1 });
playerSchema.index({ 'profile.jerseyNumber': 1, team: 1 }, { 
  unique: true, 
  sparse: true,
  partialFilterExpression: { 'profile.jerseyNumber': { $exists: true } }
});

// Virtual for age
playerSchema.virtual('age').get(function() {
  if (!this.profile.dateOfBirth) return null;
  return Math.floor((new Date() - this.profile.dateOfBirth) / (365.25 * 24 * 60 * 60 * 1000));
});

module.exports = mongoose.model('Player', playerSchema);