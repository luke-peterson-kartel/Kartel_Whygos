import { ReactNode } from 'react'

interface SplitViewLayoutProps {
  leftPanel: ReactNode
  rightPanel: ReactNode
}

export function SplitViewLayout({ leftPanel, rightPanel }: SplitViewLayoutProps) {
  return (
    <div className="max-w-[1600px] mx-auto px-6 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-6">
        {/* Left Panel: My Goals */}
        <div className="space-y-4 md:pr-6 md:border-r md:border-gray-200">
          {leftPanel}
        </div>

        {/* Right Panel: Leadership Context */}
        <div className="space-y-4 md:pl-6">
          {rightPanel}
        </div>
      </div>
    </div>
  )
}
