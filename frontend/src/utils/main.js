// Main.js - Core functionality for Pot Logic Poker Bot
// Handles form submissions, API communication, and service worker registration

class PokerBotAPI {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
    this.endpoints = {
      calculateOdds: '/api/calculate-odds',
      evaluateHand: '/api/evaluate-hand',
      potOdds: '/api/pot-odds',
      gameHistory: '/api/game-history'
    };
    
    this.init();
  }

  init() {
    this.registerServiceWorker();
    this.setupEventListeners();
    this.loadGameHistory();
  }

  // Register Service Worker for PWA functionality
  async registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js', {
          scope: '/'
        });
        
        console.log('✅ Service Worker registered successfully:', registration);
        
        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                console.log('🔄 New service worker available. Refresh to update.');
                this.showUpdateNotification();
              }
            });
          }
        });
        
        // Handle service worker updates
        let refreshing = false;
        navigator.serviceWorker.addEventListener('controllerchange', () => {
          if (!refreshing) {
            refreshing = true;
            window.location.reload();
          }
        });
        
      } catch (registrationError) {
        console.error('❌ Service Worker registration failed:', registrationError);
      }
    } else {
      console.warn('⚠️ Service Worker not supported in this browser');
    }
  }

  // Setup global event listeners
  setupEventListeners() {
    // Listen for form submissions
    document.addEventListener('submit', (e) => {
      if (e.target.classList.contains('poker-form')) {
        e.preventDefault();
        this.handleFormSubmission(e.target);
      }
    });

    // Listen for calculate button clicks
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('calculate-btn')) {
        e.preventDefault();
        this.handleCalculateClick(e.target);
      }
    });

    // Listen for reset button clicks
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('reset-btn')) {
        e.preventDefault();
        this.handleResetClick(e.target);
      }
    });

    // Listen for navigation changes (for SPA routing)
    window.addEventListener('popstate', () => {
      this.updateActiveNavigation();
    });
  }

  // Handle form submissions
  async handleFormSubmission(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Validate required fields
    if (!this.validateFormData(data)) {
      this.showError('Please fill in all required fields');
      return;
    }

    // Show loading state
    this.showLoading(true);
    
    try {
      // Determine which API endpoint to use based on form type
      const endpoint = this.getEndpointForForm(form);
      const response = await this.sendAPIRequest(endpoint, data);
      
      // Display results
      this.displayResults(response);
      
      // Save to game history
      this.saveToGameHistory(data, response);
      
      // Show success message
      this.showSuccess('Calculation completed successfully!');
      
    } catch (error) {
      console.error('API Error:', error);
      this.showError('Failed to calculate odds. Please try again.');
    } finally {
      this.showLoading(false);
    }
  }

  // Handle calculate button clicks
  async handleCalculateClick(button) {
    const form = button.closest('form') || button.closest('.poker-form');
    if (form) {
      await this.handleFormSubmission(form);
    }
  }

  // Handle reset button clicks
  handleResetClick(button) {
    const form = button.closest('form') || button.closest('.poker-form');
    if (form) {
      form.reset();
      this.clearResults();
      this.showSuccess('Form reset successfully');
    }
  }

  // Validate form data
  validateFormData(data) {
    const required = ['potSize', 'betSize', 'callAmount'];
    return required.every(field => data[field] && data[field].trim() !== '');
  }

  // Get appropriate API endpoint for form type
  getEndpointForForm(form) {
    if (form.classList.contains('pot-odds-form')) {
      return this.endpoints.potOdds;
    } else if (form.classList.contains('hand-evaluator-form')) {
      return this.endpoints.evaluateHand;
    } else {
      return this.endpoints.calculateOdds;
    }
  }

  // Send API request to backend
  async sendAPIRequest(endpoint, data) {
    const url = `${this.baseURL}${endpoint}`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  // Display calculation results
  displayResults(results) {
    // Clear previous results
    this.clearResults();
    
    // Find results container
    const resultsContainer = document.querySelector('.results-container') || 
                           document.querySelector('[data-results]');
    
    if (!resultsContainer) {
      console.warn('Results container not found');
      return;
    }

    // Create results HTML
    const resultsHTML = this.createResultsHTML(results);
    
    // Display results
    resultsContainer.innerHTML = resultsHTML;
    resultsContainer.style.display = 'block';
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
  }

  // Create HTML for results display
  createResultsHTML(results) {
    return `
      <div class="results-display">
        <h2 class="text-2xl font-semibold mb-6 text-center text-green-300">Results</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="bg-gradient-to-br from-blue-600/30 to-blue-800/30 p-4 rounded-xl border border-blue-400/30">
            <h3 class="text-lg font-medium text-blue-200 mb-2">Pot Odds</h3>
            <p class="text-3xl font-bold text-blue-100">${results.potOdds || 0}%</p>
            <p class="text-sm text-blue-300">Required equity to call</p>
          </div>

          <div class="bg-gradient-to-br from-green-600/30 to-green-800/30 p-4 rounded-xl border border-green-400/30">
            <h3 class="text-lg font-medium text-green-200 mb-2">Hand Equity</h3>
            <p class="text-3xl font-bold text-green-100">${results.equity || 0}%</p>
            <p class="text-sm text-green-300">Your winning probability</p>
          </div>

          <div class="bg-gradient-to-br from-purple-600/30 to-purple-800/30 p-4 rounded-xl border border-purple-400/30">
            <h3 class="text-lg font-medium text-purple-200 mb-2">Expected Value</h3>
            <p class="text-3xl font-bold text-purple-100">$${results.expectedValue || 0}</p>
            <p class="text-sm text-purple-300">Long-term profit/loss</p>
          </div>
        </div>

        <div class="mt-6 p-4 bg-gradient-to-r from-yellow-600/20 to-orange-600/20 rounded-xl border border-yellow-400/30">
          <h3 class="text-xl font-semibold text-yellow-200 mb-2">Recommendation</h3>
          <p class="text-2xl font-bold text-yellow-100">${results.recommendation || 'No recommendation'}</p>
          <p class="text-sm text-yellow-300 mt-2">
            Break-even percentage: ${results.breakEvenPercentage || 0}%
          </p>
        </div>

        <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-white/5 p-4 rounded-lg">
            <h4 class="font-medium text-blue-200 mb-2">Analysis</h4>
            <ul class="text-sm text-gray-300 space-y-1">
              <li>• Pot odds: ${results.potOdds || 0}%</li>
              <li>• Hand equity: ${results.equity || 0}%</li>
              <li>• Break-even: ${results.breakEvenPercentage || 0}%</li>
              <li>• EV: $${results.expectedValue || 0}</li>
            </ul>
          </div>

          <div class="bg-white/5 p-4 rounded-lg">
            <h4 class="font-medium text-green-200 mb-2">Strategy</h4>
            <ul class="text-sm text-gray-300 space-y-1">
              <li>• ${(results.equity || 0) > (results.potOdds || 0) ? '✅ Profitable call' : '❌ Unprofitable call'}</li>
              <li>• ${(results.equity || 0) > 50 ? '✅ Strong hand' : '⚠️ Weak hand'}</li>
              <li>• ${(results.expectedValue || 0) > 0 ? '✅ +EV decision' : '❌ -EV decision'}</li>
            </ul>
          </div>
        </div>
      </div>
    `;
  }

  // Clear previous results
  clearResults() {
    const resultsContainer = document.querySelector('.results-container') || 
                           document.querySelector('[data-results]');
    
    if (resultsContainer) {
      resultsContainer.innerHTML = '';
      resultsContainer.style.display = 'none';
    }
  }

  // Show loading state
  showLoading(show) {
    const buttons = document.querySelectorAll('.calculate-btn');
    buttons.forEach(button => {
      if (show) {
        button.disabled = true;
        button.innerHTML = '🔄 Calculating...';
        button.classList.add('opacity-50');
      } else {
        button.disabled = false;
        button.innerHTML = '🧮 Calculate';
        button.classList.remove('opacity-50');
      }
    });
  }

  // Show success message
  showSuccess(message) {
    this.showNotification(message, 'success');
  }

  // Show error message
  showError(message) {
    this.showNotification(message, 'error');
  }

  // Show notification
  showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
      type === 'success' ? 'bg-green-500 text-white' :
      type === 'error' ? 'bg-red-500 text-white' :
      'bg-blue-500 text-white'
    }`;
    
    notification.innerHTML = `
      <div class="flex items-center">
        <span class="mr-2">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
        <span>${message}</span>
      </div>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 3000);
  }

  // Show update notification
  showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'fixed bottom-4 right-4 p-4 bg-blue-500 text-white rounded-lg shadow-lg z-50';
    notification.innerHTML = `
      <div class="flex items-center justify-between">
        <span>🔄 New version available</span>
        <button onclick="window.location.reload()" class="ml-4 px-3 py-1 bg-white text-blue-500 rounded text-sm">
          Update
        </button>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 10 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 10000);
  }

  // Save calculation to game history
  async saveToGameHistory(inputData, results) {
    try {
      const historyData = {
        timestamp: new Date().toISOString(),
        input: inputData,
        results: results,
        sessionId: this.getSessionId()
      };
      
      // Save to localStorage for now (can be extended to backend)
      const history = JSON.parse(localStorage.getItem('pokerGameHistory') || '[]');
      history.unshift(historyData);
      
      // Keep only last 100 entries
      if (history.length > 100) {
        history.splice(100);
      }
      
      localStorage.setItem('pokerGameHistory', JSON.stringify(history));
      
      // Also try to save to backend
      await this.sendAPIRequest(this.endpoints.gameHistory, historyData);
      
    } catch (error) {
      console.warn('Failed to save to backend history:', error);
      // Continue with localStorage only
    }
  }

  // Load game history
  loadGameHistory() {
    try {
      const history = JSON.parse(localStorage.getItem('pokerGameHistory') || '[]');
      this.updateHistoryDisplay(history);
    } catch (error) {
      console.warn('Failed to load game history:', error);
    }
  }

  // Update history display
  updateHistoryDisplay(history) {
    const historyContainer = document.querySelector('.game-history-container');
    if (!historyContainer) return;
    
    if (history.length === 0) {
      historyContainer.innerHTML = '<p class="text-gray-500">No games played yet</p>';
      return;
    }
    
    const historyHTML = history.slice(0, 5).map(entry => `
      <div class="flex items-center justify-between p-3 border-b border-gray-200">
        <div>
          <p class="font-medium text-gray-900">${entry.results.recommendation || 'Calculation'}</p>
          <p class="text-sm text-gray-500">Pot: $${entry.input.potSize || 0}</p>
        </div>
        <span class="text-sm text-gray-500">${this.formatTimestamp(entry.timestamp)}</span>
      </div>
    `).join('');
    
    historyContainer.innerHTML = historyHTML;
  }

  // Format timestamp
  formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  }

  // Get or create session ID
  getSessionId() {
    let sessionId = localStorage.getItem('pokerSessionId');
    if (!sessionId) {
      sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('pokerSessionId', sessionId);
    }
    return sessionId;
  }

  // Update active navigation
  updateActiveNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }
}

// Initialize the PokerBot API when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.pokerBotAPI = new PokerBotAPI();
});

// Export for use in other modules
export default PokerBotAPI; 