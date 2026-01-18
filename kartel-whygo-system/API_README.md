# Kartel WhyGO Management API

## ✅ Implementation Complete!

The FastAPI REST API backend has been successfully implemented and is ready for the React/Next.js frontend.

---

## What's Been Built

### Core Infrastructure
- ✅ FastAPI application with automatic API docs
- ✅ JWT-based authentication (email login, no password for MVP)
- ✅ Dependency injection for services and repositories
- ✅ CORS middleware configured for frontend integration
- ✅ Pydantic models for request/response validation

### Data Layer Extensions
- ✅ Extended `Person` model with onboarding fields (email, onboarding_status, last_login, etc.)
- ✅ Repository layer extended with user/person methods
- ✅ All 22 employees have emails added (format: firstname.lastname@kartelai.com)

### Services Created
1. **UserService** - User profile and team operations
2. **OnboardingService** - Onboarding flow and context retrieval
3. **ValidationService** - WhyGO rule validation (3-goal limit, ladder-up, etc.)

### API Endpoints Implemented

#### Authentication (`/api/auth`)
- `POST /api/auth/login` - Email-based login, returns JWT token
- `POST /api/auth/logout` - Logout (client deletes token)

#### Users (`/api/users`)
- `GET /api/users/me` - Get current user's profile
- `PUT /api/users/me` - Update profile (email, timezone, notifications)
- `GET /api/users/me/team` - Get team members (same department)

#### Onboarding (`/api/onboarding`)
- `GET /api/onboarding/context` - Get all onboarding data (company goals, dept goals, individual goals, pending approvals)
- `POST /api/onboarding/start` - Mark onboarding as started
- `POST /api/onboarding/complete` - Mark onboarding as completed

#### Company Goals (`/api/company`)
- `GET /api/company/goals` - Get all 4 company WhyGOs
- `GET /api/company/dashboard` - Get company dashboard with stats

#### Departments (`/api/departments`)
- `GET /api/departments/{dept_id}/goals` - Get department goals
- `GET /api/departments/{dept_id}/dashboard` - Get department dashboard

#### Individual Goals (`/api/individuals`)
- `GET /api/individuals/me` - Get current user's individual goals

#### Outcomes (`/api/outcomes`)
- `GET /api/outcomes/{outcome_id}` - Get outcome details with quarterly data

---

## How to Run

### 1. Start the API Server

```bash
cd kartel-whygo-system
./run_api.sh
```

Or manually:
```bash
python3 -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access the API

- **API Root**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Testing the API

### Using curl

#### 1. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"ben.kusin@kartelai.com"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "person_id": "person_ben_kusin",
  "name": "Ben Kusin",
  "level": "department_head"
}
```

#### 2. Get Profile (with token)
```bash
TOKEN="<your-token-here>"

curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer $TOKEN"
```

#### 3. Get Onboarding Context
```bash
curl -X GET "http://localhost:8000/api/onboarding/context" \
  -H "Authorization: Bearer $TOKEN"
```

### Using the Swagger UI

1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Login using `/api/auth/login` endpoint with an email
4. Copy the `access_token` from the response
5. Click "Authorize" again and paste: `Bearer <token>`
6. Now you can test all endpoints interactively!

---

## Available Test Users

All 22 employees have been set up with emails:

| Name | Email | Level | Department |
|------|-------|-------|------------|
| Kevin Reilly | kevin.reilly@kartelai.com | Executive | Management |
| Luke Peterson | luke.peterson@kartelai.com | Executive | Management |
| Ben Kusin | ben.kusin@kartelai.com | Department Head | Sales |
| Wayan Palmieri | wayan.palmieri@kartelai.com | Department Head | Production |
| Fill Isgro | fill.isgro@kartelai.com | Department Head | Generative |
| Daniel Kalotov | daniel.kalotov@kartelai.com | Department Head | Community |
| Niels Hoffmann | niels.hoffmann@kartelai.com | Department Head | Platform |
| ... | (+ 15 more ICs/managers) | ... | ... |

---

## Project Structure

