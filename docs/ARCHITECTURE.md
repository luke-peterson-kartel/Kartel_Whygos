# WHYGOs System Architecture

**Last Updated**: 2026-01-17

## Overview

The WHYGOs Management System is built with a modern full-stack architecture:
- **Frontend**: Next.js 14 with React Server Components
- **Backend**: FastAPI with Python 3.9+
- **Data**: JSON files (designed for easy database migration)
- **Architecture Pattern**: Repository pattern with clean separation

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Frontend                      │
│                  (localhost:3000)                        │
├─────────────────────────────────────────────────────────┤
│  App Router (RSC)  │  Components  │  React Query        │
│  - Server Pages    │  - Atomic    │  - Data Fetching    │
│  - Client Wrappers │  - Layouts   │  - Caching          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────┐
│                   FastAPI Backend                        │
│                  (localhost:8000)                        │
├─────────────────────────────────────────────────────────┤
│  Routers  │  Services  │  Models  │  Repositories       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   JSON Data Store                        │
│  company_whygos.json  │  department_goals.json          │
│  individual_goals.json │ progress_updates.json          │
└─────────────────────────────────────────────────────────┘
```

## Frontend Architecture (Next.js 14)

### 1. Server Components First

**Philosophy**: Maximize server-side rendering for performance

```typescript
// app/dashboard/page.tsx - SERVER COMPONENT
export default async function DashboardPage() {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value
  const user = await getCurrentUser(token) // Server-side fetch
  return <DashboardView user={user} />
}
```

**Benefits**:
- 30-50% faster initial load
- Smaller JavaScript bundle
- Better SEO
- Reduced client-side API calls

### 2. Atomic Component Design

**Component Structure**:
```
components/dashboard/
├── primitives/           # 4 atomic components
│   ├── StatusDot.tsx     # Single responsibility
│   ├── ConnectionBadge.tsx
│   ├── QuarterBadge.tsx
│   └── ProgressBar.tsx
├── layouts/              # 2 layout components
│   ├── DashboardCard.tsx
│   └── SplitViewLayout.tsx
├── goals/                # 6 goal components
│   ├── GoalHeader.tsx
│   ├── GoalProgress.tsx
│   ├── GoalConnections.tsx
│   ├── GoalActions.tsx
│   ├── GoalCard.tsx      # Composed from above
│   └── GoalList.tsx
├── team/                 # 2 team components
├── approvals/            # 2 approval components
└── containers/           # 4 smart components
    ├── MyGoalsContainer.tsx
    ├── TeamProgressContainer.tsx
    ├── ApprovalsContainer.tsx
    └── LeadershipContainer.tsx
```

**Principles**:
- Each component: 20-50 lines
- Single responsibility
- Easy to test and maintain
- No monolithic files

### 3. React Query for Data Management

**Before (Manual State)**:
```typescript
const [goals, setGoals] = useState([])
const [isLoading, setIsLoading] = useState(true)
const [error, setError] = useState(null)

useEffect(() => {
  fetchGoals()
    .then(setGoals)
    .catch(setError)
    .finally(() => setIsLoading(false))
}, [])
```

**After (React Query)**:
```typescript
const { data: goals, isLoading, error } = useMyGoals()
```

**Benefits**:
- Automatic caching
- Request deduplication
- Background refetching
- Optimistic updates
- Less boilerplate

### 4. Context for Shared State

**Dashboard Context** (eliminates props drilling):

```typescript
// Before: Props drilling
<Page level={level}>
  <Layout level={level}>
    <Section level={level}>
      <Card level={level}> {/* Drilling! */}

// After: Context
<DashboardProvider user={user}>
  {/* Any component can access: */}
  const { user, canEditGoals, canViewTeam } = useDashboard()
</DashboardProvider>
```

### 5. Split View Layout

- **Left Panel**: Personal goals with status, progress, connections
- **Right Panel**: Team progress + pending approvals (for managers/executives)
- **Responsive**: Stacks vertically on mobile (<768px)

## Backend Architecture (FastAPI)

### Layered Architecture

```
┌─────────────────────────────┐
│   API Routers               │  FastAPI endpoints
│   - auth.py                 │  HTTP request handling
│   - individuals.py          │  Input validation
│   - onboarding.py           │  Response formatting
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│   Service Layer             │  Business logic
│   - whygo_service.py        │  Goal validation
│   - progress_service.py     │  Status calculation
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│   Repository Layer          │  Data access
│   - JsonWhygoRepository     │  CRUD operations
│   - JsonProgressRepository  │  Abstraction layer
└──────────────┬──────────────┘
               │
         ┌─────▼─────┐
         │ JSON Files│
         └───────────┘
```

**Key Benefits**:
- **Swappable Backend**: Replace JSON with PostgreSQL/MongoDB by implementing the same interfaces
- **Testable**: Each layer can be tested independently
- **Maintainable**: Changes to one layer don't affect others

### API Endpoints

**Base URL**: `http://localhost:8000`

```
Authentication:
POST /api/auth/login              # Email login (no password for MVP)
POST /api/auth/logout             # Logout

Users:
GET  /api/users/me                # Current user profile

Onboarding:
GET  /api/onboarding/context      # Full context (person, dept, company goals)
POST /api/onboarding/start        # Mark onboarding started
POST /api/onboarding/complete     # Mark onboarding complete

Individual Goals:
GET  /api/individuals/me          # Get user's goals
POST /api/individuals/create      # Create new goal (max 3)
POST /api/individuals/{id}/approve # Approve goal (managers only)
GET  /api/individuals/pending-approval # Get pending approvals
```

