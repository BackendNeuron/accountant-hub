"""
Accountant Hub - Master Seed Script
Seeds all reference data + demo users + sample jobs
Run: python seed_all.py
"""
import asyncio
import sys
import os
from datetime import date, timedelta, datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from app.database import Base
from app.models.user import User
from app.models.country import Country
from app.models.category import Category
from app.models.certification import Certification
from app.models.software_skill import SoftwareSkill
from app.models.platform_content import PlatformContent
from app.models.accountant_profile import AccountantProfile
from app.models.client_profile import ClientProfile
from app.models.job import Job
from app.utils.security import hash_password

DATABASE_URL = "postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/YOUR_DB_NAME"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed():
    async with AsyncSessionLocal() as db:
        print("🌱 Starting seed...")

        # ==========================================
        # 1. ADMIN USER
        # ==========================================
        existing = await db.execute(select(User).where(User.email == "admin@accounthub.com"))
        if not existing.scalar_one_or_none():
            admin = User(
                name="Admin",
                email="admin@accounthub.com",
                phone="+1000000000",
                password=hash_password("Admin123!"),
                role="admin",
                is_active=True,
                email_verified_at=datetime.utcnow(),
            )
            db.add(admin)
            await db.flush()
            print("  ✅ Admin user created (admin@accounthub.com / Admin123!)")

        # ==========================================
        # 2. COUNTRIES
        # ==========================================
        countries_data = [
            {"country_name_ar": "المملكة العربية السعودية", "country_name_en": "Saudi Arabia", "country_iso_code2": "SA", "country_iso_code3": "SAU", "currency_name": "Saudi Riyal", "currency_iso_code": "SAR", "phone_code": "+966", "phone_digits_count": 9},
            {"country_name_ar": "الإمارات العربية المتحدة", "country_name_en": "United Arab Emirates", "country_iso_code2": "AE", "country_iso_code3": "ARE", "currency_name": "UAE Dirham", "currency_iso_code": "AED", "phone_code": "+971", "phone_digits_count": 9},
            {"country_name_ar": "مصر", "country_name_en": "Egypt", "country_iso_code2": "EG", "country_iso_code3": "EGY", "currency_name": "Egyptian Pound", "currency_iso_code": "EGP", "phone_code": "+20", "phone_digits_count": 10},
            {"country_name_ar": "الولايات المتحدة", "country_name_en": "United States", "country_iso_code2": "US", "country_iso_code3": "USA", "currency_name": "US Dollar", "currency_iso_code": "USD", "phone_code": "+1", "phone_digits_count": 10},
            {"country_name_ar": "المملكة المتحدة", "country_name_en": "United Kingdom", "country_iso_code2": "GB", "country_iso_code3": "GBR", "currency_name": "Pound Sterling", "currency_iso_code": "GBP", "phone_code": "+44", "phone_digits_count": 10},
            {"country_name_ar": "قطر", "country_name_en": "Qatar", "country_iso_code2": "QA", "country_iso_code3": "QAT", "currency_name": "Qatari Riyal", "currency_iso_code": "QAR", "phone_code": "+974", "phone_digits_count": 8},
            {"country_name_ar": "الكويت", "country_name_en": "Kuwait", "country_iso_code2": "KW", "country_iso_code3": "KWT", "currency_name": "Kuwaiti Dinar", "currency_iso_code": "KWD", "phone_code": "+965", "phone_digits_count": 8},
            {"country_name_ar": "عمان", "country_name_en": "Oman", "country_iso_code2": "OM", "country_iso_code3": "OMN", "currency_name": "Omani Rial", "currency_iso_code": "OMR", "phone_code": "+968", "phone_digits_count": 8},
            {"country_name_ar": "البحرين", "country_name_en": "Bahrain", "country_iso_code2": "BH", "country_iso_code3": "BHR", "currency_name": "Bahraini Dinar", "currency_iso_code": "BHD", "phone_code": "+973", "phone_digits_count": 8},
            {"country_name_ar": "النمسا", "country_name_en": "Austria", "country_iso_code2": "AT", "country_iso_code3": "AUT", "currency_name": "Euro", "currency_iso_code": "EUR", "phone_code": "+43", "phone_digits_count": 10},
        ]
        count_countries = 0
        for c in countries_data:
            existing = await db.execute(select(Country).where(Country.country_iso_code2 == c["country_iso_code2"]))
            if not existing.scalar_one_or_none():
                db.add(Country(**c))
                count_countries += 1
        await db.flush()
        print(f"  ✅ {count_countries} countries seeded")

        # ==========================================
        # 3. CATEGORIES (Hierarchical)
        # ==========================================
        categories_tree = {
            "Tax Services": {
                "slug": "tax-services",
                "children": {
                    "Individual Tax Preparation": "individual-tax",
                    "Corporate Tax Filing": "corporate-tax",
                    "Tax Planning & Advisory": "tax-planning",
                    "VAT/GST/Sales Tax": "vat-gst",
                }
            },
            "Audit & Assurance": {
                "slug": "audit-assurance",
                "children": {
                    "External Audit": "external-audit",
                    "Internal Audit": "internal-audit",
                    "SOX Compliance": "sox-compliance",
                }
            },
            "Bookkeeping": {
                "slug": "bookkeeping",
                "children": {
                    "Monthly Reconciliation": "monthly-reconciliation",
                    "Accounts Payable/Receivable": "ap-ar",
                    "Payroll Processing": "payroll",
                }
            },
            "Financial Advisory": {
                "slug": "financial-advisory",
                "children": {
                    "Mergers & Acquisitions": "mergers-acquisitions",
                    "Valuation Services": "valuation",
                    "Due Diligence": "due-diligence",
                }
            },
            "Forensic Accounting": {
                "slug": "forensic-accounting",
                "children": {
                    "Fraud Investigation": "fraud-investigation",
                    "Litigation Support": "litigation-support",
                }
            },
            "Specialized": {
                "slug": "specialized",
                "children": {
                    "IFRS Conversion": "ifrs-conversion",
                    "ESG Reporting": "esg-reporting",
                    "Crypto Accounting": "crypto-accounting",
                }
            },
        }
        count_cats = 0
        sort_order = 0
        for parent_name, parent_data in categories_tree.items():
            existing = await db.execute(select(Category).where(Category.slug == parent_data["slug"]))
            if not existing.scalar_one_or_none():
                parent = Category(name=parent_name, slug=parent_data["slug"], sort_order=sort_order)
                db.add(parent)
                await db.flush()
                count_cats += 1
                sort_order += 1
                child_order = 0
                for child_name, child_slug in parent_data["children"].items():
                    existing_child = await db.execute(select(Category).where(Category.slug == child_slug))
                    if not existing_child.scalar_one_or_none():
                        child = Category(name=child_name, slug=child_slug, parent_id=parent.id, sort_order=child_order)
                        db.add(child)
                        count_cats += 1
                        child_order += 1
        await db.flush()
        print(f"  ✅ {count_cats} categories seeded")

        # ==========================================
        # 4. CERTIFICATIONS
        # ==========================================
        certs = [
            {"name": "CPA", "issuing_body": "AICPA", "region": "US"},
            {"name": "CMA", "issuing_body": "IMA", "region": "Global"},
            {"name": "ACCA", "issuing_body": "ACCA", "region": "UK/Global"},
            {"name": "EA", "issuing_body": "IRS", "region": "US"},
            {"name": "CFA", "issuing_body": "CFA Institute", "region": "Global"},
            {"name": "CIA", "issuing_body": "IIA", "region": "Global"},
            {"name": "DipIFRS", "issuing_body": "ACCA", "region": "Global"},
            {"name": "SOCPA", "issuing_body": "SOCPA", "region": "Saudi Arabia"},
        ]
        count_certs = 0
        for c in certs:
            existing = await db.execute(select(Certification).where(Certification.name == c["name"]))
            if not existing.scalar_one_or_none():
                db.add(Certification(**c))
                count_certs += 1
        await db.flush()
        print(f"  ✅ {count_certs} certifications seeded")

        # ==========================================
        # 5. SOFTWARE SKILLS
        # ==========================================
        software = [
            "QuickBooks", "Xero", "SAP", "Oracle NetSuite", "Sage",
            "Zoho Books", "FreshBooks", "Wave", "Microsoft Dynamics GP", "Tally",
            "Excel/Google Sheets", "Tableau", "Power BI", "Alteryx",
        ]
        count_sw = 0
        for s in software:
            existing = await db.execute(select(SoftwareSkill).where(SoftwareSkill.name == s))
            if not existing.scalar_one_or_none():
                db.add(SoftwareSkill(name=s))
                count_sw += 1
        await db.flush()
        print(f"  ✅ {count_sw} software skills seeded")

        # ==========================================
        # 6. PLATFORM CONTENT
        # ==========================================
        content_data = {
            "disclaimer_footer": {
                "title": "Platform Disclaimer",
                "body": "Accountant Hub is a marketplace connecting businesses with independent accounting professionals. We do not employ, verify, or guarantee the work of any accountant. All engagements are direct contracts between clients and professionals. We are not liable for tax errors, filing mistakes, or financial losses.",
            },
            "disclaimer_registration": {
                "title": "Registration Terms",
                "body": "By registering, you agree to our Terms of Service and Privacy Policy. You confirm that the information you provide is accurate and that you are authorized to use this platform.",
            },
            "disclaimer_bid_submission": {
                "title": "Bid Submission Disclaimer",
                "body": "By submitting this bid, you confirm you are qualified to perform this work in the specified jurisdiction. You understand this platform does not verify professional credentials. The client is solely responsible for evaluating your qualifications.",
            },
            "nda_default_text": {
                "title": "Non-Disclosure Agreement",
                "body": "By accepting, you agree to maintain strict confidentiality of all information shared in this job posting, including financial data, company information, and any attachments. You agree not to share, copy, or use this information for any purpose other than submitting your proposal. This obligation survives whether or not you are awarded the engagement.",
            },
            "terms_of_service": {
                "title": "Terms of Service",
                "body": "These Terms of Service govern your use of Accountant Hub. By using the platform, you agree to these terms. Accountant Hub serves as a marketplace only and is not a party to any contracts between clients and accountants. Users are responsible for their own tax compliance, professional licensing, and work quality.",
            },
            "privacy_policy": {
                "title": "Privacy Policy",
                "body": "We collect information you provide during registration and platform use. This includes your name, email, phone, professional credentials, and uploaded documents. We do not sell your data. Your information is used solely to facilitate connections on the platform and to improve our services.",
            },
            "reminder_profile_incomplete": {
                "title": "Complete Your Profile",
                "body": "Your profile is incomplete. Accountants with complete profiles receive 3x more engagement from clients. Add your certifications, experience, and software skills to increase your visibility.",
            },
            "reminder_certification_expiring": {
                "title": "Certification Expiring",
                "body": "One or more of your certifications is expiring within 30 days. Update your certification details to maintain accurate match scores.",
            },
            "reminder_certification_expired": {
                "title": "Certification Expired",
                "body": "One or more of your certifications has expired. Expired certifications are not counted in match scores. Please update your profile.",
            },
        }
        count_content = 0
        for key, data in content_data.items():
            existing = await db.execute(select(PlatformContent).where(PlatformContent.key == key))
            if not existing.scalar_one_or_none():
                db.add(PlatformContent(key=key, title=data["title"], body=data["body"], is_active=True, published_at=datetime.utcnow()))
                count_content += 1
        await db.flush()
        print(f"  ✅ {count_content} platform content items seeded")

        # ==========================================
        # 7. DEMO ACCOUNTANTS
        # ==========================================
        accountant_users = [
            {"name": "Ahmed Hassan", "email": "ahmed@example.com", "phone": "+966501234567", "password": "Ahmed123!", "bio": "Senior Tax Accountant with 8 years experience in GCC tax law", "years": 8, "rate": 150, "jurisdictions": ["SA", "AE", "QA"], "standards": ["IFRS", "Local GAAP"], "certs": ["CPA", "SOCPA"], "software": ["QuickBooks", "SAP", "Excel/Google Sheets"]},
            {"name": "Sarah Ibrahim", "email": "sarah@example.com", "phone": "+971501234567", "password": "Sarah123!", "bio": "ACCA qualified auditor specializing in external audit and SOX compliance", "years": 5, "rate": 120, "jurisdictions": ["AE", "US"], "standards": ["IFRS", "GAAP"], "certs": ["ACCA", "CIA"], "software": ["Xero", "Oracle NetSuite", "Power BI"]},
            {"name": "John Smith", "email": "john@example.com", "phone": "+12025551234", "password": "John1234!", "bio": "CPA with forensic accounting expertise, 12 years in fraud investigation", "years": 12, "rate": 200, "jurisdictions": ["US", "GB"], "standards": ["GAAP", "IFRS"], "certs": ["CPA", "CFA"], "software": ["SAP", "Tableau", "Alteryx"]},
        ]

        accountant_ids = []
        for a in accountant_users:
            existing = await db.execute(select(User).where(User.email == a["email"]))
            if not existing.scalar_one_or_none():
                user = User(
                    name=a["name"], email=a["email"], phone=a["phone"],
                    password=hash_password(a["password"]), role="accountant",
                    is_active=True, email_verified_at=datetime.utcnow(),
                )
                db.add(user)
                await db.flush()

                profile = AccountantProfile(
                    user_id=user.id, bio=a["bio"], years_of_experience=a["years"],
                    hourly_rate=a["rate"], jurisdictions_served=a["jurisdictions"],
                    accounting_standards=a["standards"], profile_completed=True,
                    identity_verified=True,
                )
                db.add(profile)
                accountant_ids.append(user.id)
        await db.flush()
        print(f"  ✅ {len(accountant_users)} demo accountants seeded")

        # ==========================================
        # 8. DEMO CLIENTS + JOBS
        # ==========================================
        client_users = [
            {"name": "Deloitte Middle East", "email": "deloitte@example.com", "phone": "+966551234567", "password": "Deloitte1!", "company_name": "Deloitte & Touche", "industry": "Professional Services", "size": "1000+", "country_code": "SA"},
            {"name": "Emirates Holdings", "email": "emirates@example.com", "phone": "+971551234567", "password": "Emirates1!", "company_name": "Emirates Holdings Group", "industry": "Real Estate", "size": "501-1000", "country_code": "AE"},
            {"name": "TechVentures Inc", "email": "techventures@example.com", "phone": "+12025559876", "password": "TechVent1!", "company_name": "TechVentures Inc", "industry": "Technology/SaaS", "size": "51-200", "country_code": "US"},
        ]

        # Get country IDs
        result = await db.execute(select(Country))
        countries_map = {c.country_iso_code2: c.id for c in result.scalars().all()}

        client_ids = []
        for cl in client_users:
            existing = await db.execute(select(User).where(User.email == cl["email"]))
            if not existing.scalar_one_or_none():
                user = User(
                    name=cl["name"], email=cl["email"], phone=cl["phone"],
                    password=hash_password(cl["password"]), role="client",
                    is_active=True, email_verified_at=datetime.utcnow(),
                )
                db.add(user)
                await db.flush()

                profile = ClientProfile(
                    user_id=user.id, company_name=cl["company_name"],
                    company_industry=cl["industry"], company_size=cl["size"],
                    country_id=countries_map.get(cl["country_code"]),
                    profile_completed=True,
                )
                db.add(profile)
                client_ids.append(user.id)
        await db.flush()
        print(f"  ✅ {len(client_users)} demo clients seeded")

        # Get category IDs
        result = await db.execute(select(Category))
        all_cats = result.scalars().all()
        cat_map = {c.slug: c.id for c in all_cats}

        # Sample jobs
        today = date.today()
        jobs_data = [
            {"title": "Senior Corporate Tax Accountant Needed", "description": "We are looking for an experienced corporate tax accountant to handle Q4 2026 filings for our Saudi operations. The ideal candidate should have strong knowledge of Saudi tax law (Zakat, VAT) and experience with multinational corporations.\n\nScope includes:\n- Preparation of corporate tax returns\n- Zakat calculation and filing\n- VAT reconciliation\n- Tax planning advisory for 2027\n\nPlease include your experience with Saudi tax authorities in your proposal.", "client_idx": 0, "cat_slug": "corporate-tax", "budget_min": 5000, "budget_max": 10000, "currency": "SAR", "pricing_model": "fixed", "deadline": today + timedelta(days=30), "jurisdiction": "SA", "standard": "IFRS", "req_certs": ["CPA", "SOCPA"], "req_software": ["SAP", "QuickBooks"], "req_skills": ["Tax Preparation", "Zakat", "VAT"], "engagement": "one_time", "nda": True},
            {"title": "Monthly Bookkeeping for Real Estate Company", "description": "Emirates Holdings needs an ongoing bookkeeper to manage monthly reconciliations for 5 entities across Dubai and Abu Dhabi. We use Xero and need someone who can commit to a recurring monthly engagement.\n\nResponsibilities:\n- Monthly bank reconciliation\n- Accounts payable/receivable management\n- Monthly financial statements\n- Inter-company transaction recording", "client_idx": 1, "cat_slug": "monthly-reconciliation", "budget_min": 3000, "budget_max": 5000, "currency": "AED", "pricing_model": "retainer", "deadline": today + timedelta(days=14), "jurisdiction": "AE", "standard": "IFRS", "req_certs": ["ACCA"], "req_software": ["Xero"], "req_skills": ["Bookkeeping", "Reconciliation"], "engagement": "recurring", "nda": False},
            {"title": "External Audit for SaaS Company", "description": "TechVentures Inc is preparing for Series B funding and needs a full external audit of our 2025-2026 financials. Must have experience with SaaS revenue recognition (ASC 606) and US GAAP.\n\nDeliverables:\n- Audited financial statements\n- Management letter\n- Revenue recognition review\n- Internal controls assessment", "client_idx": 2, "cat_slug": "external-audit", "budget_min": 15000, "budget_max": 25000, "currency": "USD", "pricing_model": "fixed", "deadline": today + timedelta(days=45), "jurisdiction": "US", "standard": "GAAP", "req_certs": ["CPA"], "req_software": ["Excel/Google Sheets", "Tableau"], "req_skills": ["Auditing", "ASC 606", "SaaS"], "engagement": "one_time", "nda": True},
            {"title": "VAT Filing Specialist - UAE", "description": "Need a VAT specialist to handle quarterly VAT filing for our UAE entities. Must be up to date with FTA regulations and have experience with multiple entity filings.\n\nScope: 3 entities, quarterly filing, reconciliation of VAT returns with accounting records.", "client_idx": 1, "cat_slug": "vat-gst", "budget_min": 2000, "budget_max": 4000, "currency": "AED", "pricing_model": "fixed", "deadline": today + timedelta(days=7), "jurisdiction": "AE", "standard": "IFRS", "req_certs": ["ACCA", "CMA"], "req_software": ["Zoho Books", "QuickBooks"], "req_skills": ["VAT", "FTA Compliance"], "engagement": "recurring", "nda": False},
            {"title": "Financial Due Diligence for M&A Deal", "description": "Conduct financial due diligence on a target company in the logistics sector. Review 3 years of financials, identify risks, assess working capital, and provide a detailed due diligence report for our investment committee.\n\nConfidential project. NDA required before details shared.", "client_idx": 0, "cat_slug": "due-diligence", "budget_min": 8000, "budget_max": 15000, "currency": "SAR", "pricing_model": "fixed", "deadline": today + timedelta(days=21), "jurisdiction": "SA", "standard": "IFRS", "req_certs": ["CPA", "CFA"], "req_software": ["Power BI", "Excel/Google Sheets"], "req_skills": ["Due Diligence", "Financial Analysis", "M&A"], "engagement": "one_time", "nda": True},
            {"title": "Payroll Setup & Processing", "description": "Setting up payroll for a new entity in Qatar. Need someone to configure payroll system, register with authorities, and process monthly payroll for ~50 employees. Ongoing engagement preferred.", "client_idx": 2, "cat_slug": "payroll", "budget_min": 1000, "budget_max": 2500, "currency": "USD", "pricing_model": "retainer", "deadline": today + timedelta(days=10), "jurisdiction": "QA", "standard": "IFRS", "req_certs": [], "req_software": ["Sage", "SAP"], "req_skills": ["Payroll", "HR Compliance"], "engagement": "recurring", "nda": False},
            {"title": "IFRS Conversion Project", "description": "Our company is transitioning from local GAAP to full IFRS. Need an experienced accountant to lead the conversion project, including restatement of prior year financials, training our team, and documentation of new accounting policies.", "client_idx": 1, "cat_slug": "ifrs-conversion", "budget_min": 10000, "budget_max": 20000, "currency": "AED", "pricing_model": "fixed", "deadline": today + timedelta(days=60), "jurisdiction": "AE", "standard": "IFRS", "req_certs": ["ACCA", "DipIFRS"], "req_software": ["Oracle NetSuite", "Excel/Google Sheets"], "req_skills": ["IFRS", "Financial Reporting", "Conversion"], "engagement": "one_time", "nda": False},
            {"title": "Internal Audit - SOX Compliance", "description": "Annual internal audit focusing on SOX compliance for our US-listed entity. Review internal controls, test key controls, document findings, and present to audit committee. Previous Big 4 experience strongly preferred.", "client_idx": 0, "cat_slug": "sox-compliance", "budget_min": 12000, "budget_max": 18000, "currency": "USD", "pricing_model": "fixed", "deadline": today + timedelta(days=35), "jurisdiction": "US", "standard": "GAAP", "req_certs": ["CPA", "CIA"], "req_software": ["SAP", "Power BI"], "req_skills": ["Internal Audit", "SOX", "COSO"], "engagement": "one_time", "nda": True},
            {"title": "Tax Planning for Crypto Startup", "description": "Innovative crypto startup needs tax advisory for structuring operations across multiple jurisdictions. Knowledge of crypto taxation, token classification, and cross-border tax planning essential.", "client_idx": 2, "cat_slug": "crypto-accounting", "budget_min": 4000, "budget_max": 7000, "currency": "USD", "pricing_model": "hourly", "deadline": today + timedelta(days=14), "jurisdiction": "Global", "standard": "IFRS", "req_certs": ["CPA", "CFA"], "req_software": ["Excel/Google Sheets"], "req_skills": ["Crypto", "Tax Planning", "Cross-border"], "engagement": "one_time", "nda": True},
            {"title": "Accounts Receivable Cleanup", "description": "Short-term project to clean up and reconcile AR aging for a retail company with 200+ customers. We've migrated from legacy to SAP and need cleanup of outstanding items from the last 18 months.", "client_idx": 0, "cat_slug": "ap-ar", "budget_min": 2500, "budget_max": 4500, "currency": "SAR", "pricing_model": "fixed", "deadline": today + timedelta(days=14), "jurisdiction": "SA", "standard": "IFRS", "req_certs": [], "req_software": ["SAP", "Excel/Google Sheets"], "req_skills": ["AR", "Reconciliation"], "engagement": "one_time", "nda": False},
        ]

        # Close some older jobs for variety
        closed_count = 0
        count_jobs = 0
        for i, jd in enumerate(jobs_data):
            client_id = client_ids[jd["client_idx"]]
            existing = await db.execute(select(Job).where(Job.title == jd["title"], Job.client_id == client_id))
            if not existing.scalar_one_or_none():
                is_closed = i >= 7  # Close jobs 8, 9, 10 for variety
                job = Job(
                    title=jd["title"], description=jd["description"],
                    client_id=client_id, category_id=cat_map.get(jd["cat_slug"]),
                    budget_min=jd["budget_min"], budget_max=jd["budget_max"],
                    currency=jd["currency"], pricing_model=jd["pricing_model"],
                    deadline=jd["deadline"], jurisdiction=jd["jurisdiction"],
                    accounting_standard=jd["standard"],
                    required_certifications=jd["req_certs"] if jd["req_certs"] else None,
                    required_software=jd["req_software"] if jd["req_software"] else None,
                    required_skills=jd["req_skills"] if jd["req_skills"] else None,
                    engagement_type=jd["engagement"], nda_required=jd["nda"],
                    status="closed" if is_closed else "open",
                    closed_reason="deadline_passed" if is_closed else None,
                    posted_date=today - timedelta(days=(i * 3 + 1)),
                    bids_count=0,
                )
                db.add(job)
                count_jobs += 1
                if is_closed:
                    closed_count += 1
        await db.flush()
        print(f"  ✅ {count_jobs} jobs seeded ({closed_count} closed, {count_jobs - closed_count} open)")

        await db.commit()
        print("\n🎉 SEED COMPLETE!")
        print("\n--- Test Credentials ---")
        print("Admin:     admin@accounthub.com / Admin123!")
        print("Accountant: ahmed@example.com / Ahmed123!")
        print("Accountant: sarah@example.com / Sarah123!")
        print("Accountant: john@example.com / John1234!")
        print("Client:    deloitte@example.com / Deloitte1!")
        print("Client:    emirates@example.com / Emirates1!")
        print("Client:    techventures@example.com / TechVent1!")


if __name__ == "__main__":
    asyncio.run(seed())
