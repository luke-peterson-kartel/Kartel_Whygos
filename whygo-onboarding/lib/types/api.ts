export interface Person {
  id: string
  name: string
  title: string
  email: string | null
  department_id: string
  manager_id: string | null
  level: 'executive' | 'department_head' | 'manager' | 'ic'
  employment_type: 'w2' | 'contractor' | 'international' | 'trial'
  status: 'active' | 'trial' | 'searching'
  onboarding_status: 'not_started' | 'in_progress' | 'completed'
  last_login: string | null
  timezone: string
  notification_enabled: boolean
}

export interface Department {
  id: string
  name: string
  head_id: string
  primary_company_goal_ids: string[]
  secondary_company_goal_ids: string[]
  reports_to: string | null
}

export interface Outcome {
  id: string
  goal_id: string
  description: string
  metric_type: 'number' | 'percentage' | 'currency' | 'boolean' | 'milestone'
  owner_id: string
  target_annual: number | null
  target_q1: number | null
  target_q2: number | null
  target_q3: number | null
  target_q4: number | null
  actual_q1: number | null
  actual_q2: number | null
  actual_q3: number | null
  actual_q4: number | null
  status_q1: string | null
  status_q2: string | null
  status_q3: string | null
  status_q4: string | null
}

export interface CompanyGoal {
  id: string
  why: string
  goal: string
  status: string
  owner_id: string
  fiscal_year: number
  outcomes: Outcome[]
  created_at: string | null
  updated_at: string | null
}

export interface DepartmentGoal {
  id: string
  department_id: string
  parent_goal_ids: string[]
  why: string
  goal: string
  status: string
  approved_by: string | null
  fiscal_year: number
  outcomes: Outcome[]
  created_at: string | null
  updated_at: string | null
}

export interface IndividualGoal {
  id: string
  person_id: string
  parent_goal_ids: string[]
  why: string
  goal: string
  status: string
  approved_by: string | null
  fiscal_year: number
  outcomes: Outcome[]
  created_at: string | null
  updated_at: string | null
}

export interface OnboardingContext {
  person: Person
  department: Department
  manager: Person | null
  company_goals: CompanyGoal[]
  department_goals: DepartmentGoal[]
  individual_goals: IndividualGoal[]
  pending_approvals: IndividualGoal[]
}

export interface LoginResponse {
  access_token: string
  token_type: string
  person_id: string
  name: string
  level: string
}

export interface CreateGoalRequest {
  parent_goal_ids: string[]
  why: string
  goal: string
  outcomes: {
    description: string
    metric_type: string
    owner_id: string
    target_annual: number
    target_q1?: number
    target_q2?: number
    target_q3?: number
    target_q4?: number
  }[]
}
