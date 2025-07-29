import React, { useState } from 'react'
import { Calculator, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import toast from 'react-hot-toast'

const potOddsSchema = z.object({
  potSize: z.number().positive('Pot size must be positive'),
  betToCall: z.number().min(0, 'Bet to call must be non-negative'),
  playerCards: z.array(z.string()).length(2, 'Must have exactly 2 hole cards'),
  communityCards: z.array(z.string()).optional(),
  position: z.enum(['early', 'middle', 'cutoff', 'button', 'small_blind', 'big_blind', 'unknown']),
  numPlayers: z.number().min(2).max(10),
})

type PotOddsFormData = z.infer<typeof potOddsSchema>

interface PotOddsResult {
  pot_odds_ratio: number
  pot_odds_percentage: number
  implied_odds: number
  equity: number
  expected_value: number
  is_profitable: boolean
  recommendation: string
  break_even_equity: number
}

export function PotOddsCalculator() {
  const [result, setResult] = useState<PotOddsResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<PotOddsFormData>({
    resolver: zodResolver(potOddsSchema),
    defaultValues: {
      potSize: 0,
      betToCall: 0,
      playerCards: ['', ''],
      communityCards: [],
      position: 'unknown',
      numPlayers: 2,
    },
  })

  const onSubmit = async (data: PotOddsFormData) => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/calculate-pot-odds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      if (!response.ok) {
        throw new Error('Failed to calculate pot odds')
      }

      const result = await response.json()
      setResult(result)
      toast.success('Pot odds calculated successfully!')
    } catch (error) {
      console.error('Error calculating pot odds:', error)
      toast.error('Failed to calculate pot odds')
    } finally {
      setIsLoading(false)
    }
  }

  const watchedValues = watch()

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Pot Odds Calculator</h1>
        <p className="mt-2 text-gray-600">
          Calculate pot odds, implied odds, and get playing recommendations
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Game Information</h2>
          
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Pot and Bet Information */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label className="label">Pot Size ($)</label>
                <input
                  type="number"
                  step="0.01"
                  className="input"
                  {...register('potSize', { valueAsNumber: true })}
                />
                {errors.potSize && (
                  <p className="mt-1 text-sm text-danger-600">{errors.potSize.message}</p>
                )}
              </div>

              <div>
                <label className="label">Bet to Call ($)</label>
                <input
                  type="number"
                  step="0.01"
                  className="input"
                  {...register('betToCall', { valueAsNumber: true })}
                />
                {errors.betToCall && (
                  <p className="mt-1 text-sm text-danger-600">{errors.betToCall.message}</p>
                )}
              </div>
            </div>

            {/* Player Cards */}
            <div>
              <label className="label">Your Hole Cards</label>
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="e.g., Ah"
                  className="input"
                  {...register('playerCards.0')}
                />
                <input
                  type="text"
                  placeholder="e.g., Kd"
                  className="input"
                  {...register('playerCards.1')}
                />
              </div>
              {errors.playerCards && (
                <p className="mt-1 text-sm text-danger-600">{errors.playerCards.message}</p>
              )}
            </div>

            {/* Community Cards */}
            <div>
              <label className="label">Community Cards (Optional)</label>
              <div className="grid grid-cols-5 gap-2">
                {[0, 1, 2, 3, 4].map((index) => (
                  <input
                    key={index}
                    type="text"
                    placeholder={`Card ${index + 1}`}
                    className="input"
                    {...register(`communityCards.${index}`)}
                  />
                ))}
              </div>
            </div>

            {/* Position and Players */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <label className="label">Position</label>
                <select className="input" {...register('position')}>
                  <option value="unknown">Unknown</option>
                  <option value="early">Early</option>
                  <option value="middle">Middle</option>
                  <option value="cutoff">Cutoff</option>
                  <option value="button">Button</option>
                  <option value="small_blind">Small Blind</option>
                  <option value="big_blind">Big Blind</option>
                </select>
              </div>

              <div>
                <label className="label">Number of Players</label>
                <select className="input" {...register('numPlayers', { valueAsNumber: true })}>
                  {[2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                    <option key={num} value={num}>
                      {num} players
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full"
            >
              {isLoading ? 'Calculating...' : 'Calculate Pot Odds'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="space-y-6">
          {result && (
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Analysis Results</h2>
              
              <div className="space-y-4">
                {/* Pot Odds */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-500">Pot Odds</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {result.pot_odds_percentage.toFixed(1)}%
                    </p>
                  </div>
                  <Calculator className="h-8 w-8 text-primary-600" />
                </div>

                {/* Equity */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-500">Hand Equity</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {result.equity.toFixed(1)}%
                    </p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-success-600" />
                </div>

                {/* Expected Value */}
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-500">Expected Value</p>
                    <p className={`text-2xl font-bold ${
                      result.expected_value >= 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      ${result.expected_value.toFixed(2)}
                    </p>
                  </div>
                  {result.expected_value >= 0 ? (
                    <CheckCircle className="h-8 w-8 text-success-600" />
                  ) : (
                    <AlertCircle className="h-8 w-8 text-danger-600" />
                  )}
                </div>

                {/* Recommendation */}
                <div className="p-4 bg-primary-50 rounded-lg">
                  <p className="text-sm font-medium text-primary-900 mb-2">Recommendation</p>
                  <p className="text-lg font-semibold text-primary-900">
                    {result.recommendation}
                  </p>
                </div>

                {/* Additional Info */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Implied Odds</p>
                    <p className="text-lg font-semibold text-gray-900">
                      ${result.implied_odds.toFixed(2)}
                    </p>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Break-even Equity</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {result.break_even_equity.toFixed(1)}%
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Quick Reference */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Reference</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Pot Odds &gt; Equity</span>
                <span className="font-medium text-danger-600">Fold</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Pot Odds &lt; Equity</span>
                <span className="font-medium text-success-600">Call</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">High Implied Odds</span>
                <span className="font-medium text-success-600">Call</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Position Matters</span>
                <span className="font-medium text-warning-600">Consider</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 