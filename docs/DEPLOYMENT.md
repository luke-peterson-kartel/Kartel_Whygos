# WHYGOs Deployment Guide

**Last Updated**: 2026-01-17

## Quick Start

### Prerequisites

- **Node.js**: 18+ (for Next.js frontend)
- **Python**: 3.9+ (for FastAPI backend)
- **npm**: 9+ or pnpm

### Development Setup

**1. Clone Repository**
```bash
cd /Users/lukepeterson/Desktop/Git\ Projects/WHYGOs
```

**2. Start Backend (FastAPI)**
```bash
cd kartel-whygo-system
pip install -r requirements.txt
./run_api.sh
```

Verify: http://localhost:8000/docs shows FastAPI interactive docs

**3. Start Frontend (Next.js)**
```bash
cd whygo-onboarding
npm install
npm run dev
```

Verify: http://localhost:3000 shows login page

### Environment Variables

**Backend** (`kartel-whygo-system/.env`):
```bash
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

**Frontend** (`whygo-onboarding/.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Test Accounts

| Email | Name | Role | Goals | Notes |
|-------|------|------|-------|-------|
| `fill.isgro@kartel.ai` | Fill Isgro | Department Head | 1/3 | Good for testing |
| `luke.peterson@kartel.ai` | Luke Peterson | Executive | 0/3 | Your account |
| `wayan.palmieri@kartel.ai` | Wayan Palmieri | Department Head | 0/3 | VP Production |
| `ben.kusin@kartel.ai` | Ben Kusin | Department Head | 3/3 | MAX - can't add more |

## Test Flows

### A. Complete Onboarding (New User)

1. Navigate to http://localhost:3000
2. Login with `fill.isgro@kartel.ai`
3. **Step 1: Profile** → Confirm profile information
4. **Step 2: Company Goals** → View 4 company WhyGOs
5. **Step 3: Department Goals** → View your department's goals
6. **Step 4: Create Goal** → Fill form with 2-3 outcomes
7. **Step 5: Complete** → See completion screen
8. Click "Go to Dashboard"

### B. View Dashboard

1. Navigate to http://localhost:3000/dashboard
2. **Left Panel**: Your personal goals
   - Status dots (green/yellow/red)
   - Progress bars
   - Quarterly badges (Q1-Q4)
   - Connection badges (→ Dept Goal #1)
   - Action buttons (View Details, Edit)
3. **Right Panel**: Leadership context (if manager/executive)
   - Team Progress
   - Pending Approvals

### C. Create Additional Goals

1. Click "Add Goal" button in left panel
2. Redirects to `/onboarding/goals`
3. Create goal (max 3 total per person)

## API Testing

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "fill.isgro@kartel.ai"}'

# Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {...}
}
```

### Get User Goals
```bash
TOKEN="your-token-here"

curl http://localhost:8000/api/individuals/me \
  -H "Authorization: Bearer $TOKEN"
```

### Get Onboarding Context
```bash
curl http://localhost:8000/api/onboarding/context \
  -H "Authorization: Bearer $TOKEN"
```

### Create Individual Goal
```bash
curl -X POST http://localhost:8000/api/individuals/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "why": "Why this matters",
    "goal": "What will be achieved",
    "outcomes": [
      {
        "description": "Measurable outcome",
        "metric_type": "number",
        "targets": {"Q1": 100, "Q2": 200, "Q3": 300, "Q4": 400},
        "owner": "person_fill_isgro"
      }
    ],
    "connects_to": ["dg_1_generative"]
  }'
```

## Build for Production

### Frontend
```bash
cd whygo-onboarding
npm run build
npm start  # Production server on port 3000
```

### Backend
```bash
cd kartel-whygo-system
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Production Deployment (Planned)

### Option 1: Vercel (Frontend) + Railway (Backend)

**Frontend (Vercel)**:
1. Connect GitHub repo to Vercel
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL=https://api.whygo.kartel.ai`
3. Deploy automatically on push to `main`

**Backend (Railway)**:
1. Create new Railway project
2. Add PostgreSQL database
3. Set environment variables:
   - `DATABASE_URL=postgresql://...`
   - `SECRET_KEY=...`
4. Deploy from GitHub

**Cost**: ~$20-50/month

### Option 2: AWS (Full Stack)

**Frontend**: S3 + CloudFront
**Backend**: Lambda + API Gateway
**Database**: RDS PostgreSQL
**Auth**: Cognito

**Cost**: ~$50-100/month

### Option 3: Self-Hosted (Docker)

```dockerfile
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./kartel-whygo-system
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...

  frontend:
    build: ./whygo-onboarding
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**Cost**: Server + domain (~$10-30/month)

## Database Migration (from JSON to PostgreSQL)

### 1. Install PostgreSQL
```bash
brew install postgresql  # macOS
# or use Railway, Supabase, etc.
```

### 2. Create Database
```sql
CREATE DATABASE whygo_system;
```

### 3. Update Backend
```python
# Replace JsonWhygoRepository with PostgresWhygoRepository
from src.repositories.postgres_repository import PostgresWhygoRepository

whygo_repo = PostgresWhygoRepository(database_url=os.getenv("DATABASE_URL"))
```

### 4. Migrate Data
```bash
python scripts/migrate_to_postgres.py
```

## Monitoring & Logging

### Development
- **Backend Logs**: Console output from `./run_api.sh`
- **Frontend Logs**: Browser console + Next.js terminal

### Production
- **Application Monitoring**: Sentry
- **Performance**: Vercel Analytics
- **Logs**: CloudWatch or Railway logs
- **Uptime**: UptimeRobot

## Backup Strategy

### Current (JSON Files)
```bash
# Backup data directory
cd kartel-whygo-system
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### Future (PostgreSQL)
```bash
# Daily automated backups
pg_dump whygo_system > backup-$(date +%Y%m%d).sql
```

## Troubleshooting

### Frontend Won't Start
```bash
cd whygo-onboarding
rm -rf node_modules .next
npm install
npm run dev
```

### Backend Won't Start
```bash
cd kartel-whygo-system
pip install --upgrade -r requirements.txt
python -m uvicorn src.api.main:app --reload
```

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Authentication Issues
- Clear browser localStorage
- Delete cookies
- Login again
- Check token expiration (7 days default)

### Data Not Showing
```bash
# Verify data files exist
ls kartel-whygo-system/data/

# Check file permissions
chmod 644 kartel-whygo-system/data/*.json

# Re-import from markdown sources
cd kartel-whygo-system
python scripts/import_whygos.py
```

## Performance Optimization

### Frontend
- Enable compression in Next.js config
- Optimize images with next/image
- Implement code splitting for large components
- Use React.memo for expensive components

### Backend
- Enable FastAPI response caching
- Use async database connections
- Implement request rate limiting
- Add database indexes for common queries

## Security Checklist

- [ ] Change default SECRET_KEY in production
- [ ] Enable HTTPS (SSL certificates)
- [ ] Implement rate limiting
- [ ] Add CORS restrictions
- [ ] Use HTTP-only cookies for tokens
- [ ] Enable CSP headers
- [ ] Regular dependency updates
- [ ] Implement proper error handling (no stack traces in production)

## Next Steps

See [CURRENT_STATE.md](../CURRENT_STATE.md) for current implementation status and roadmap.
