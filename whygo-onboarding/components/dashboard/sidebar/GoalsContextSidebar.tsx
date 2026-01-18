'use client'

import { useCompanyGoals, useMyDepartmentGoals } from '@/lib/api/queries'
import { CompanyGoalItem } from './CompanyGoalItem'
import { DepartmentGoalItem } from './DepartmentGoalItem'
import { Loader2, Target, Building2 } from 'lucide-react'
import { useMemo } from 'react'

export function GoalsContextSidebar() {
  const { data: companyGoals, isLoading: loadingCompany } = useCompanyGoals()
  const { data: departmentGoals, isLoading: loadingDept } = useMyDepartmentGoals()

  // Create a mapping of company goal IDs to their numbers
  const companyGoalNumbers = useMemo(() => {
    if (!companyGoals) return {}
    return companyGoals.reduce((acc, goal, idx) => {
      acc[goal.id] = idx + 1
      return acc
    }, {} as Record<string, number>)
  }, [companyGoals])

  const isLoading = loadingCompany || loadingDept

  return (
    <div className="w-64 border-r border-gray-200 bg-white flex flex-col h-full">
      {/* Sidebar Header */}
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-sm font-bold text-gray-900">Goals Context</h2>
        <p className="text-xs text-gray-500 mt-1">Company & Department</p>
      </div>

      {/* Sidebar Content */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
          </div>
        ) : (
          <div className="space-y-4 py-4">
            {/* Company WhyGOs Section */}
            <div>
              <div className="px-4 pb-2 flex items-center gap-2">
                <Target className="w-4 h-4 text-blue-600" />
                <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">
                  Company WhyGOs
                </h3>
              </div>
              <div className="bg-white">
                {companyGoals && companyGoals.length > 0 ? (
                  companyGoals.map((goal, idx) => (
                    <CompanyGoalItem
                      key={goal.id}
                      goal={goal}
                      number={idx + 1}
                    />
                  ))
                ) : (
                  <div className="px-4 py-3 text-xs text-gray-500">
                    No company goals found
                  </div>
                )}
              </div>
            </div>

            {/* Department Goals Section */}
            <div>
              <div className="px-4 pb-2 flex items-center gap-2">
                <Building2 className="w-4 h-4 text-green-600" />
                <h3 className="text-xs font-semibold text-gray-700 uppercase tracking-wide">
                  Your Department
                </h3>
              </div>
              <div className="bg-white">
                {departmentGoals && departmentGoals.length > 0 ? (
                  departmentGoals.map((goal) => (
                    <DepartmentGoalItem
                      key={goal.id}
                      goal={goal}
                      companyGoalNumbers={companyGoalNumbers}
                    />
                  ))
                ) : (
                  <div className="px-4 py-3 text-xs text-gray-500">
                    No department goals found
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Sidebar Footer - Optional */}
      <div className="p-3 border-t border-gray-200 bg-gray-50">
        <p className="text-xs text-gray-500 text-center">
          2026 WhyGO Goals
        </p>
      </div>
    </div>
  )
}
