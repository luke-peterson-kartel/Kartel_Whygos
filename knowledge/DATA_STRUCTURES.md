# Data Structures - WhyGO Management System

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   CompanyGoal   │───┐   │ DepartmentGoal  │───┐   │ IndividualGoal  │
│                 │   │   │                 │   │   │                 │
│ - id            │   │   │ - id            │   │   │ - id            │
│ - why           │   │   │ - why           │   │   │ - why           │
│ - goal          │   │   │ - goal          │   │   │ - goal          │
│ - status        │   │   │ - status        │   │   │ - status        │
│ - owner_id      │   │   │ - department_id │   │   │ - person_id     │
│ - fiscal_year   │   │   │ - parent_goal_id│◄──┘   │ - parent_goal_id│◄──┐
└────────┬────────┘   │   └────────┬────────┘       └────────┬────────┘   │
         │            │            │                         │            │
         │ 1:N        │            │ 1:N                     │ 1:N        │
         ▼            │            ▼                         ▼            │
┌─────────────────┐   │   ┌─────────────────┐       ┌─────────────────┐   │
│     Outcome     │   │   │     Outcome     │       │     Outcome     │   │
│                 │   │   │                 │       │                 │   │
│ - id            │   │   │ - id            │       │ - id            │   │
│ - goal_id       │   │   │ - goal_id       │       │ - goal_id       │   │
│ - description   │   │   │ - owner_id      │       │ - owner_id      │   │
│ - target_annual │   │   │ - q1_target     │       │ - q1_actual     │   │
│ - q1/q2/q3/q4   │   │   │ - q1_actual     │       │ - status        │   │
│ - owner_id      │   │   └─────────────────┘       └─────────────────┘   │
└─────────────────┘   │                                                   │
                      │   ┌─────────────────┐       ┌─────────────────┐   │
                      │   │   Department    │       │     Person      │───┘
                      │   │                 │       │                 │
                      │   │ - id            │◄──────│ - department_id │
                      │   │ - name          │       │ - name          │
                      │   │ - head_id       │       │ - title         │
                      │   │ - company_goals │       │ - manager_id    │
                      │   └─────────────────┘       │ - level         │
                      │            ▲                └─────────────────┘
                      │            │
                      └────────────┘
                         (alignment)
```

---

## Core Schemas

### Person

```typescript
interface Person {
  id: string;
  name: string;
  title: string;
  department_id: string;
  manager_id: string | null;  // null for executives
  level: 'executive' | 'department_head' | 'manager' | 'ic';
  email?: string;
  linkedin_url?: string;
  employment_type: 'w2' | 'contractor' | 'international';
  start_date: Date;
  status: 'active' | 'trial' | 'searching';
}
```

### Department

```typescript
interface Department {
  id: string;
  name: string;
  head_id: string;  // Person.id
  primary_company_goal_ids: string[];  // CompanyGoal.id[]
  secondary_company_goal_ids: string[];
  reports_to: string;  // Person.id (typically Luke or Kevin)
}
```

### WhyGO (Base)

```typescript
interface WhyGOBase {
  id: string;
  why: string;  // Max 3 sentences
  goal: string;
  status: 'draft' | 'pending_approval' | 'approved' | 'archived';
  created_at: Date;
  updated_at: Date;
  fiscal_year: number;
}
```

### CompanyWhyGO

```typescript
interface CompanyWhyGO extends WhyGOBase {
  level: 'company';
  owner_id: string;  // CEO
  outcomes: CompanyOutcome[];
}
```

### DepartmentWhyGO

```typescript
interface DepartmentWhyGO extends WhyGOBase {
  level: 'department';
  department_id: string;
  parent_goal_ids: string[];  // CompanyWhyGO.id[]
  approved_by: string | null;  // CEO approval
  outcomes: DepartmentOutcome[];
}
```

### IndividualWhyGO

```typescript
interface IndividualWhyGO extends WhyGOBase {
  level: 'individual';
  person_id: string;
  parent_goal_ids: string[];  // DepartmentWhyGO.id[]
  approved_by: string | null;  // Manager approval
  outcomes: IndividualOutcome[];
}
```

### Outcome

```typescript
interface Outcome {
  id: string;
  goal_id: string;
  description: string;
  metric_type: 'number' | 'percentage' | 'currency' | 'boolean' | 'milestone';
  owner_id: string;
  
