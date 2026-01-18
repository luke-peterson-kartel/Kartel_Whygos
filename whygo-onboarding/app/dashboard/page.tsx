'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import DashboardView from './DashboardView'
import { Person } from '@/lib/types/api'
import { Button } from '@/components/ui/button'
import { LogOut, Loader2 } from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<Person | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadUser()
  }, [])

  const loadUser = async () => {
    try {
      const token = localStorage.getItem('auth_token')

      if (!token) {
        router.push('/')
        return
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/users/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (!response.ok) {
        localStorage.removeItem('auth_token')
        router.push('/')
        return
      }

      const userData = await response.json()
      setUser(userData)
    } catch (error) {
      console.error('Failed to load user:', error)
      localStorage.removeItem('auth_token')
      router.push('/')
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    router.push('/')
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b h-16 flex-shrink-0">
        <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
            <span className="text-sm text-gray-600">
              {user.name} • {user.title}
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/onboarding/profile">
              <Button variant="ghost" size="sm">
                View Profile
              </Button>
            </Link>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Dashboard Content */}
      <div className="flex-1 overflow-hidden">
        <DashboardView user={user} />
      </div>
    </div>
  )
}
