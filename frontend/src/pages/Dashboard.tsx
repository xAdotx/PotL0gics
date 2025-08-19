import React from 'react'
import { Link } from 'react-router-dom'
import { 
  Calculator, 
  Activity, 
  TrendingUp, 
  DollarSign,
  Play,
  Settings
} from 'lucide-react'

export function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Welcome to Pot Logic - Your advanced poker analysis companion
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Calculator className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Pot Odds Calculated</p>
              <p className="text-2xl font-semibold text-gray-900">1,234</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Activity className="h-8 w-8 text-success-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Hands Analyzed</p>
              <p className="text-2xl font-semibold text-gray-900">567</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-warning-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Win Rate</p>
              <p className="text-2xl font-semibold text-gray-900">68.5%</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <DollarSign className="h-8 w-8 text-success-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Session Profit</p>
              <p className="text-2xl font-semibold text-gray-900">$1,234</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Link
              to="/pot-odds"
              className="flex items-center p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <Calculator className="h-5 w-5 text-primary-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">Calculate Pot Odds</p>
                <p className="text-sm text-gray-500">Get instant pot odds analysis</p>
              </div>
            </Link>

            <Link
              to="/poker-bot"
              className="flex items-center p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <Activity className="h-5 w-5 text-primary-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">Poker Bot</p>
                <p className="text-sm text-gray-500">Advanced poker analysis & calculations</p>
              </div>
            </Link>

            <Link
              to="/hand-evaluator"
              className="flex items-center p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <Activity className="h-5 w-5 text-primary-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">Evaluate Hand</p>
                <p className="text-sm text-gray-500">Analyze your hand strength</p>
              </div>
            </Link>

            <Link
              to="/statistics"
              className="flex items-center p-3 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors"
            >
              <TrendingUp className="h-5 w-5 text-primary-600 mr-3" />
              <div>
                <p className="font-medium text-gray-900">View Statistics</p>
                <p className="text-sm text-gray-500">Check your performance metrics</p>
              </div>
            </Link>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Pot odds calculated</p>
                <p className="text-sm text-gray-500">A♠ K♥ vs 3 players</p>
              </div>
              <span className="text-sm text-gray-500">2 min ago</span>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Hand evaluated</p>
                <p className="text-sm text-gray-500">Full House - Aces over Kings</p>
              </div>
              <span className="text-sm text-gray-500">5 min ago</span>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900">Game saved</p>
                <p className="text-sm text-gray-500">Won $45.50</p>
              </div>
              <span className="text-sm text-gray-500">10 min ago</span>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Features</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                <Calculator className="h-5 w-5 text-primary-600" />
              </div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-gray-900">Pot Odds Calculator</h4>
              <p className="text-sm text-gray-500">Calculate pot odds and implied odds in real-time</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center">
                <Activity className="h-5 w-5 text-success-600" />
              </div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-gray-900">Hand Evaluator</h4>
              <p className="text-sm text-gray-500">Evaluate hand strength and calculate outs</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-warning-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="h-5 w-5 text-warning-600" />
              </div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-gray-900">Statistics</h4>
              <p className="text-sm text-gray-500">Track your performance and analyze trends</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                <Play className="h-5 w-5 text-primary-600" />
              </div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-gray-900">Real-time Analysis</h4>
              <p className="text-sm text-gray-500">Get live updates during your games</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                <Activity className="h-5 w-5 text-indigo-600" />
              </div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-gray-900">Poker Bot</h4>
              <p className="text-sm text-gray-500">Advanced calculations and strategy recommendations</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center">
                <DollarSign className="h-5 w-5 text-success-600" />
              </div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-gray-900">Profit Tracking</h4>
              <p className="text-sm text-gray-500">Monitor your wins and losses</p>
            </div>
          </div>

          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-warning-100 rounded-lg flex items-center justify-center">
                <Settings className="h-5 w-5 text-warning-600" />
              </div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-gray-900">Customizable</h4>
              <p className="text-sm text-gray-500">Adjust settings to your preferences</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 