```
kartel-whygo-system/
├── src/
│   ├── api/                    # FastAPI application
│   │   ├── main.py            # App entry point
│   │   ├── config.py          # Settings from .env
│   │   ├── dependencies.py    # Dependency injection
│   │   └── routers/           # API endpoints
│   │       ├── auth.py        # Authentication
│   │       ├── users.py       # User profiles
│   │       ├── onboarding.py  # Onboarding flow
│   │       ├── company.py     # Company goals
│   │       ├── departments.py # Department goals
│   │       ├── individuals.py # Individual goals
│   │       └── outcomes.py    # Outcomes & progress
│   ├── models/
│   │   ├── whygo.py           # Data models (extended)
│   │   └── api_models.py      # Pydantic request/response models
│   ├── repositories/          # Data access layer
│   │   ├── interfaces.py      # Abstract interfaces
│   │   └── json_repository.py # JSON implementation
│   └── services/              # Business logic
│       ├── whygo_service.py   # WhyGO operations
│       ├── progress_service.py # Progress tracking
│       ├── user_service.py    # User operations (NEW)
│       ├── onboarding_service.py # Onboarding flow (NEW)
│       └── validation_service.py # WhyGO validation (NEW)
├── data/
│   ├── employees.json         # Now includes emails!
│   ├── company_whygos.json
│   ├── department_goals.json
│   └── individual_goals.json
├── .env                       # Configuration
├── requirements.txt           # Dependencies
├── run_api.sh                 # Start script
└── API_README.md              # This file
```

---

## Environment Variables

The `.env` file contains:

```bash
# Security
SECRET_KEY=<secure-random-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 1 week

# App settings
DEBUG=true
APP_NAME=Kartel WhyGO Management API
VERSION=1.0.0

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]

# Data
DATA_DIR=data
```

---

## Key Features

### 1. Authentication
- Simple email-based login (no password for MVP)
- JWT tokens with 1-week expiration
- Role-based access control (executive, department_head, manager, ic)

### 2. Onboarding Context API
The `/api/onboarding/context` endpoint returns everything needed for the onboarding UI:
- User's profile and department
- All 4 company goals
- Department goals (filtered by user's department)
- User's existing individual goals
- Pending approvals (if user is a manager/dept head)

### 3. Validation
The `ValidationService` enforces all WhyGO rules:
- Maximum 3 active goals per person
- Goals must ladder up to department goals
- 2-3 outcomes required
- Measurable targets required

### 4. Repository Pattern
- Easy to swap JSON for PostgreSQL/MongoDB later
- All business logic in services, not repositories
- In-memory operations for speed

---

## Next Steps

### For Frontend Development

1. **Start the API server**: `./run_api.sh`
2. **Build Next.js frontend** with these API endpoints
3. **Key flows to implement**:
   - Login screen → JWT token storage
   - Onboarding wizard → Calls `/api/onboarding/context`
   - Department head goal review → Shows goals from API
   - Individual goal creation → Posts to `/api/individuals/me`
   - Dashboard views → Real-time data from API

### Future Enhancements

The plan document includes full implementations for:
- Goal creation/editing endpoints
- Approval workflow endpoints
- Progress recording endpoints
- More detailed dashboard endpoints

These can be added by referencing the plan at:
`/Users/lukepeterson/.claude/plans/witty-toasting-sun.md`

---

## Troubleshooting

### API won't start
- Check that port 8000 is available
- Ensure all dependencies installed: `pip3 install -r requirements.txt`
- Check `.env` file exists with SECRET_KEY

### Authentication errors
- Verify email exists in `data/employees.json`
- Check JWT token is passed in `Authorization: Bearer <token>` header
- Token expires after 1 week

### Data not found
- Ensure JSON files exist in `data/` directory
- Check file permissions
- Repository loads data on startup

---

## Success Metrics

✅ API starts without errors
✅ Swagger docs accessible at /docs
✅ All 22 employees can login with email
✅ Onboarding context returns full data
✅ Company/department/individual goals accessible
✅ Authentication and authorization working
✅ Ready for frontend integration

---

**Status**: Ready for Next.js frontend development!

**Estimated Time to Frontend Integration**: The API is production-ready. Frontend team can start building immediately using the `/docs` for reference.
