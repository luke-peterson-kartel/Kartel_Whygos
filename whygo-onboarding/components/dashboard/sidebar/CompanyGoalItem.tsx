'use client'

import { CompanyGoal } from '@/lib/types/api'
import { ChevronRight, ChevronDown } from 'lucide-react'
import { useState } from 'react'

interface CompanyGoalItemProps {
  goal: CompanyGoal
  number: number
}

export function CompanyGoalItem({ goal, number }: CompanyGoalItemProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  // Extract the goal title (first part before details)
  const goalTitle = goal.goal.length > 60
    ? goal.goal.substring(0, 60) + '...'
    : goal.goal

  return (
    <div className="border-b border-gray-100 last:border-0">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-3 py-2 flex items-start hover:bg-gray-50 transition-colors text-left"
      >
        <span className="flex-shrink-0 mt-0.5">
          {isExpanded ? (
            <ChevronDown className="w-4 h-4 text-gray-400" />
          ) : (
            <ChevronRight className="w-4 h-4 text-gray-400" />
          )}
        </span>
        <div className="ml-2 flex-1 min-w-0">
          <div className="text-sm font-medium text-gray-900">
            #{number}: {goalTitle}
          </div>
        </div>
      </button>

      {isExpanded && (
        <div className="px-3 py-2 ml-6 bg-gray-50 border-t border-gray-100">
          <div className="space-y-3">
            <div>
              <h4 className="text-xs font-semibold text-gray-700 mb-1">WHY</h4>
              <p className="text-xs text-gray-600 leading-relaxed">{goal.why}</p>
            </div>

            <div>
              <h4 className="text-xs font-semibold text-gray-700 mb-1">GOAL</h4>
              <p className="text-xs text-gray-600 leading-relaxed">{goal.goal}</p>
            </div>

            {goal.outcomes && goal.outcomes.length > 0 && (
              <div>
                <h4 className="text-xs font-semibold text-gray-700 mb-2">OUTCOMES</h4>
                <div className="space-y-1.5">
                  {goal.outcomes.map((outcome, idx) => (
                    <div key={outcome.id} className="text-xs text-gray-600">
                      <span className="font-medium">{idx + 1}.</span> {outcome.description}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