  // Targets (set at goal creation)
  target_annual: number | string;
  target_q1: number | string;
  target_q2: number | string;
  target_q3: number | string;
  target_q4: number | string;
  
  // Actuals (updated during tracking)
  actual_q1?: number | string;
  actual_q2?: number | string;
  actual_q3?: number | string;
  actual_q4?: number | string;
  
  // Calculated status
  status_q1?: '+' | '~' | '-' | null;
  status_q2?: '+' | '~' | '-' | null;
  status_q3?: '+' | '~' | '-' | null;
  status_q4?: '+' | '~' | '-' | null;
}
```

### ProgressUpdate

```typescript
interface ProgressUpdate {
  id: string;
  outcome_id: string;
  quarter: 'Q1' | 'Q2' | 'Q3' | 'Q4';
  actual_value: number | string;
  status: '+' | '~' | '-';
  notes?: string;
  blocker?: string;
  recorded_by: string;  // Person.id
  recorded_at: Date;
}
```

---

## Kartel-Specific Data

### 2026 Departments

```json
{
  "departments": [
    {
      "id": "dept_sales",
      "name": "Sales",
      "head_id": "person_ben_kusin",
      "primary_company_goal_ids": ["cg_1_pmf"],
      "secondary_company_goal_ids": ["cg_2_ops"],
      "reports_to": "person_kevin_reilly"
    },
    {
      "id": "dept_production",
      "name": "Production",
      "head_id": "person_wayan_palmieri",
      "primary_company_goal_ids": ["cg_2_ops"],
      "secondary_company_goal_ids": ["cg_1_pmf"],
      "reports_to": "person_luke_peterson"
    },
    {
      "id": "dept_generative",
      "name": "Generative Engineering",
      "head_id": "person_fill_isgro",
      "primary_company_goal_ids": ["cg_2_ops"],
      "secondary_company_goal_ids": ["cg_3_talent", "cg_4_platform"],
      "reports_to": "person_luke_peterson"
    },
    {
      "id": "dept_community",
      "name": "Community & Partnerships",
      "head_id": "person_daniel_kalotov",
      "primary_company_goal_ids": ["cg_3_talent"],
      "secondary_company_goal_ids": ["cg_1_pmf"],
      "reports_to": "person_luke_peterson"
    },
    {
      "id": "dept_platform",
      "name": "Platform Engineering",
      "head_id": "person_niels_hoffmann",
      "primary_company_goal_ids": ["cg_4_platform"],
      "secondary_company_goal_ids": ["cg_2_ops"],
      "reports_to": "person_luke_peterson"
    },
    {
      "id": "dept_management",
      "name": "Management",
      "head_id": "person_kevin_reilly",
      "primary_company_goal_ids": ["cg_1_pmf", "cg_2_ops", "cg_3_talent", "cg_4_platform"],
      "secondary_company_goal_ids": [],
      "reports_to": null
    }
  ]
}
```

### 2026 Employees

```json
{
  "employees": [
    {
      "id": "person_kevin_reilly",
      "name": "Kevin Reilly",
      "title": "CEO",
      "department_id": "dept_management",
      "manager_id": null,
      "level": "executive"
    },
    {
      "id": "person_luke_peterson",
      "name": "Luke Peterson",
      "title": "President & Co-Founder",
      "department_id": "dept_management",
      "manager_id": null,
      "level": "executive"
    },
    {
      "id": "person_ben_kusin",
      "name": "Ben Kusin",
      "title": "CRO & Co-Founder",
      "department_id": "dept_sales",
      "manager_id": "person_kevin_reilly",
      "level": "department_head"
    },
    {
      "id": "person_wayan_palmieri",
      "name": "Wayan Palmieri",
      "title": "SVP, Head of Production",
      "department_id": "dept_production",
      "manager_id": "person_luke_peterson",
      "level": "department_head"
    },
    {
      "id": "person_fill_isgro",
      "name": "Fill Isgro",
      "title": "SVP, Head of Generative Engineering",
      "department_id": "dept_generative",
      "manager_id": "person_luke_peterson",
      "level": "department_head"
    },
    {
      "id": "person_daniel_kalotov",
      "name": "Daniel Kalotov",
      "title": "SVP, Head of Community & Partnerships",
      "department_id": "dept_community",
      "manager_id": "person_luke_peterson",
      "level": "department_head"
    },
    {
      "id": "person_niels_hoffmann",
      "name": "Niels Hoffmann",
      "title": "CTO",
      "department_id": "dept_platform",
      "manager_id": "person_luke_peterson",
      "level": "department_head"
    },
    {
      "id": "person_emmet_reilly",
      "name": "Emmet Reilly",
      "title": "Director of Customer Success",
      "department_id": "dept_sales",
      "manager_id": "person_ben_kusin",
      "level": "manager"
    },
    {
      "id": "person_veronica_diaz",
      "name": "Veronica Diaz",
      "title": "Production Manager",
      "department_id": "dept_production",
      "manager_id": "person_wayan_palmieri",
      "level": "manager"
    },
    {
      "id": "person_estefania_guarderas",
      "name": "Estefania Guarderas",
      "title": "Producer",
      "department_id": "dept_production",
      "manager_id": "person_wayan_palmieri",
      "level": "ic"
    },
    {
      "id": "person_jason_goldwatch",
      "name": "Jason Goldwatch",
      "title": "Director",
      "department_id": "dept_production",
      "manager_id": "person_wayan_palmieri",
      "level": "manager"
    },
    {
      "id": "person_noah_shields",
      "name": "Noah Shields",
      "title": "Associate Producer",
      "department_id": "dept_production",
      "manager_id": "person_veronica_diaz",
      "level": "ic"
    },
    {
      "id": "person_brandon_valedez",
      "name": "Brandon Valedez",
      "title": "Data Training / LoRA Models",
      "department_id": "dept_generative",
      "manager_id": "person_fill_isgro",
      "level": "ic"
    },
    {
      "id": "person_sean_geisterfer",
      "name": "Sean Geisterfer",
      "title": "Data Engineering",
      "department_id": "dept_generative",
      "manager_id": "person_fill_isgro",
      "level": "ic"
    },
    {
      "id": "person_trent_hunter",
      "name": "Trent Hunter",
      "title": "Workflow Engineer",
      "department_id": "dept_generative",
      "manager_id": "person_fill_isgro",
      "level": "ic"
    },
    {
      "id": "person_elliot_quartz",
      "name": "Elliot Quartz",
      "title": "AI Generalist",
      "department_id": "dept_generative",
      "manager_id": "person_fill_isgro",
      "level": "ic"
    },
    {
      "id": "person_marc_donhue",
      "name": "Marc Donhue",
      "title": "Preditor",
      "department_id": "dept_generative",
      "manager_id": "person_fill_isgro",
      "level": "ic"
    },
    {
      "id": "person_ahmed_yakout",
      "name": "Ahmed Yakout",
      "title": "Workflow Engineer - Real Estate",
      "department_id": "dept_generative",
      "manager_id": "person_fill_isgro",
      "level": "ic"
    },
    {
      "id": "person_matthias_thoemmes",
      "name": "Matthias Thoemmes",
      "title": "Full Stack Developer",
      "department_id": "dept_platform",
      "manager_id": "person_niels_hoffmann",
      "level": "ic"
    },
    {
      "id": "person_lukas_motiejunas",
      "name": "Lukas Motiejunas",
      "title": "Full Stack Developer",
      "department_id": "dept_platform",
      "manager_id": "person_niels_hoffmann",
      "level": "ic"
    },
    {
      "id": "person_zac_bagley",
      "name": "Zac Bagley",
      "title": "Backend Engineer",
      "department_id": "dept_platform",
      "manager_id": "person_niels_hoffmann",
      "level": "ic"
    },
    {
      "id": "person_jerry_bellman",
      "name": "Jerry Bellman",
      "title": "CFO (Part-Time)",
      "department_id": "dept_management",
      "manager_id": "person_kevin_reilly",
      "level": "executive"
    }
  ]
}
```

---

## Status Calculation Logic

```typescript
function calculateStatus(actual: number, target: number): '+' | '~' | '-' {
  const percentage = (actual / target) * 100;
  
  if (percentage >= 100) return '+';
  if (percentage >= 80) return '~';
  return '-';
}

