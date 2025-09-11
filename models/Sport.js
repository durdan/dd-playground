const mongoose = require('mongoose');

const sportSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Sport name is required'],
    unique: true,
    trim: true,
    maxlength: [50, 'Sport name cannot exceed 50 characters']
  },
  category: {
    type: String,
    required: [true, 'Category is required'],
    enum: ['team', 'individual', 'combat', 'racing', 'water', 'winter', 'other'],
    lowercase: true
  },
  description: {
    type: String,
    trim: true,
    maxlength: [500, 'Description cannot exceed 500 characters']
  },
  rules: {
    playersPerTeam: {
      type: Number,
      min: [1, 'Must have at least 1 player per team'],
      max: [50, 'Cannot exceed 50 players per team']
    },
    gameDuration: {
      type: Number, // in minutes
      min: [1, 'Game duration must be at least 1 minute']
    },
    scoringSystem: {
      type: String,
      enum: ['points', 'goals', 'time', 'distance', 'other'],
      default: 'points'
    }
  },
  equipment: [{
    type: String,
    trim: true,
    maxlength: [100, 'Equipment name cannot exceed 100 characters']
  }],
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

// Indexes
sportSchema.index({ name: 1 });
sportSchema.index({ category: 1 });
sportSchema.index({ isActive: 1 });

module.exports = mongoose.model('Sport', sportSchema);