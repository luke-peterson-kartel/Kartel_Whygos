import { ReactNode } from 'react'

interface DashboardCardProps {
  title?: string
  children: ReactNode
  action?: ReactNode
  className?: string
}

export function DashboardCard({ title, children, action, className = '' }: DashboardCardProps) {
  return (
    <div className={`bg-white rounded-lg border border-gray-200 p-4 ${className}`}>
      {(title || action) && (
        <div className="flex items-center justify-between mb-3">
          {title && <h3 className="text-sm font-semibold text-gray-900">{title}</h3>}
          {action}
        </div>
      )}
      <div className="space-y-3">{children}</div>
    </div>
  )
}
