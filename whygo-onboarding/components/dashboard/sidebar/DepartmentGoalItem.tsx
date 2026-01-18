'use client'

import { DepartmentGoal } from '@/lib/types/api'
import { ChevronRight, ChevronDown, ArrowUp } from 'lucide-react'
import { useState } from 'react'

interface DepartmentGoalItemProps {
  goal: DepartmentGoal
  companyGoalNumbers?: Record<string, number>
}

export function DepartmentGoalItem({ goal, companyGoalNumbers }: DepartmentGoalItemProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const goalTitle = goal.goal.length > 50
    ? goal.goal.substring(0, 50) + '...'
    : goal.goal

  // Map parent goal IDs to company goal numbers
  const parentNumbers = goal.parent_goal_ids
    .map(id => companyGoalNumbers?.[id])
    .filter(Boolean)

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
            {goalTitle}
          </div>
          {parentNumbers.length > 0 && (
            <div className="flex items-center gap-1 mt-1">
              <ArrowUp className="w-3 h-3 text-blue-500" />
              <span className="text-xs text-blue-600">
                Company #{parentNumbers.join(', #')}
              </span>
            </div>
          )}
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
