import { api } from './client'
import { IndividualGoal, CreateGoalRequest, CompanyGoal, DepartmentGoal } from '../types/api'

export async function getMyGoals(): Promise<IndividualGoal[]> {
  return api.get<IndividualGoal[]>('/api/individuals/me')
}

export async function createGoal(
  goalData: CreateGoalRequest
): Promise<IndividualGoal> {
  return api.post<IndividualGoal>('/api/individuals/create', goalData)
}

export async function approveGoal(goalId: string): Promise<void> {
  await api.post(`/api/individuals/${goalId}/approve`)
}

export async function getPendingApprovals(): Promise<IndividualGoal[]> {
  return api.get<IndividualGoal[]>('/api/individuals/pending-approval')
}

export async function getCompanyGoals(): Promise<CompanyGoal[]> {
  return api.get<CompanyGoal[]>('/api/company/goals')
}

export async function getMyDepartmentGoals(): Promise<DepartmentGoal[]> {
  return api.get<DepartmentGoal[]>('/api/departments/me/goals')
}
