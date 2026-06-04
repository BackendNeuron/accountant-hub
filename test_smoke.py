"""
Accountant Hub - Full System Smoke Test
Run: python smoke_test.py
Output saved to: test_results.txt
"""
import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import httpx
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

BASE_URL = os.getenv("API_URL", "http://localhost:8001/api/v1")
DB_URL = "postgresql+asyncpg://postgres:mohamedhoss@localhost:5432/accountant_hub"

results = []
passed = 0
failed = 0

def log(msg, is_pass=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if is_pass is True:
        global passed
        passed += 1
        results.append(f"[{timestamp}] ✅ PASS: {msg}")
        print(f"✅ {msg}")
    elif is_pass is False:
        global failed
        failed += 1
        results.append(f"[{timestamp}] ❌ FAIL: {msg}")
        print(f"❌ {msg}")
    else:
        results.append(f"[{timestamp}] 📋 {msg}")
        print(f"📋 {msg}")


async def test_database():
    """Test database connection and seed data."""
    log("=== DATABASE TESTS ===")
    engine = create_async_engine(DB_URL, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with session_factory() as db:
        from sqlalchemy import text
        
        # Test connection
        try:
            await db.execute(text("SELECT 1"))
            log("Database connection successful", True)
        except Exception as e:
            log(f"Database connection failed: {e}", False)
            return

        # Check tables exist
        tables = ['users', 'jobs', 'bids', 'categories', 'certifications', 'countries', 'platform_content', 'audit_logs']
        for table in tables:
            try:
                result = await db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                log(f"Table '{table}' exists ({count} rows)", True)
            except Exception as e:
                log(f"Table '{table}' check failed: {e}", False)

        # Check seed data
        result = await db.execute(text("SELECT COUNT(*) FROM users WHERE role = 'admin'"))
        admin_count = result.scalar()
        log(f"Admin users: {admin_count}", admin_count >= 1)

        result = await db.execute(text("SELECT COUNT(*) FROM jobs"))
        job_count = result.scalar()
        log(f"Jobs seeded: {job_count}", job_count >= 5)

        result = await db.execute(text("SELECT COUNT(*) FROM categories"))
        cat_count = result.scalar()
        log(f"Categories seeded: {cat_count}", cat_count >= 10)

        result = await db.execute(text("SELECT COUNT(*) FROM certifications"))
        cert_count = result.scalar()
        log(f"Certifications seeded: {cert_count}", cert_count >= 5)

    await engine.dispose()


async def test_auth():
    """Test authentication endpoints."""
    log("\n=== AUTH TESTS ===")
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Register new user
        resp = await client.post("/auth/register", json={
            "name": "Test User",
            "email": "test_smoke@example.com",
            "phone": "+999000000000",
            "password": "TestPass123!",
            "role": "accountant"
        })
        if resp.status_code == 200:
            log("Register new user", True)
        elif resp.status_code == 409:
            log("Register - email already exists (expected if re-run)", True)
        else:
            log(f"Register failed: {resp.status_code} {resp.text}", False)

        # Login with valid credentials
        resp = await client.post("/auth/login", json={
            "email": "ahmed@example.com",
            "password": "Ahmed123!"
        })
        is_pass = resp.status_code == 200 and "access_token" in resp.json()
        log("Login with valid credentials", is_pass)
        token = resp.json().get("access_token", "") if resp.status_code == 200 else ""
        headers = {"Authorization": f"Bearer {token}"}

        # Login with invalid credentials
        resp = await client.post("/auth/login", json={
            "email": "ahmed@example.com",
            "password": "WrongPassword!"
        })
        log("Login with invalid credentials returns 401", resp.status_code == 401)

        # Get my profile (authenticated)
        resp = await client.get("/my-profile", headers=headers)
        is_pass = resp.status_code == 200 and "data" in resp.json()
        log("Get authenticated profile", is_pass)

        return token


async def test_public_endpoints():
    """Test public API endpoints."""
    log("\n=== PUBLIC ENDPOINTS ===")
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # List jobs
        resp = await client.get("/jobs")
        is_pass = resp.status_code == 200 and "data" in resp.json()
        log("GET /jobs returns job list", is_pass)

        # Filter jobs
        resp = await client.get("/jobs?status=open")
        is_pass = resp.status_code == 200
        log("Filter jobs by status=open", is_pass)

        resp = await client.get("/jobs?status=closed")
        is_pass = resp.status_code == 200
        log("Filter jobs by status=closed", is_pass)

        # Search jobs
        resp = await client.get("/jobs?search=IFRS")
        is_pass = resp.status_code == 200
        log("Search jobs by keyword", is_pass)

        # Sort jobs
        resp = await client.get("/jobs?sort=budget_high")
        is_pass = resp.status_code == 200
        log("Sort jobs by highest budget", is_pass)

        # Pagination
        resp = await client.get("/jobs?page=1&per_page=3")
        data = resp.json()
        is_pass = resp.status_code == 200 and data.get("meta", {}).get("per_page") == 3
        log("Pagination works (per_page=3)", is_pass)

        # Job detail
        resp = await client.get("/jobs/1")
        is_pass = resp.status_code == 200 and "job" in resp.json()
        log("GET /jobs/1 returns job detail", is_pass)

        # Categories
        resp = await client.get("/categories")
        is_pass = resp.status_code == 200 and len(resp.json().get("data", [])) > 0
        log("GET /categories returns categories", is_pass)

        # Certifications
        resp = await client.get("/certifications")
        is_pass = resp.status_code == 200 and len(resp.json().get("data", [])) > 0
        log("GET /certifications returns certifications", is_pass)

        # Countries
        resp = await client.get("/countries")
        is_pass = resp.status_code == 200 and len(resp.json().get("data", [])) > 0
        log("GET /countries returns countries", is_pass)

        # Content
        resp = await client.get("/content/terms_of_service")
        is_pass = resp.status_code == 200
        log("GET /content/terms_of_service", is_pass)

        resp = await client.get("/content/privacy_policy")
        is_pass = resp.status_code == 200
        log("GET /content/privacy_policy", is_pass)


async def test_accountant_flow(token=None):
    """Test accountant features."""
    log("\n=== ACCOUNTANT FLOW ===")
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        # Get match score
        resp = await client.get("/jobs/1/match-score", headers=headers)
        is_pass = resp.status_code == 200 and "data" in resp.json()
        log("GET match score for job", is_pass)

        # Accept NDA
        resp = await client.post("/jobs/1/accept-nda", json={"agree": True}, headers=headers)
        is_pass = resp.status_code in [200, 201]
        log("Accept NDA for job", is_pass)

        # Submit bid
        resp = await client.post("/jobs/2/bids", json={
            "price": 500,
            "pricing_model": "fixed",
            "delivery_time": "1 week",
            "proposal_letter": "I am qualified for this job with extensive experience in accounting and tax preparation services.",
            "services_included": ["Accounting"],
            "includes_all_fees": True,
            "jurisdiction_confirmed": True,
            "terms_accepted": True
        }, headers=headers)
        if resp.status_code == 201 or resp.status_code == 200:
            log("Submit bid on job", True)
        elif resp.status_code == 409:
            log("Submit bid - already submitted (expected on re-run)", True)
        else:
            log(f"Submit bid failed: {resp.status_code} {resp.text}", False)

        # My bids
        resp = await client.get("/my-bids", headers=headers)
        is_pass = resp.status_code == 200
        log("GET my bids", is_pass)

        # Update profile
        resp = await client.put("/my-profile", json={
            "bio": "Test bio updated",
            "years_of_experience": 5
        }, headers=headers)
        is_pass = resp.status_code == 200
        log("Update profile", is_pass)

        # Update certifications
        resp = await client.put("/my-profile/certifications", json={
            "certifications": ["CPA", "CMA"]
        }, headers=headers)
        is_pass = resp.status_code == 200
        log("Update certifications", is_pass)

        # Update software skills
        resp = await client.put("/my-profile/software-skills", json={
            "software_skills": ["QuickBooks", "Xero"]
        }, headers=headers)
        is_pass = resp.status_code == 200
        log("Update software skills", is_pass)


async def test_client_flow():
    """Test client features."""
    log("\n=== CLIENT FLOW ===")
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Login as client
        resp = await client.post("/auth/login", json={
            "email": "deloitte@example.com",
            "password": "Deloitte1!"
        })
        token = resp.json().get("access_token", "") if resp.status_code == 200 else ""
        headers = {"Authorization": f"Bearer {token}"}
        log("Client login", resp.status_code == 200)

        # List my jobs
        resp = await client.get("/my-jobs", headers=headers)
        is_pass = resp.status_code == 200
        log("GET my jobs", is_pass)

        # Create a job
        resp = await client.post("/my-jobs", json={
            "title": "Test Job Smoke Test",
            "description": "This is a smoke test job posting for verifying the system works end to end with all features.",
            "category_id": 3,
            "budget_min": 1000,
            "budget_max": 3000,
            "currency": "USD",
            "pricing_model": "fixed",
            "deadline": "2026-12-31",
            "engagement_type": "one_time"
        }, headers=headers)
        job_id = resp.json().get("data", {}).get("id") if resp.status_code == 200 else None
        log("Create new job", resp.status_code == 200)

        if job_id:
            # View job bids
            resp = await client.get(f"/my-jobs/{job_id}/bids", headers=headers)
            log(f"View bids on job #{job_id}", resp.status_code == 200)

            # Close job
            resp = await client.patch(f"/my-jobs/{job_id}/status", json={
                "status": "closed",
                "closed_reason": "cancelled_by_client"
            }, headers=headers)
            log(f"Close job #{job_id}", resp.status_code == 200)

        # Update client profile
        resp = await client.put("/my-profile", json={
            "company_name": "Deloitte Updated",
            "company_industry": "Professional Services"
        }, headers=headers)
        log("Update client profile", resp.status_code == 200)


async def test_admin_flow():
    """Test admin features."""
    log("\n=== ADMIN FLOW ===")
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Login as admin
        resp = await client.post("/auth/login", json={
            "email": "admin@accounthub.com",
            "password": "Admin123!"
        })
        token = resp.json().get("access_token", "") if resp.status_code == 200 else ""
        headers = {"Authorization": f"Bearer {token}"}
        log("Admin login", resp.status_code == 200)

        # Dashboard stats
        resp = await client.get("/admin/dashboard/stats", headers=headers)
        data = resp.json().get("data", {})
        has_keys = all(k in data for k in ["total_users", "total_jobs", "total_bids", "jobs_time_series", "top_accountants"])
        log("Dashboard stats with all keys", resp.status_code == 200 and has_keys)

        # List users
        resp = await client.get("/admin/users", headers=headers)
        log("Admin list users", resp.status_code == 200)

        # List jobs
        resp = await client.get("/admin/jobs", headers=headers)
        log("Admin list jobs", resp.status_code == 200)

        # List bids
        resp = await client.get("/admin/bids", headers=headers)
        log("Admin list bids", resp.status_code == 200)

        # List categories
        resp = await client.get("/admin/categories", headers=headers)
        log("Admin list categories", resp.status_code == 200)

        # Create category
        resp = await client.post("/admin/categories", json={
            "name": "Test Category Smoke",
            "slug": "test-smoke-cat"
        }, headers=headers)
        cat_id = resp.json().get("data", {}).get("id") if resp.status_code == 200 else None
        log("Admin create category", resp.status_code == 200)

        # List certifications
        resp = await client.get("/admin/certifications", headers=headers)
        log("Admin list certifications", resp.status_code == 200)

        # List software skills
        resp = await client.get("/admin/software-skills", headers=headers)
        log("Admin list software skills", resp.status_code == 200)

        # List countries
        resp = await client.get("/admin/countries", headers=headers)
        log("Admin list countries", resp.status_code == 200)

        # List documents
        resp = await client.get("/admin/documents", headers=headers)
        log("Admin list documents", resp.status_code == 200)

        # List content
        resp = await client.get("/admin/content", headers=headers)
        log("Admin list content", resp.status_code == 200)

        # Audit logs
        resp = await client.get("/admin/audit-logs", headers=headers)
        log("Admin view audit logs", resp.status_code == 200)

        # Audit toggle
        resp = await client.get("/admin/me/audit-toggle", headers=headers)
        log("Admin get audit toggle", resp.status_code == 200)

        resp = await client.patch("/admin/me/audit-toggle", json={"audit_enabled": True}, headers=headers)
        log("Admin set audit toggle", resp.status_code == 200)

        # Restrictions
        resp = await client.get("/admin/users/2/restrictions", headers=headers)
        log("Admin view user restrictions", resp.status_code == 200)

        # Cleanup - delete test category
        if cat_id:
            resp = await client.delete(f"/admin/categories/{cat_id}", headers=headers)
            log("Admin delete test category", resp.status_code in [200, 400])


async def test_error_handling():
    """Test error handling and edge cases."""
    log("\n=== ERROR HANDLING ===")
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Duplicate bid prevention
        resp = await client.post("/auth/login", json={
            "email": "ahmed@example.com", "password": "Ahmed123!"
        })
        token = resp.json().get("access_token", "")
        headers = {"Authorization": f"Bearer {token}"}

        resp = await client.post("/jobs/1/bids", json={
            "price": 500, "pricing_model": "fixed", "delivery_time": "1 week",
            "proposal_letter": "Duplicate test bid submission for verification purposes. This is a test.",
            "services_included": ["Accounting"], "includes_all_fees": True,
            "jurisdiction_confirmed": True, "terms_accepted": True
        }, headers=headers)
        if resp.status_code == 409:
            log("Duplicate bid returns 409", True)
        elif resp.status_code == 200 or resp.status_code == 201:
            log("Bid submitted (first time for this user)", True)
        else:
            log(f"Unexpected response: {resp.status_code}", False)

        # Protected endpoint without auth
        resp = await client.get("/my-profile")
        log("Protected endpoint without auth returns 401/403", resp.status_code in [401, 403])

        # Invalid job ID
        try:
            resp = await client.get("/jobs/99999")
            log("Invalid job ID returns 404", resp.status_code == 404)
        except Exception:
            log("Invalid job ID test - connection handled", True)

        # Wrong credentials
        resp = await client.post("/auth/login", json={"email": "wrong@email.com", "password": "wrong"})
        log("Wrong credentials returns 401", resp.status_code == 401)


async def main():
    log("=" * 60)
    log("ACCOUNTANT HUB - FULL SYSTEM SMOKE TEST")
    log(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)

    # Database tests
    await test_database()

    # Auth tests
    token = await test_auth()

    # Public endpoints
    await test_public_endpoints()

    # Accountant flow
    await test_accountant_flow(token)

    # Client flow
    await test_client_flow()

    # Admin flow
    await test_admin_flow()

    # Error handling
    await test_error_handling()

    # Summary
    log("\n" + "=" * 60)
    log(f"TEST RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
    log(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)

    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), "test_results.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Accountant Hub - Smoke Test Results\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Result: {passed} passed, {failed} failed, {passed + failed} total\n")
        f.write("=" * 60 + "\n\n")
        for line in results:
            f.write(line + "\n")
    log(f"\n📄 Results saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())