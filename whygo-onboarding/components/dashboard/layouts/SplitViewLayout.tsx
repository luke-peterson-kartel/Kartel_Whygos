import { ReactNode } from 'react'

interface SplitViewLayoutProps {
  leftPanel: ReactNode
  rightPanel: ReactNode
}

export function SplitViewLayout({ leftPanel, rightPanel }: SplitViewLayoutProps) {
  return (
    <div className="flex flex-col lg:flex-row min-h-screen bg-gray-50">
      {/* Left Panel: My Goals */}
      <div className="w-full lg:w-1/2 lg:border-r border-gray-200 px-6 py-6 space-y-4">
        {leftPanel}
      </div>

      {/* Right Panel: Leadership Context */}
      <div className="w-full lg:w-1/2 px-6 py-6 space-y-4">
        {rightPanel}
      </div>
    </div>
  )
}