function calculateOutcomeStatus(outcome: Outcome, quarter: string): string {
  const actualKey = `actual_${quarter.toLowerCase()}`;
  const targetKey = `target_${quarter.toLowerCase()}`;
  
  const actual = outcome[actualKey];
  const target = outcome[targetKey];
  
  if (actual === undefined || actual === null) return null;
  
  // Handle different metric types
  if (outcome.metric_type === 'boolean') {
    return actual === target ? '+' : '-';
  }
  
  if (outcome.metric_type === 'milestone') {
    // Milestones: check if milestone was reached
    return actual === target ? '+' : '-';
  }
  
  // Numeric types
  return calculateStatus(Number(actual), Number(target));
}
```

---

## Cross-Department Dependencies

### Dependency Types

```typescript
interface Dependency {
  id: string;
  from_department_id: string;
  to_department_id: string;
  description: string;
  deliverable: string;
  timeline: string;
  success_criteria: string;
}
```

### Key Dependencies (2026)

| From | To | Deliverable | Timeline |
|------|-----|-------------|----------|
| Platform | Generative | Community Ecosystem Platform MVP | Q1 |
| Platform | Production | Production Management tools | Q1 |
| Generative | Community | Role playbooks for certification | Q1-Q2 |
| Community | Generative | Tier 5 qualified talent | Q1-Q4 |
| Production | Sales | Closing Reports with case study visuals | Per project |
| Sales | Production | SOW package within 48 hrs | Per deal |

---

## Talent Pipeline (Community Specific)

```typescript
interface TalentTier {
  tier: 1 | 2 | 3 | 4 | 5;
  name: string;
  criteria: string[];
  platform_access: string[];
}

