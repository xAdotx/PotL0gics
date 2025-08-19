# Pot Logic Poker Bot - Frontend

## 🚀 New Features with main.js

The application now includes a comprehensive `main.js` utility that handles:

### ✅ **Form Submissions**
- Automatically listens for form submissions with class `poker-form`
- Validates required fields before sending to API
- Shows loading states and success/error messages

### ✅ **Backend API Integration**
- Sends form data to your backend API endpoints
- Configurable API base URL (default: `http://localhost:5000`)
- Handles different form types (pot odds, hand evaluator, general calculator)

### ✅ **Dynamic Results Display**
- Automatically displays API results in the HTML
- Beautiful, responsive results layout
- Scrolls to results after calculation

### ✅ **Service Worker Registration**
- Registers `sw.js` for PWA functionality
- Handles updates and notifications
- Provides offline capabilities

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```bash
# Backend API URL
REACT_APP_API_URL=http://localhost:5000

# Development settings
REACT_APP_DEBUG=true
REACT_APP_LOG_LEVEL=info
```

### Backend API Endpoints
The main.js expects these endpoints:

- `/api/calculate-odds` - General poker calculations
- `/api/evaluate-hand` - Hand strength evaluation
- `/api/pot-odds` - Pot odds calculations
- `/api/game-history` - Save game history

## 📱 How It Works

### 1. **Form Setup**
Add the `poker-form` class to your forms:
```html
<form class="poker-form">
  <!-- form fields -->
  <button type="submit" class="calculate-btn">Calculate</button>
  <button type="button" class="reset-btn">Reset</button>
</form>
```

### 2. **Results Container**
Add a results container:
```html
<div class="results-container">
  <!-- Results will be dynamically inserted here -->
</div>
```

### 3. **Automatic Functionality**
- Forms are automatically handled
- Results are displayed automatically
- Service worker is registered automatically
- Game history is saved automatically

## 🎯 API Response Format

Your backend should return data in this format:

```json
{
  "potOdds": 33.33,
  "equity": 32.0,
  "expectedValue": -5.50,
  "recommendation": "FOLD - Negative expected value",
  "breakEvenPercentage": 33.33
}
```

## 🔍 Debugging

Check the browser console for:
- ✅ Service Worker registration status
- 🔄 API request/response logs
- ❌ Error messages and validation issues

## 🚀 Getting Started

1. **Start your backend server** (e.g., on port 5000)
2. **Set environment variables** in `.env` file
3. **Run the frontend**: `npm run dev`
4. **Navigate to** `/poker-bot`
5. **Fill out the form** and click Calculate
6. **View results** automatically displayed

## 📚 Additional Features

- **Game History**: Automatically saved to localStorage and backend
- **Session Management**: Unique session IDs for tracking
- **Update Notifications**: Service worker update alerts
- **Responsive Design**: Works on all device sizes
- **Offline Support**: PWA functionality with service worker

## 🛠️ Customization

You can extend the main.js functionality by:
- Adding new API endpoints
- Customizing result display templates
- Adding new form validation rules
- Implementing additional notification types

The system is designed to be modular and easily extensible! 