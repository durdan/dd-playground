const mongoose = require('mongoose');

const statisticsSchema = new mongoose.Schema({
  event: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Event',
    required: true
  },
  team: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Team',
    required: true
  },
  player: {
    name: String,
    position: String,
    number: Number
  },
  sport: {
    type: String,
    required: true,
    enum: ['football', 'basketball', 'baseball', 'hockey', 'soccer'],
    lowercase: true
  },
  category: {
    type: String,
    required: true,
    enum: ['team', 'player'],
    lowercase: true
  },
  period: {
    type: String,
    enum: ['game', 'quarter', 'half', 'period', 'inning'],
    default: 'game'
  },
  periodNumber: {
    type: Number,
    min: 1
  },
  stats: {
    type: Map,
    of: mongoose.Schema.Types.Mixed,
    required: true
  },
  recordedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true
});

// Validation: player stats must have player info
statisticsSchema.pre('save', function(next) {
  if (this.category === 'player' && !this.player?.name) {
    next(new Error('Player statistics must include player name'));
  }
  next();
});

// Indexes for efficient queries
statisticsSchema.index({ event: 1, team: 1, category: 1 });
statisticsSchema.index({ team: 1, sport: 1, category: 1 });
statisticsSchema.index({ 'player.name': 1, sport: 1 });
statisticsSchema.index({ event: 1, period: 1, periodNumber: 1 });
statisticsSchema.index({ sport: 1, category: 1, recordedAt: 1 });

module.exports = mongoose.model('Statistics', statisticsSchema);