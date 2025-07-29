import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { PotOddsCalculator } from './pages/PotOddsCalculator'
import { HandEvaluator } from './pages/HandEvaluator'
import { Statistics } from './pages/Statistics'
import { GameHistory } from './pages/GameHistory'
import { Settings } from './pages/Settings'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/pot-odds" element={<PotOddsCalculator />} />
        <Route path="/hand-evaluator" element={<HandEvaluator />} />
        <Route path="/statistics" element={<Statistics />} />
        <Route path="/history" element={<GameHistory />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  )
}

export default App 