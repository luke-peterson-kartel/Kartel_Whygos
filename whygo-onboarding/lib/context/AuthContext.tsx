'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { login as apiLogin, logout as apiLogout, getStoredAuth } from '../api/auth'
import { Person } from '../types/api'

interface AuthContextType {
  user: Person | null
  isLoading: boolean
  login: (email: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<Person | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check for stored auth on mount
    const { token } = getStoredAuth()
    if (token) {
      // User is logged in, we'll fetch their profile in the onboarding page
      setIsLoading(false)
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string) => {
    try {
      await apiLogin(email)
      router.push('/onboarding/profile')
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    apiLogout()
    setUser(null)
    router.push('/')
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