## Data Models

### WhyGO Structure

Every WhyGO follows the WHY-GOAL-OUTCOMES pattern:

```json
{
  "id": "ig_1_fill_isgro",
  "person_id": "person_fill_isgro",
  "why": "3 sentences explaining strategic importance",
  "goal": "Clear objective statement with timeframe",
  "outcomes": [
    {
      "outcome_id": "ig_1_o1_fill_isgro",
      "description": "Measurable result",
      "metric_type": "number",
      "targets": {
        "Q1": 100,
        "Q2": 200,
        "Q3": 300,
        "Q4": 400
      },
      "actuals": {
        "Q1": 120,
        "Q2": null,
        "Q3": null,
        "Q4": null
      },
      "owner": "person_fill_isgro"
    }
  ],
  "connects_to": ["dg_1_generative"],
  "status": "approved",
  "created_at": "2026-01-17T00:00:00Z"
}
```

### Status Calculation

```typescript
[+] On Track       = Green  = ≥100% of quarterly target
[~] Slightly Behind = Yellow = 80-99% of target
[-] Off Track      = Red    = <80% of target
[ ] Not Started    = Gray   = No data yet

Formula: status = (actual / target) * 100
```

## Design System

### Spacing
- **Container padding**: `px-6 py-6` (24px)
- **Card padding**: `p-4` (16px)
- **Element spacing**: `space-y-3` (12px)

### Borders
- **Standard**: `border` (1px solid)
- **Accent**: `border-2` (2px solid)
- **Colors**: `border-gray-200` (standard), `border-blue-600` (accent)

### Component Sizes
- **StatusDot**: `sm` (8px), `md` (12px), `lg` (16px)
- **ProgressBar**: `sm` (4px), `md` (8px), `lg` (12px)
- **Buttons**: `sm` (small), default (medium)

## Performance Optimizations

1. **Server Components**: Reduce client JavaScript by 30-50%
2. **React Query Caching**: Prevent duplicate API calls
3. **Atomic Components**: Enable code splitting and lazy loading
4. **Minimal Re-renders**: Context + memoization prevent unnecessary updates

## Security

1. **JWT Authentication**: Stateless token-based auth
2. **HTTP-Only Cookies**: Secure token storage (TODO)
3. **Role-Based Access**: Department heads vs ICs vs executives
4. **Input Validation**: Pydantic models on backend, TypeScript on frontend

## Scalability

### Current (MVP)
- JSON file storage
- Single server deployment
- ~100 users (Kartel team)

### Future (Scale)
- PostgreSQL/MongoDB
- Docker + Kubernetes
- Load balancing
- CDN for static assets
- Redis for session management

## Testing Strategy

### Frontend
- **Unit Tests**: Vitest for utilities and hooks
- **Component Tests**: React Testing Library
- **E2E Tests**: Playwright for critical flows

### Backend
- **Unit Tests**: pytest for services and utilities
- **Integration Tests**: FastAPI TestClient
- **API Tests**: Contract testing with Pact

## Deployment

### Development
```bash
# Backend
cd kartel-whygo-system && ./run_api.sh

# Frontend
cd whygo-onboarding && npm run dev
```

### Production (Planned)
- **Frontend**: Vercel or Netlify
- **Backend**: Railway, Fly.io, or AWS Lambda
- **Database**: PostgreSQL on Railway or Supabase
- **CDN**: Cloudflare

## Technology Stack

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 3.4
- **Data Fetching**: TanStack React Query 5
- **Icons**: Lucide React
- **HTTP Client**: Fetch API

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Validation**: Pydantic
- **Auth**: python-jose
- **ASGI Server**: Uvicorn

### Data
- **Current**: JSON files
- **Planned**: PostgreSQL or MongoDB

## Key Files Reference

### Frontend
- [app/dashboard/page.tsx](../whygo-onboarding/app/dashboard/page.tsx) - Server Component entry
- [app/dashboard/DashboardView.tsx](../whygo-onboarding/app/dashboard/DashboardView.tsx) - Client wrapper
- [lib/context/DashboardContext.tsx](../whygo-onboarding/lib/context/DashboardContext.tsx) - Permissions & user state
- [lib/api/queries.ts](../whygo-onboarding/lib/api/queries.ts) - React Query hooks

### Backend
- [src/api/routers/individuals.py](../kartel-whygo-system/src/api/routers/individuals.py) - Goal CRUD endpoints
- [src/api/routers/auth.py](../kartel-whygo-system/src/api/routers/auth.py) - Login logic
- [src/services/whygo_service.py](../kartel-whygo-system/src/services/whygo_service.py) - Business logic

## Known Limitations

1. **Auth Token Storage**: Currently localStorage, should be HTTP-only cookies
2. **Mock Team Data**: TeamProgressContainer uses hardcoded data
3. **Missing Person Names**: Approval cards show "Team Member" instead of real names
4. **Read-Only Dashboard**: "View Details" and "Edit" buttons not yet functional

See [CURRENT_STATE.md](../CURRENT_STATE.md) for current implementation status and next steps.
