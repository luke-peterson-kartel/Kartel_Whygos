import { TeamMemberCard } from './TeamMemberCard'
import { StatusType } from '@/lib/utils/status'

interface TeamMember {
  id: string
  name: string
  title: string
  goalsCount: number
  totalGoals: number
  status: StatusType
}

interface TeamMemberListProps {
  members: TeamMember[]
  emptyMessage?: string
}

export function TeamMemberList({ members, emptyMessage = 'No team members found' }: TeamMemberListProps) {
  if (members.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 text-sm">
        {emptyMessage}
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {members.map((member) => (
        <TeamMemberCard
          key={member.id}
          name={member.name}
          title={member.title}
          goalsCount={member.goalsCount}
          totalGoals={member.totalGoals}
          status={member.status}
        />
      ))}
    </div>
  )
}
