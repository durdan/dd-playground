const Team = require('../models/Team');
const Event = require('../models/Event');
const Statistics = require('../models/Statistics');

class QueryHelpers {
  // Get events for a team within date range
  static async getTeamEvents(teamId, startDate, endDate, options = {}) {
    const query = {
      $or: [{ homeTeam: teamId }, { awayTeam: teamId }],
      scheduledDate: {
        $gte: new Date(startDate),
        $lte: new Date(endDate)
      }
    };

    if (options.status) {
      query.status = options.status;
    }

    return Event.find(query)
      .populate('homeTeam awayTeam', 'name shortName')
      .sort({ scheduledDate: 1 })
      .limit(options.limit || 100);
  }

  // Get team statistics aggregated by sport
  static async getTeamStats(teamId, sport, options = {}) {
    const matchStage = {
      team: teamId,
      sport: sport,
      category: 'team'
    };

    if (options.season) {
      // Join with events to filter by season
      const pipeline = [
        { $match: matchStage },
        {
          $lookup: {
            from: 'events',
            localField: 'event',
            foreignField: '_id',
            as: 'eventData'
          }
        },
        { $unwind: '$eventData' },
        { $match: { 'eventData.season': options.season } }
      ];

      return Statistics.aggregate(pipeline);
    }

    return Statistics.find(matchStage)
      .populate('event', 'scheduledDate season')
      .sort({ recordedAt: -1 })
      .limit(options.limit || 50);
  }

  // Get league standings helper
  static async getLeagueStandings(league, season) {
    return Event.aggregate([
      {
        $match: {
          league: league,
          season: season,
          status: 'completed'
        }
      },
      {
        $facet: {
          homeGames: [
            {
              $group: {
                _id: '$homeTeam',
                wins: {
                  $sum: {
                    $cond: [{ $gt: ['$score.home', '$score.away'] }, 1, 0]
                  }
                },
                losses: {
                  $sum: {
                    $cond: [{ $lt: ['$score.home', '$score.away'] }, 1, 0]
                  }
                },
                pointsFor: { $sum: '$score.home' },
                pointsAgainst: { $sum: '$score.away' }
              }
            }
          ],
          awayGames: [
            {
              $group: {
                _id: '$awayTeam',
                wins: {
                  $sum: {
                    $cond: [{ $gt: ['$score.away', '$score.home'] }, 1, 0]
                  }
                },
                losses: {
                  $sum: {
                    $cond: [{ $lt: ['$score.away', '$score.home'] }, 1, 0]
                  }
                },
                pointsFor: { $sum: '$score.away' },
                pointsAgainst: { $sum: '$score.home' }
              }
            }
          ]
        }
      }
    ]);
  }
}

module.exports = QueryHelpers;