const TALENT_TIERS: TalentTier[] = [
  {
    tier: 1,
    name: "Community Member",
    criteria: ["Joined Discord", "Completed onboarding"],
    platform_access: ["Discord"]
  },
  {
    tier: 2,
    name: "Engaged Learner",
    criteria: ["Completed foundational training", "Active in community"],
    platform_access: ["Discord", "Training modules"]
  },
  {
    tier: 3,
    name: "Skill Verified",
    criteria: ["Passed technical assessment in 1+ role tracks"],
    platform_access: ["Discord", "Training", "Open Generative Platform"]
  },
  {
    tier: 4,
    name: "Trial Contributor",
    criteria: ["Completed supervised trial project", "Quality review passed"],
    platform_access: ["Discord", "Training", "Generative Platform", "Trial projects"]
  },
  {
    tier: 5,
    name: "Approved Kartel Talent",
    criteria: ["Deployed on client work", "Meets quality standards"],
    platform_access: ["Full Production Platform access"]
  }
];

const ROLE_TRACKS = [
  "Workflow Engineer",
  "AI Generalist",
  "Data Specialist",
  "Training Specialist",
  "Preditor"
];
```

---

## Handoff Tracking (Production Specific)

```typescript
interface Handoff {
  id: string;
  type: 'sales_to_production' | 'production_to_generative' | 'generative_to_production' | 'production_to_sales';
  project_id: string;
  from_person_id: string;
  to_person_id: string;
  status: 'pending' | 'complete' | 'blocked';
  due_date: Date;
  completed_date?: Date;
  deliverables: string[];
  notes?: string;
}

const HANDOFF_DEFINITIONS = {
  sales_to_production: {
    name: "Sales → Production",
    deliverables: ["SOW signed", "Milestones defined", "Timeline set", "Staffing plan", "Budget approved"],
    sla_hours: 48
  },
  production_to_generative: {
    name: "Production → Generative",
    deliverables: ["Pod request with specs", "Pod roles defined", "Timeline set", "Deliverable specs", "Brand context"],
    sla_hours: 24
  },
  generative_to_production: {
    name: "Generative → Production",
    deliverables: ["QC-passed assets", "Submitted in platform"],
    sla_hours: null  // Based on project timeline
  },
  production_to_sales: {
    name: "Production → Sales",
    deliverables: ["Closing Report", "Margin data", "Case study visuals", "Use cases for Sales"],
    sla_hours: 72
  }
};
```
