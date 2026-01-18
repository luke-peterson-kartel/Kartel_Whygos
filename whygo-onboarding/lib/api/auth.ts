import { api } from './client'
import { LoginResponse, Person } from '../types/api'

export async function login(email: string): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>('/api/auth/login', { email })

  // Store token in localStorage
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', response.access_token)
    localStorage.setItem('person_id', response.person_id)
    localStorage.setItem('person_name', response.name)
    localStorage.setItem('person_level', response.level)
  }

  return response
}

export function logout() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('person_id')
    localStorage.removeItem('person_name')
    localStorage.removeItem('person_level')
  }
}

export function getStoredAuth() {
  if (typeof window === 'undefined') {
    return {
      token: null,
      personId: null,
      personName: null,
      personLevel: null,
    }
  }

  return {
    token: localStorage.getItem('auth_token'),
    personId: localStorage.getItem('person_id'),
    personName: localStorage.getItem('person_name'),
    personLevel: localStorage.getItem('person_level'),
  }
}

export async function getCurrentUser(): Promise<Person> {
  return api.get<Person>('/api/users/me')
}
