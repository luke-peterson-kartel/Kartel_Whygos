import { ArrowUp } from 'lucide-react'

interface ConnectionBadgeProps {
  label: string
  type?: 'department' | 'company'
}

export function ConnectionBadge({ label, type = 'department' }: ConnectionBadgeProps) {
  const bgColor = type === 'company' ? 'bg-blue-50' : 'bg-gray-50'
  const textColor = type === 'company' ? 'text-blue-700' : 'text-gray-700'
  const borderColor = type === 'company' ? 'border-blue-200' : 'border-gray-200'

  return (
    <div
      className={`inline-flex items-center space-x-1 px-2 py-1 rounded border ${bgColor} ${textColor} ${borderColor} text-xs`}
    >
      <ArrowUp className="w-3 h-3" />
      <span>{label}</span>
    </div>
  )
}
