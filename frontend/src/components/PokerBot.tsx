import React, { useState, useEffect } from 'react';
import PokerBotAPI from '../utils/main';

interface PokerCalculation {
  potOdds: number;
  equity: number;
  expectedValue: number;
  recommendation: string;
  breakEvenPercentage: number;
}

const PokerBot: React.FC = () => {
  const [formData, setFormData] = useState({
    potSize: '',
    betSize: '',
    callAmount: '',
    handStrength: 'medium',
    position: 'middle',
    stackSize: '',
    villainStack: '',
    street: 'flop',
    outs: '',
    potOdds: 0,
    equity: 0,
    expectedValue: 0,
    recommendation: '',
    breakEvenPercentage: 0
  });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Initialize PokerBotAPI when component mounts
  useEffect(() => {
    // The PokerBotAPI will be initialized automatically when imported
    // This ensures the service worker and event listeners are set up
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 text-white p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">🃏 Pot Logic</h1>
          <p className="text-blue-200 text-lg">Advanced Poker Bot & Calculator</p>
        </div>

        {/* Main Calculator */}
        <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-6 border border-white/20">
          <h2 className="text-2xl font-semibold mb-6 text-center">Poker Calculator</h2>
          
          <form className="poker-form">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Left Column - Basic Inputs */}
            <div className="space-y-4">
              <h3 className="text-xl font-medium text-blue-200 mb-4">Basic Information</h3>
              
              <div>
                <label className="block text-sm font-medium mb-2">Pot Size ($)</label>
                <input
                  type="number"
                  name="potSize"
                  value={formData.potSize}
                  onChange={handleInputChange}
                  placeholder="100"
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-300"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Bet Size ($)</label>
                <input
                  type="number"
                  name="betSize"
                  value={formData.betSize}
                  onChange={handleInputChange}
                  placeholder="50"
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-300"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Call Amount ($)</label>
                <input
                  type="number"
                  name="callAmount"
                  value={formData.callAmount}
                  onChange={handleInputChange}
                  placeholder="50"
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-300"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Number of Outs</label>
                <input
                  type="number"
                  name="outs"
                  value={formData.outs}
                  onChange={handleInputChange}
                  placeholder="8"
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-300"
                />
              </div>
            </div>

            {/* Right Column - Advanced Inputs */}
            <div className="space-y-4">
              <h3 className="text-xl font-medium text-blue-200 mb-4">Game Context</h3>
              
              <div>
                <label className="block text-sm font-medium mb-2">Hand Strength</label>
                <select
                  name="handStrength"
                  value={formData.handStrength}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white"
                >
                  <option value="weak">Weak</option>
                  <option value="medium">Medium</option>
                  <option value="strong">Strong</option>
                  <option value="nuts">Nuts</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Position</label>
                <select
                  name="position"
                  value={formData.position}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white"
                >
                  <option value="early">Early</option>
                  <option value="middle">Middle</option>
                  <option value="late">Late</option>
                  <option value="blinds">Blinds</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Street</label>
                <select
                  name="street"
                  value={formData.street}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white"
                >
                  <option value="preflop">Preflop</option>
                  <option value="flop">Flop</option>
                  <option value="turn">Turn</option>
                  <option value="river">River</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Your Stack ($)</label>
                <input
                  type="number"
                  name="stackSize"
                  value={formData.stackSize}
                  onChange={handleInputChange}
                  placeholder="1000"
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 text-white placeholder-gray-300"
                />
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 mt-8 justify-center">
            <button
              type="submit"
              className="calculate-btn px-8 py-4 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105"
            >
              🧮 Calculate
            </button>
            
            <button
              type="button"
              className="reset-btn px-8 py-4 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105"
            >
              🔄 Reset
            </button>
          </div>
        </form>
        </div>

        {/* Results Container */}
        <div className="results-container bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20" style={{ display: 'none' }}>
          {/* Results will be dynamically inserted here by main.js */}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-blue-200 text-sm">
          <p>Pot Logic - Advanced Poker Analysis Tool</p>
          <p className="mt-2">Use this tool to make informed poker decisions</p>
        </div>
      </div>
    </div>
  );
};

export default PokerBot; 