## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [What Was Built](#what-was-built)
- [Deployment](#deployment)
- [Setup Instructions](#setup-instructions)
- [Running Locally](#running-locally)
- [Running with Docker](#running-with-docker)
- [API Endpoints](#api-endpoints)
- [Test Credentials](#test-credentials)
- [Assumptions Made](#assumptions-made)

---

## Project Overview

Accountant Hub is a professional marketplace platform purpose-built for the accounting domain. It is not a generic job board with accounting labels — every feature reflects how real accounting engagements operate. The UI/UX was designed with Upwork-style patterns in mind, adapted and domain-specialised for accounting workflows.

**Four user roles:**
- **Public** — browse and filter job listings
- **Accountant** — register, build a profile, accept NDAs, view match scores, and submit structured bids
- **Client** — post accounting jobs, review bids, accept/reject, and manage the full job lifecycle
- **Administration** — full platform oversight: user management, content management, audit logs, and reference data

**Key domain features:**
- 8 predefined accounting certifications (CPA, CMA, ACCA, EA, CFA, CIA, DipIFRS, SOCPA) with expiry tracking and 30-day warnings
- Jurisdiction and accounting standards matching (GAAP, IFRS, Local GAAP)
- 5-dimension soft match scoring engine — never blocks submission, market decides
- Structured bid proposals: pricing model, milestones, engagement terms, jurisdiction confirmation
- Per-job NDA gate with DB-logged acceptance (IP + timestamp)
- Hierarchical accounting category taxonomy (6 parent, 18 child categories)
- Immutable audit logging (10 event types, before/after JSONB)
- EN/AR language toggle with full RTL layout support

---

## Tech Stack

> The brief suggested Laravel + MySQL. The stack below was chosen with a documented rationale for each deviation.

| Layer | Technology | Reason |
|---|---|---|
| Frontend | React 18 (Vite) | Component-based architecture, fast HMR, rich ecosystem |
| Backend | FastAPI (Python 3.10+) | Native async support, auto-generated Swagger/OpenAPI docs, Pydantic validation — superior for domain-specific JSONB fields |
| Database | PostgreSQL | JSONB with GIN indexes for certifications/skills/jurisdictions — performant flexible querying not achievable with MySQL's JSON implementation. CHECK constraints for data integrity |
| ORM | SQLAlchemy 2.0 (async) | Mature async support, type safety |
| Auth | JWT (python-jose + bcrypt) | Stateless, FastAPI standard, tab-isolated via sessionStorage |
| State Management | React Context + TanStack Query v5 | Context for auth; TanStack Query for server cache, pagination, auto-refetch |
| Styling | CSS Variables | Full dark/light theming with zero framework overhead, anti-flash on load |
| i18n | i18next + react-i18next | EN/AR with RTL layout support, Cairo font for Arabic |
| Deployment | Docker + Private Registry | React frontend built and served via Docker image; backend + DB containerised with docker-compose |

**Stack deviation rationale:** PostgreSQL was necessary for JSONB with GIN indexing — the accounting domain's flexible certification, software skill, and jurisdiction data cannot be served performantly by MySQL's JSON implementation. FastAPI was chosen over Laravel for native async and auto-generated OpenAPI documentation. These are engineering decisions, not preferences.

---

## What Was Built

### Required features — all delivered

- ✅ Jobs listing page with job cards (title, company, description, budget, deadline, category, bids count, status)
- ✅ Job detail page with full accounting-specific fields
- ✅ Structured bid submission with duplicate prevention
- ✅ Basic authentication: register, login, logout
- ✅ Only logged-in accountants can submit bids

### Bonus points — all delivered

| Bonus | Implementation |
|---|---|
| Dashboard for submitted bids | Accountant Dashboard + Client Dashboard with live stats |
| Job status: Open / Closed | Full filtering, status badges, `closed_reason` tracking (4 reasons) |
| Pagination for job listing | Backend offset/limit + TanStack Query + custom Pagination component |
| Better filtering and sorting | 10 filter parameters, 5 sort options — including domain-specific filters (jurisdiction, accounting standard) |
| Reusable UI components | 15+ components in `ui/` folder with consistent props API |
| API Resources / clean formatting | Standard `{data, meta}` envelope on all list endpoints |
| Deployment with live URL | Deployed on personal server via Docker — see [Deployment](#deployment) |
| README with setup instructions | This file |
| Seeded demo data | 10 jobs, 7 users, 10 countries, 24 categories, 8 certifications, 14 software skills, 9 content items |

### Extra — built beyond requirements

- **Admin role + full panel** — complete admin dashboard: user management, CRUD for all entities, audit log viewer, content management
- **Client role + job posting** — full client workflow: post, edit, close jobs, accept/reject bids, view bidder profiles
- **Hierarchical categories** — 6 parent + 18 child accounting taxonomy with self-referencing schema
- **Certification expiry tracking** — 30-day warning, expired certs excluded from match scores
- **Jurisdiction & standards matching** — cross-referenced in 5-dimension match engine
- **Software skills tracking** — 14 accounting software tools with profile tagging
- **NDA gate per job** — DB-driven NDA text, acceptance audit trail, IP logging
- **Match scoring engine** — 5-dimension matching with visual percentage score
- **Structured bid proposals** — 10+ fields including milestones, engagement terms, jurisdiction confirmation
- **Audit logging system** — 10 event types, immutable, filterable, admin-controllable
- **Dark/light theme** — CSS variables, localStorage persistence, anti-flash on load
- **EN/AR language toggle** — full i18n with RTL layout, Cairo font for Arabic
- **Document upload** — PDF/DOC/PNG/JPG with admin verification workflow
- **User restrictions (admin)** — JSONB permissions scoping per user account
- **Bidder profile view (client)** — access-gated: only viewable if accountant bid on that client's job

---

## Deployment

The project is deployed on a personal server using Docker.

**How it works:**
- The React frontend is built into a production bundle and served via a Docker image pushed to a private image registry
- The FastAPI backend runs as a Docker container
- PostgreSQL runs as a Docker container
- All services are orchestrated with `docker-compose`

**Repository includes:**
- `Dockerfile` for the backend
- `Dockerfile` for the frontend (multi-stage build)
- `docker-compose.yml` for running the full stack

**To run the full stack with Docker:**

```bash
# Clone the repo
git clone YOUR_GITHUB_REPO_URL
cd accountant-hub

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your values

# Build and start all services
docker-compose up --build

# Seed the database (first run only)
docker-compose exec backend python seed.py
```

The app will be available at `http://localhost:3000` and the API at `http://localhost:8000`.

---

## Setup Instructions

> Prefer Docker? See [Running with Docker](#running-with-docker) above — it's simpler.

For local development without Docker:

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPO_URL
cd accountant-hub
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/accountant_hub
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. Database Setup

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE accountant_hub;"

# Run migrations
alembic upgrade head

# Seed demo data
python seed.py
```

### 4. Frontend Setup

```bash
cd ../frontend
npm install
```

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## Running Locally

### Start the Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

API: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

### Start the Frontend

```bash
cd frontend
npm run dev
```

App: `http://localhost:5173`

---

## Running with Docker

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

Seed on first run:

```bash
docker-compose exec backend python seed.py
```

---

## API Endpoints

All endpoints are prefixed with `/api/v1/`. Protected routes require a `Bearer` JWT token in the `Authorization` header.

**Standard response envelope:**
```json
{
  "data": { ... },
  "meta": { "page": 1, "per_page": 12, "total": 48 }
}
```

### Public (8 endpoints — no auth required)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT |
| GET | `/jobs` | List jobs (10 filter params, 5 sort options, pagination) |
| GET | `/jobs/{id}` | Job detail (includes `current_user_bid` if authenticated) |
| GET | `/categories` | All categories |
| GET | `/certifications` | All certifications |
| GET | `/countries` | All countries |
| GET | `/content/{key}` | Platform content (NDA text, disclaimers) |

**Job filter parameters:**

| Parameter | Description |
|---|---|
| `?search=term` | Full-text search on title + description |
| `?category=slug` | Filter by category slug |
| `?budget_min=X` | Minimum budget |
| `?budget_max=Y` | Maximum budget |
| `?currency=USD` | Currency filter |
| `?pricing_model=fixed` | fixed / hourly / retainer |
| `?jurisdiction=US` | Jurisdiction filter |
| `?accounting_standard=GAAP` | Accounting standard filter |
| `?status=open` | open / closed / (empty for all) |
| `?sort=newest` | newest / budget_high / budget_low / bids / deadline |
| `?page=1&per_page=12` | Pagination |

### Accountant (11 endpoints — role: accountant)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs/{id}/accept-nda` | Accept NDA for a job (logged with IP + timestamp) |
| POST | `/jobs/{id}/bids` | Submit a structured bid |
| GET | `/jobs/{id}/match-score` | 5-dimension profile match score |
| GET | `/my-bids` | All submitted bids with status |
| GET | `/my-profile` | Accountant profile |
| PUT | `/my-profile` | Update profile |
| PUT | `/my-profile/certifications` | Update certifications |
| PUT | `/my-profile/software-skills` | Update software skills |
| POST | `/my-profile/documents` | Upload a document |
| GET | `/my-profile/documents` | List uploaded documents |
| DELETE | `/my-profile/documents/{id}` | Delete a document |

### Client (9 endpoints — role: client)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/my-jobs` | Post a new job |
| GET | `/my-jobs` | List my jobs |
| GET | `/my-jobs/{id}` | Job detail |
| PUT | `/my-jobs/{id}` | Edit a job |
| PATCH | `/my-jobs/{id}/status` | Manually open or close a job |
| GET | `/my-jobs/{id}/bids` | View all bids on a job (with accountant names) |
| PATCH | `/my-jobs/{id}/bids/{bid_id}/accept` | Accept a bid (closes job, rejects all others) |
| PATCH | `/my-jobs/{id}/bids/{bid_id}/reject` | Reject a bid |
| GET | `/accountants/{id}/profile?job_id=X` | View bidder profile (only if they bid on your job) |

### Admin (49 endpoints — role: admin)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/admin/dashboard/stats` | Platform stats: users by role, jobs by status, bids by status |
| GET/POST/PUT/DELETE | `/admin/users` | Full user management |
| PATCH | `/admin/users/{id}/restrictions` | Set per-user JSONB permission scopes |
| DELETE | `/admin/users/{id}/restrictions` | Remove user restrictions |
| GET/POST/PUT/DELETE | `/admin/jobs` | Full job management |
| GET/POST/PUT/DELETE | `/admin/bids` | Full bid management |
| GET/POST/PUT/DELETE | `/admin/categories` | Category management |
| GET/POST/PUT/DELETE | `/admin/certifications` | Certification management |
| GET/POST/PUT/DELETE | `/admin/software-skills` | Software skill management |
| GET/POST/PUT/DELETE | `/admin/countries` | Country management |
| GET/POST/PUT/DELETE | `/admin/documents` | Document management |
| GET/POST/PUT/DELETE | `/admin/content` | Platform content (NDA text, disclaimers, reminders) |
| GET/PATCH | `/admin/me/audit-toggle` | Toggle own audit logging |
| GET | `/admin/audit-logs` | Filterable immutable audit log |
| GET | `/admin/audit-logs/meta/filters` | Available filter values for audit log |

> Full interactive documentation available at `/docs` (Swagger UI) when running locally or via Docker.

---

## Test Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@accounthub.com | Admin123! |
| Accountant | ahmed@example.com | Ahmed123! |
| Accountant | sarah@example.com | Sarah123! |
| Accountant | john@example.com | John1234! |
| Client | deloitte@example.com | Deloitte1! |
| Client | emirates@example.com | Emirates1! |
| Client | techventures@example.com | TechVent1! |

---

## Assumptions Made

1. **Stack deviation** — PostgreSQL was chosen over MySQL for JSONB + GIN index support required by the accounting domain. FastAPI was chosen over Laravel for native async and auto-generated OpenAPI documentation. Each decision is documented with rationale in the architecture report.

2. **Soft match scoring** — The match engine warns on missing certifications, expired certifications, or jurisdiction mismatches but never blocks bid submission. The market decides suitability.

3. **NDA per job** — NDA acceptance is optional per job (controlled by a flag on the job). Jobs without an NDA flag do not require acceptance before bidding.

4. **Custom certifications** — Accountants can add certifications beyond the 8 predefined ones via a free-text field, enforced by a CHECK constraint (either predefined `certification_id` OR custom name, not both).

5. **Client authentication** — The brief stated client auth is not required but jobs should be seeded. A full client role was built to demonstrate a complete platform workflow.

6. **sessionStorage over localStorage** — JWT tokens are stored in sessionStorage (tab-isolated) to prevent cross-role conflicts when multiple tabs are open with different accounts.

7. **Admin role** — A full admin role was built beyond requirements to demonstrate production-grade platform thinking.

8. **Bidder profile access** — An accountant's full profile is only visible to a client if that accountant has bid on one of the client's jobs. Intentional privacy design decision.

9. **Deployment** — Deployed on a personal server using Docker. The React frontend is served via a Docker image from a private image registry. A `docker-compose` file was intentionally not included at this stage — for MVP scope, each service is run independently via Docker. A full `docker-compose` orchestration setup is a straightforward next step and was left out by design, not oversight. Environment variables and secrets are managed via `.env` files and are not committed to the repository.

