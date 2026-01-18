/**
 * React Query hooks for data fetching
 */

import { useQuery } from '@tanstack/react-query'
import { getMyGoals, getPendingApprovals, getCompanyGoals, getMyDepartmentGoals } from './goals'
import { getOnboardingContext } from './onboarding'
import { IndividualGoal, OnboardingContext, CompanyGoal, DepartmentGoal } from '../types/api'

/**
 * Fetch current user's goals
 */
export function useMyGoals(initialData?: IndividualGoal[]) {
  return useQuery({
    queryKey: ['myGoals'],
    queryFn: getMyGoals,
    initialData,
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}

/**
 * Fetch pending approvals (for managers/executives)
 */
export function usePendingApprovals(initialData?: IndividualGoal[]) {
  return useQuery({
    queryKey: ['pendingApprovals'],
    queryFn: getPendingApprovals,
    initialData,
    staleTime: 1000 * 60 * 2, // 2 minutes (more frequent updates for approvals)
  })
}

/**
 * Fetch onboarding context (includes user, department, company goals, etc.)
 */
export function useOnboardingContext(initialData?: OnboardingContext) {
  return useQuery({
    queryKey: ['onboardingContext'],
    queryFn: getOnboardingContext,
    initialData,
    staleTime: 1000 * 60 * 10, // 10 minutes (context doesn't change often)
  })
}

export function useCompanyGoals(initialData?: CompanyGoal[]) {
  return useQuery({
    queryKey: ['companyGoals'],
    queryFn: getCompanyGoals,
    initialData,
    staleTime: 1000 * 60 * 30, // 30 minutes (company goals rarely change)
  })
}

export function useMyDepartmentGoals(initialData?: DepartmentGoal[]) {
  return useQuery({
    queryKey: ['myDepartmentGoals'],
    queryFn: getMyDepartmentGoals,
    initialData,
    staleTime: 1000 * 60 * 15, // 15 minutes
  })
}
