import { api } from './client'
import { IndividualGoal, CreateGoalRequest } from '../types/api'

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
