-- =============================================
-- Accountant Hub — Complete Database Schema
-- PostgreSQL Migration File
-- 
-- Usage:
--   psql -U postgres -c "CREATE DATABASE accountant_hub;"
--   psql -U postgres -d accountant_hub -f 001_initial_schema.sql
-- =============================================

BEGIN;

-- =============================================
-- 01. users
-- =============================================
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    email_verified_at TIMESTAMPTZ,
    phone_verified_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    terms_accepted_at TIMESTAMPTZ,
    terms_version VARCHAR(20),
    last_login_at TIMESTAMPTZ,
    last_login_ip VARCHAR(45),
    restrictions JSONB DEFAULT NULL,
    audit_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT ck_users_role CHECK (role IN ('admin', 'client', 'accountant')),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT uq_users_phone UNIQUE (phone)
);

CREATE INDEX idx_users_role ON users (role);
CREATE INDEX idx_users_is_active ON users (is_active);
CREATE INDEX idx_users_created_at ON users (created_at DESC);

-- Add self-referencing FKs after table creation
ALTER TABLE users ADD CONSTRAINT fk_users_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE users ADD CONSTRAINT fk_users_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 02. countries
-- =============================================
CREATE TABLE countries (
    id BIGSERIAL PRIMARY KEY,
    country_name_ar VARCHAR(255),
    country_name_en VARCHAR(255) NOT NULL,
    country_iso_code2 VARCHAR(2) NOT NULL,
    country_iso_code3 VARCHAR(3) NOT NULL,
    country_iso_numeric VARCHAR(3),
    currency_name VARCHAR(100) NOT NULL,
    currency_iso_code VARCHAR(3) NOT NULL,
    currency_iso_number VARCHAR(3),
    phone_code VARCHAR(5) NOT NULL,
    phone_digits_count INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT uq_countries_iso2 UNIQUE (country_iso_code2),
    CONSTRAINT uq_countries_iso3 UNIQUE (country_iso_code3)
);

CREATE INDEX idx_countries_currency ON countries (currency_iso_code);
CREATE INDEX idx_countries_is_active ON countries (is_active);
CREATE INDEX idx_countries_name_en ON countries (country_name_en);

ALTER TABLE countries ADD CONSTRAINT fk_countries_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE countries ADD CONSTRAINT fk_countries_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 03. client_profiles
-- =============================================
CREATE TABLE client_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    company_industry VARCHAR(100),
    company_size VARCHAR(50),
    company_description TEXT,
    website VARCHAR(255),
    country_id BIGINT,
    city VARCHAR(100),
    logo_url VARCHAR(500),
    preferred_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    profile_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT uq_client_profile_user UNIQUE (user_id),
    CONSTRAINT fk_client_profile_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_client_profile_country FOREIGN KEY (country_id) REFERENCES countries(id) ON DELETE SET NULL
);

CREATE INDEX idx_client_profiles_industry ON client_profiles (company_industry);
CREATE INDEX idx_client_profiles_country ON client_profiles (country_id);

