import { redirect } from 'next/navigation'
import { cookies } from 'next/headers'
import DashboardView from './DashboardView'
import { api } from '@/lib/api/client'
import { Person } from '@/lib/types/api'
import { Button } from '@/components/ui/button'
import { LogOut } from 'lucide-react'
import Link from 'next/link'

async function getCurrentUser(token: string): Promise<Person | null> {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) return null
    return await response.json()
  } catch (error) {
    return null
  }
}

export default async function DashboardPage() {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    redirect('/')
  }

  const user = await getCurrentUser(token)

  if (!user) {
    redirect('/')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b h-16">
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
            <form action="/api/auth/logout" method="POST">
              <Button variant="ghost" size="sm" type="submit">
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </form>
          </div>
        </div>
      </header>

      {/* Dashboard Content */}
      <DashboardView user={user} />
    </div>
  )
}
