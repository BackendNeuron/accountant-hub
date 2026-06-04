
-- =============================================
-- Accountant Hub — Complete Database Schema
-- Run: psql -U postgres -d accountant_hub -f 001_initial_schema.sql
-- =============================================

-- 01. users
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'client', 'accountant')),
    email_verified_at TIMESTAMP NULL,
    phone_verified_at TIMESTAMP NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    terms_accepted_at TIMESTAMP NULL,
    terms_version VARCHAR(20) NULL,
    last_login_at TIMESTAMP NULL,
    last_login_ip VARCHAR(45) NULL,
    restrictions JSONB NULL DEFAULT NULL,
    audit_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);

-- 02. countries
CREATE TABLE countries (
    id BIGSERIAL PRIMARY KEY,
    country_name_ar VARCHAR(255) NULL,
    country_name_en VARCHAR(255) NOT NULL,
    country_iso_code2 VARCHAR(2) NOT NULL UNIQUE,
    country_iso_code3 VARCHAR(3) NOT NULL UNIQUE,
    country_iso_numeric VARCHAR(3) NULL,
    currency_name VARCHAR(100) NOT NULL,
    currency_iso_code VARCHAR(3) NOT NULL,
    currency_iso_number VARCHAR(3) NULL,
    phone_code VARCHAR(5) NOT NULL,
    phone_digits_count INTEGER NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_countries_currency ON countries(currency_iso_code);
CREATE INDEX idx_countries_is_active ON countries(is_active);

-- 03. client_profiles
CREATE TABLE client_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    company_industry VARCHAR(100) NULL,
    company_size VARCHAR(50) NULL,
    company_description TEXT NULL,
    website VARCHAR(255) NULL,
    country_id BIGINT NULL REFERENCES countries(id),
    city VARCHAR(100) NULL,
    logo_url VARCHAR(500) NULL,
    preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    profile_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_client_profiles_industry ON client_profiles(company_industry);
CREATE INDEX idx_client_profiles_country ON client_profiles(country_id);

-- 04. accountant_profiles
CREATE TABLE accountant_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT NULL,
    years_of_experience INTEGER NULL,
    hourly_rate DECIMAL(10,2) NULL,
    hourly_rate_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    jurisdictions_served JSONB NULL,
    accounting_standards JSONB NULL,
    education_summary TEXT NULL,
    identity_verified BOOLEAN NOT NULL DEFAULT FALSE,
    profile_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_accountant_profiles_experience ON accountant_profiles(years_of_experience);
CREATE INDEX idx_accountant_profiles_jurisdictions ON accountant_profiles USING GIN(jurisdictions_served);
CREATE INDEX idx_accountant_profiles_standards ON accountant_profiles USING GIN(accounting_standards);

-- 05. certifications
CREATE TABLE certifications (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    issuing_body VARCHAR(255) NULL,
    region VARCHAR(50) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_certifications_region ON certifications(region);
CREATE INDEX idx_certifications_is_active ON certifications(is_active);

-- 06. accountant_certifications
CREATE TABLE accountant_certifications (
    id BIGSERIAL PRIMARY KEY,
    accountant_profile_id BIGINT NOT NULL REFERENCES accountant_profiles(id) ON DELETE CASCADE,
    certification_id BIGINT NULL REFERENCES certifications(id) ON DELETE SET NULL,
    custom_certification_name VARCHAR(255) NULL,
    license_number VARCHAR(100) NULL,
    issued_date DATE NULL,
    expiry_date DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT ck_certification_or_custom CHECK (certification_id IS NOT NULL OR custom_certification_name IS NOT NULL)
);
CREATE INDEX idx_acct_cert_profile ON accountant_certifications(accountant_profile_id);
CREATE INDEX idx_acct_cert_cert ON accountant_certifications(certification_id);

-- 07. software_skills
CREATE TABLE software_skills (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_software_skills_is_active ON software_skills(is_active);

-- 08. accountant_software_skills
CREATE TABLE accountant_software_skills (
    accountant_profile_id BIGINT NOT NULL REFERENCES accountant_profiles(id) ON DELETE CASCADE,
    software_skill_id BIGINT NOT NULL REFERENCES software_skills(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (accountant_profile_id, software_skill_id)
);

-- 09. categories
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    parent_id BIGINT NULL REFERENCES categories(id) ON DELETE SET NULL,
    description TEXT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT ck_category_not_self_parent CHECK (id != parent_id)
);
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_is_active ON categories(is_active);
CREATE INDEX idx_categories_sort ON categories(sort_order);

-- 10. jobs
CREATE TABLE jobs (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    client_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    budget_min DECIMAL(12,2) NOT NULL,
    budget_max DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    pricing_model VARCHAR(20) NOT NULL CHECK (pricing_model IN ('fixed', 'hourly', 'retainer')),
    deadline DATE NOT NULL,
    expected_delivery_time VARCHAR(100) NULL,
    engagement_type VARCHAR(20) NOT NULL DEFAULT 'one_time' CHECK (engagement_type IN ('one_time', 'recurring')),
    jurisdiction VARCHAR(100) NULL,
    accounting_standard VARCHAR(50) NULL,
    required_certifications JSONB NULL,
    required_software JSONB NULL,
    required_skills JSONB NULL,
    minimum_experience_years INTEGER NULL,
    company_industry_context VARCHAR(100) NULL,
    nda_required BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'closed')),
    closed_reason VARCHAR(50) NULL,
    posted_date DATE NOT NULL DEFAULT CURRENT_DATE,
    bids_count INTEGER NOT NULL DEFAULT 0,
    bids_min_price DECIMAL(12,2) NULL,
    bids_max_price DECIMAL(12,2) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT ck_budget_range CHECK (budget_max >= budget_min),
    CONSTRAINT ck_deadline_after_posted CHECK (deadline >= posted_date)
);
CREATE INDEX idx_jobs_client ON jobs(client_id);
CREATE INDEX idx_jobs_category ON jobs(category_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_pricing ON jobs(pricing_model);
CREATE INDEX idx_jobs_jurisdiction ON jobs(jurisdiction);
CREATE INDEX idx_jobs_standard ON jobs(accounting_standard);
CREATE INDEX idx_jobs_engagement ON jobs(engagement_type);
CREATE INDEX idx_jobs_nda ON jobs(nda_required);
CREATE INDEX idx_jobs_deadline ON jobs(deadline);
CREATE INDEX idx_jobs_posted ON jobs(posted_date);
CREATE INDEX idx_jobs_budget_min ON jobs(budget_min);
CREATE INDEX idx_jobs_budget_max ON jobs(budget_max);
CREATE INDEX idx_jobs_currency ON jobs(currency);
CREATE INDEX idx_jobs_certs ON jobs USING GIN(required_certifications);
CREATE INDEX idx_jobs_software ON jobs USING GIN(required_software);
CREATE INDEX idx_jobs_skills ON jobs USING GIN(required_skills);

-- 11. bids
CREATE TABLE bids (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    accountant_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    price DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    pricing_model VARCHAR(20) NOT NULL CHECK (pricing_model IN ('fixed', 'hourly', 'retainer')),
    includes_all_fees BOOLEAN NOT NULL DEFAULT TRUE,
    additional_costs_description TEXT NULL,
    estimated_hours INTEGER NULL,
    number_of_entities INTEGER NULL,
    delivery_time VARCHAR(100) NOT NULL,
    services_included JSONB NOT NULL,
    milestones JSONB NULL,
    engagement_terms TEXT NULL,
    proposal_letter TEXT NOT NULL,
    jurisdiction_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    terms_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected')),
    accepted_at TIMESTAMP NULL,
    rejected_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id),
    CONSTRAINT uq_job_accountant_bid UNIQUE (job_id, accountant_id),
    CONSTRAINT ck_bid_price_positive CHECK (price > 0)
);
CREATE INDEX idx_bids_job ON bids(job_id);
CREATE INDEX idx_bids_accountant ON bids(accountant_id);
CREATE INDEX idx_bids_status ON bids(status);
CREATE INDEX idx_bids_created ON bids(created_at);
CREATE INDEX idx_bids_services ON bids USING GIN(services_included);

-- 12. nda_acceptances
CREATE TABLE nda_acceptances (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    content_version VARCHAR(20) NULL,
    ip_address VARCHAR(45) NULL,
    accepted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_job_nda UNIQUE (user_id, job_id)
);
CREATE INDEX idx_nda_user ON nda_acceptances(user_id);
CREATE INDEX idx_nda_job ON nda_acceptances(job_id);

-- 13. job_attachments
CREATE TABLE job_attachments (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER NULL,
    file_type VARCHAR(50) NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_job_attachments_job ON job_attachments(job_id);

-- 14. uploaded_documents
CREATE TABLE uploaded_documents (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_type VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER NULL,
    file_type VARCHAR(50) NULL,
    entity_type VARCHAR(50) NULL,
    entity_id BIGINT NULL,
    description TEXT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_by BIGINT NULL REFERENCES users(id),
    verified_at TIMESTAMP NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_uploaded_docs_user ON uploaded_documents(user_id);
CREATE INDEX idx_uploaded_docs_entity ON uploaded_documents(entity_type, entity_id);
CREATE INDEX idx_uploaded_docs_type ON uploaded_documents(document_type);

-- 15. platform_content
CREATE TABLE platform_content (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(100) NOT NULL UNIQUE,
    title VARCHAR(255) NULL,
    body TEXT NOT NULL,
    content_type VARCHAR(50) NOT NULL DEFAULT 'text',
    version VARCHAR(20) NOT NULL DEFAULT '1.0',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by BIGINT NULL REFERENCES users(id),
    updated_by BIGINT NULL REFERENCES users(id)
);
CREATE INDEX idx_platform_content_key ON platform_content(key);
CREATE INDEX idx_platform_content_active ON platform_content(is_active);

-- 16. audit_logs
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
    user_email VARCHAR(255) NULL,
    user_role VARCHAR(20) NULL,
    action VARCHAR(100) NOT NULL,
    action_category VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT NULL,
    description TEXT NULL,
    old_values JSONB NULL,
    new_values JSONB NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_category ON audit_logs(action_category);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- 17. password_reset_tokens
CREATE TABLE password_reset_tokens (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_password_reset_email ON password_reset_tokens(email);
CREATE INDEX idx_password_reset_token ON password_reset_tokens(token);
CREATE INDEX idx_password_reset_expires ON password_reset_tokens(expires_at);