ALTER TABLE client_profiles ADD CONSTRAINT fk_client_profile_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE client_profiles ADD CONSTRAINT fk_client_profile_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 04. accountant_profiles
-- =============================================
CREATE TABLE accountant_profiles (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    bio TEXT,
    years_of_experience INTEGER,
    hourly_rate DECIMAL(10,2),
    hourly_rate_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    jurisdictions_served JSONB,
    accounting_standards JSONB,
    education_summary TEXT,
    identity_verified BOOLEAN NOT NULL DEFAULT FALSE,
    profile_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT uq_accountant_profile_user UNIQUE (user_id),
    CONSTRAINT fk_accountant_profile_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_accountant_profiles_experience ON accountant_profiles (years_of_experience);
CREATE INDEX idx_accountant_profiles_jurisdictions ON accountant_profiles USING GIN (jurisdictions_served);
CREATE INDEX idx_accountant_profiles_standards ON accountant_profiles USING GIN (accounting_standards);

ALTER TABLE accountant_profiles ADD CONSTRAINT fk_accountant_profile_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE accountant_profiles ADD CONSTRAINT fk_accountant_profile_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 05. certifications
-- =============================================
CREATE TABLE certifications (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    issuing_body VARCHAR(255),
    region VARCHAR(50),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT uq_certifications_name UNIQUE (name)
);

CREATE INDEX idx_certifications_region ON certifications (region);
CREATE INDEX idx_certifications_is_active ON certifications (is_active);
CREATE INDEX idx_certifications_name ON certifications (name);

ALTER TABLE certifications ADD CONSTRAINT fk_certifications_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE certifications ADD CONSTRAINT fk_certifications_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 06. accountant_certifications
-- =============================================
CREATE TABLE accountant_certifications (
    id BIGSERIAL PRIMARY KEY,
    accountant_profile_id BIGINT NOT NULL,
    certification_id BIGINT,
    custom_certification_name VARCHAR(255),
    license_number VARCHAR(100),
    issued_date DATE,
    expiry_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT ck_certification_or_custom CHECK (certification_id IS NOT NULL OR custom_certification_name IS NOT NULL),
    CONSTRAINT fk_acct_cert_profile FOREIGN KEY (accountant_profile_id) REFERENCES accountant_profiles(id) ON DELETE CASCADE,
    CONSTRAINT fk_acct_cert_certification FOREIGN KEY (certification_id) REFERENCES certifications(id) ON DELETE SET NULL
);

CREATE INDEX idx_acct_cert_profile ON accountant_certifications (accountant_profile_id);
CREATE INDEX idx_acct_cert_cert ON accountant_certifications (certification_id);
CREATE UNIQUE INDEX uq_acct_cert_profile_cert ON accountant_certifications (accountant_profile_id, certification_id) WHERE certification_id IS NOT NULL;

ALTER TABLE accountant_certifications ADD CONSTRAINT fk_acct_cert_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE accountant_certifications ADD CONSTRAINT fk_acct_cert_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 07. software_skills
-- =============================================
CREATE TABLE software_skills (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT uq_software_skills_name UNIQUE (name)
);

CREATE INDEX idx_software_skills_is_active ON software_skills (is_active);
CREATE INDEX idx_software_skills_name ON software_skills (name);

ALTER TABLE software_skills ADD CONSTRAINT fk_software_skills_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE software_skills ADD CONSTRAINT fk_software_skills_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 08. accountant_software_skills (pivot)
-- =============================================
CREATE TABLE accountant_software_skills (
    accountant_profile_id BIGINT NOT NULL,
    software_skill_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_accountant_software_skills PRIMARY KEY (accountant_profile_id, software_skill_id),
    CONSTRAINT fk_ass_profile FOREIGN KEY (accountant_profile_id) REFERENCES accountant_profiles(id) ON DELETE CASCADE,
    CONSTRAINT fk_ass_skill FOREIGN KEY (software_skill_id) REFERENCES software_skills(id) ON DELETE CASCADE
);

-- =============================================
-- 09. categories (self-referencing)
-- =============================================
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    parent_id BIGINT,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT uq_categories_slug UNIQUE (slug),
    CONSTRAINT ck_category_not_self_parent CHECK (id != parent_id),
    CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

CREATE INDEX idx_categories_parent ON categories (parent_id);
CREATE INDEX idx_categories_is_active ON categories (is_active);
CREATE INDEX idx_categories_sort ON categories (sort_order);
CREATE INDEX idx_categories_slug ON categories (slug);

ALTER TABLE categories ADD CONSTRAINT fk_categories_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE categories ADD CONSTRAINT fk_categories_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 10. jobs
-- =============================================
CREATE TABLE jobs (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    client_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    budget_min DECIMAL(12,2) NOT NULL,
    budget_max DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    pricing_model VARCHAR(20) NOT NULL DEFAULT 'fixed',
    deadline DATE NOT NULL,
    expected_delivery_time VARCHAR(100),
    engagement_type VARCHAR(20) NOT NULL DEFAULT 'one_time',
    jurisdiction VARCHAR(100),
    accounting_standard VARCHAR(50),
    required_certifications JSONB,
    required_software JSONB,
    required_skills JSONB,
    minimum_experience_years INTEGER,
    company_industry_context VARCHAR(100),
    nda_required BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    closed_reason VARCHAR(50),
    posted_date DATE NOT NULL DEFAULT CURRENT_DATE,
    bids_count INTEGER NOT NULL DEFAULT 0,
    bids_min_price DECIMAL(12,2),
    bids_max_price DECIMAL(12,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT ck_budget_range CHECK (budget_max >= budget_min),
    CONSTRAINT ck_deadline_after_posted CHECK (deadline >= posted_date),
    CONSTRAINT ck_jobs_pricing_model CHECK (pricing_model IN ('fixed', 'hourly', 'retainer')),
    CONSTRAINT ck_jobs_engagement_type CHECK (engagement_type IN ('one_time', 'recurring')),
    CONSTRAINT ck_jobs_status CHECK (status IN ('open', 'closed')),
    CONSTRAINT fk_jobs_client FOREIGN KEY (client_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_jobs_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

CREATE INDEX idx_jobs_client ON jobs (client_id);
CREATE INDEX idx_jobs_category ON jobs (category_id);
CREATE INDEX idx_jobs_status ON jobs (status);
CREATE INDEX idx_jobs_pricing ON jobs (pricing_model);
CREATE INDEX idx_jobs_jurisdiction ON jobs (jurisdiction);
CREATE INDEX idx_jobs_standard ON jobs (accounting_standard);
CREATE INDEX idx_jobs_engagement ON jobs (engagement_type);
CREATE INDEX idx_jobs_nda ON jobs (nda_required);
CREATE INDEX idx_jobs_deadline ON jobs (deadline);
CREATE INDEX idx_jobs_posted ON jobs (posted_date DESC);
CREATE INDEX idx_jobs_budget_min ON jobs (budget_min);
CREATE INDEX idx_jobs_budget_max ON jobs (budget_max DESC);
CREATE INDEX idx_jobs_currency ON jobs (currency);
CREATE INDEX idx_jobs_bids_count ON jobs (bids_count DESC);
CREATE INDEX idx_jobs_certs ON jobs USING GIN (required_certifications);
CREATE INDEX idx_jobs_software ON jobs USING GIN (required_software);
CREATE INDEX idx_jobs_skills ON jobs USING GIN (required_skills);

-- Full-text search index
CREATE INDEX idx_jobs_search ON jobs USING GIN (to_tsvector('english', title || ' ' || description));

ALTER TABLE jobs ADD CONSTRAINT fk_jobs_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE jobs ADD CONSTRAINT fk_jobs_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 11. bids
-- =============================================
CREATE TABLE bids (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL,
    accountant_id BIGINT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    pricing_model VARCHAR(20) NOT NULL DEFAULT 'fixed',
    includes_all_fees BOOLEAN NOT NULL DEFAULT TRUE,
    additional_costs_description TEXT,
    estimated_hours INTEGER,
    number_of_entities INTEGER,
    delivery_time VARCHAR(100) NOT NULL,
    services_included JSONB NOT NULL DEFAULT '[]',
    milestones JSONB,
    engagement_terms TEXT,
    proposal_letter TEXT NOT NULL,
    jurisdiction_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    terms_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    accepted_at TIMESTAMPTZ,
    rejected_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT ck_bid_price_positive CHECK (price > 0),
    CONSTRAINT ck_bid_pricing_model CHECK (pricing_model IN ('fixed', 'hourly', 'retainer')),
    CONSTRAINT ck_bid_status CHECK (status IN ('pending', 'accepted', 'rejected')),
    CONSTRAINT uq_job_accountant_bid UNIQUE (job_id, accountant_id),
    CONSTRAINT fk_bid_job FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    CONSTRAINT fk_bid_accountant FOREIGN KEY (accountant_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_bids_job ON bids (job_id);
CREATE INDEX idx_bids_accountant ON bids (accountant_id);
CREATE INDEX idx_bids_status ON bids (status);
CREATE INDEX idx_bids_created ON bids (created_at DESC);
CREATE INDEX idx_bids_services ON bids USING GIN (services_included);

ALTER TABLE bids ADD CONSTRAINT fk_bids_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE bids ADD CONSTRAINT fk_bids_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 12. nda_acceptances
-- =============================================
CREATE TABLE nda_acceptances (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    job_id BIGINT NOT NULL,
    content_version VARCHAR(20),
    ip_address VARCHAR(45),
    accepted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_job_nda UNIQUE (user_id, job_id),
    CONSTRAINT fk_nda_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_nda_job FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

CREATE INDEX idx_nda_user ON nda_acceptances (user_id);
CREATE INDEX idx_nda_job ON nda_acceptances (job_id);

-- =============================================
-- 13. job_attachments
-- =============================================
CREATE TABLE job_attachments (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER,
    file_type VARCHAR(50),
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    CONSTRAINT fk_job_attachment_job FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);

CREATE INDEX idx_job_attachments_job ON job_attachments (job_id);

ALTER TABLE job_attachments ADD CONSTRAINT fk_job_attachments_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 14. uploaded_documents
-- =============================================
CREATE TABLE uploaded_documents (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INTEGER,
    file_type VARCHAR(50),
    entity_type VARCHAR(50),
    entity_id BIGINT,
    description TEXT,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_by BIGINT,
    verified_at TIMESTAMPTZ,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT fk_uploaded_doc_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_uploaded_doc_verified_by FOREIGN KEY (verified_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_uploaded_docs_user ON uploaded_documents (user_id);
CREATE INDEX idx_uploaded_docs_entity ON uploaded_documents (entity_type, entity_id);
CREATE INDEX idx_uploaded_docs_type ON uploaded_documents (document_type);
CREATE INDEX idx_uploaded_docs_verified ON uploaded_documents (is_verified);

ALTER TABLE uploaded_documents ADD CONSTRAINT fk_uploaded_docs_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE uploaded_documents ADD CONSTRAINT fk_uploaded_docs_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 15. platform_content
-- =============================================
CREATE TABLE platform_content (
    id BIGSERIAL PRIMARY KEY,
    key VARCHAR(100) NOT NULL,
    title VARCHAR(255),
    body TEXT NOT NULL,
    content_type VARCHAR(50) NOT NULL DEFAULT 'text',
    version VARCHAR(20) NOT NULL DEFAULT '1.0',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by BIGINT,
    updated_by BIGINT,
    CONSTRAINT uq_platform_content_key UNIQUE (key)
);

CREATE INDEX idx_platform_content_key ON platform_content (key);
CREATE INDEX idx_platform_content_active ON platform_content (is_active);

ALTER TABLE platform_content ADD CONSTRAINT fk_platform_content_created_by FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE platform_content ADD CONSTRAINT fk_platform_content_updated_by FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL;

-- =============================================
-- 16. audit_logs
-- =============================================
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    user_email VARCHAR(255),
    user_role VARCHAR(20),
    action VARCHAR(100) NOT NULL,
    action_category VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT,
    description TEXT,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_audit_log_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_audit_logs_user ON audit_logs (user_id);
CREATE INDEX idx_audit_logs_category ON audit_logs (action_category);
CREATE INDEX idx_audit_logs_action ON audit_logs (action);
CREATE INDEX idx_audit_logs_entity ON audit_logs (entity_type, entity_id);
CREATE INDEX idx_audit_logs_created ON audit_logs (created_at DESC);

-- =============================================
-- 17. password_reset_tokens
-- =============================================
CREATE TABLE password_reset_tokens (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_password_reset_email ON password_reset_tokens (email);
CREATE INDEX idx_password_reset_token ON password_reset_tokens (token);
CREATE INDEX idx_password_reset_expires ON password_reset_tokens (expires_at);

-- =============================================
-- Trigger: auto-update updated_at timestamp
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables with updated_at
CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_client_profiles_updated_at BEFORE UPDATE ON client_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_accountant_profiles_updated_at BEFORE UPDATE ON accountant_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_certifications_updated_at BEFORE UPDATE ON certifications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_accountant_certifications_updated_at BEFORE UPDATE ON accountant_certifications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_software_skills_updated_at BEFORE UPDATE ON software_skills FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_categories_updated_at BEFORE UPDATE ON categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_jobs_updated_at BEFORE UPDATE ON jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_bids_updated_at BEFORE UPDATE ON bids FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_uploaded_documents_updated_at BEFORE UPDATE ON uploaded_documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_platform_content_updated_at BEFORE UPDATE ON platform_content FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER trg_countries_updated_at BEFORE UPDATE ON countries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;