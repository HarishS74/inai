-- ============================================================
-- INAI INSURANCE AI PLATFORM
-- 01_SCHEMA.SQL
-- PART 1
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- COMPANIES
-- ============================================================

CREATE TABLE IF NOT EXISTS companies (

    company_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_name VARCHAR(255) NOT NULL,

    company_short_name VARCHAR(100),

    company_type VARCHAR(50),

    registration_number VARCHAR(100),

    irdai_license_number VARCHAR(100),

    official_website TEXT,

    official_contact TEXT,

    official_email TEXT,

    company_address TEXT,

    company_description TEXT,

    insurance_categories TEXT,

    source_url TEXT,

    founded_year INT,

    active BOOLEAN DEFAULT TRUE,

    verification_id UUID,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    updated_at TIMESTAMPTZ DEFAULT NOW(),

    deleted_at TIMESTAMPTZ
);

-- ============================================================
-- CATEGORIES
-- ============================================================

CREATE TABLE IF NOT EXISTS categories (

    category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    category_name VARCHAR(100) NOT NULL,

    category_description TEXT,

    active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- POLICY STATUS
-- ============================================================

CREATE TABLE IF NOT EXISTS policy_status (

    status_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    status_name VARCHAR(50),

    description TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- POLICIES
-- ============================================================

CREATE TABLE IF NOT EXISTS policies (

    policy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL,

    category_id UUID,

    status_id UUID,

    policy_name VARCHAR(255) NOT NULL,

    policy_code VARCHAR(100),

    uin VARCHAR(100),

    policy_variant VARCHAR(150),

    policy_type VARCHAR(100),

    policy_description TEXT,

    policy_start_date DATE,

    policy_end_date DATE,

    policy_tenure INT,

    individual_or_family VARCHAR(50),

    new_or_renewal VARCHAR(50),

    minimum_entry_age INT,

    maximum_entry_age INT,

    minimum_sum_insured NUMERIC,

    maximum_sum_insured NUMERIC,

    official_policy_url TEXT,

    policy_brochure_url TEXT,

    policy_wording_url TEXT,

    prospectus_url TEXT,

    source_url TEXT,

    searchable_text TEXT,

    embedding_status BOOLEAN DEFAULT FALSE,

    version INT DEFAULT 1,

    active BOOLEAN DEFAULT TRUE,

    data_collected_date DATE,

    last_verified_date DATE,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    updated_at TIMESTAMPTZ DEFAULT NOW(),

    deleted_at TIMESTAMPTZ

);

-- ============================================================
-- POLICY DOCUMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS policy_documents (

    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    document_type VARCHAR(100),

    document_name TEXT,

    document_url TEXT,

    local_path TEXT,

    version VARCHAR(50),

    language VARCHAR(50),

    uploaded_at TIMESTAMPTZ DEFAULT NOW(),

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- COVERAGES
-- ============================================================

CREATE TABLE IF NOT EXISTS coverages (

    coverage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    coverage_name VARCHAR(255),

    coverage_category VARCHAR(100),

    coverage_type VARCHAR(100),

    coverage_description TEXT,

    coverage_amount NUMERIC,

    coverage_limit TEXT,

    coverage_percentage NUMERIC,

    sub_limit TEXT,

    annual_limit NUMERIC,

    lifetime_limit NUMERIC,

    included_or_optional VARCHAR(50),

    eligibility_conditions TEXT,

    coverage_duration TEXT,

    deductible TEXT,

    copayment TEXT,

    coinsurance TEXT,

    special_conditions TEXT,

    searchable_text TEXT,

    embedding_status BOOLEAN DEFAULT FALSE,

    disease_id UUID,

    active BOOLEAN DEFAULT TRUE,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- EXCLUSIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS exclusions (

    exclusion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    exclusion_name VARCHAR(255),

    exclusion_category VARCHAR(100),

    exclusion_description TEXT,

    permanent_or_conditional VARCHAR(100),

    applicable_conditions TEXT,

    exceptions TEXT,

    searchable_text TEXT,

    embedding_status BOOLEAN DEFAULT FALSE,

    disease_id UUID,

    verified BOOLEAN DEFAULT FALSE,

    active BOOLEAN DEFAULT TRUE,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- WAITING PERIODS
-- ============================================================

CREATE TABLE IF NOT EXISTS waiting_periods (

    waiting_period_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    waiting_period_type VARCHAR(100),

    condition TEXT,

    duration INT,

    unit VARCHAR(30),

    applicable_to TEXT,

    exceptions TEXT,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);
-- ============================================================
-- BENEFITS
-- ============================================================

CREATE TABLE IF NOT EXISTS benefits (

    benefit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    benefit_name VARCHAR(255),

    benefit_category VARCHAR(100),

    benefit_description TEXT,

    benefit_limit TEXT,

    benefit_amount NUMERIC,

    benefit_percentage NUMERIC,

    eligibility_conditions TEXT,

    applicable_conditions TEXT,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    searchable_text TEXT,

    embedding_status BOOLEAN DEFAULT FALSE,

    active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- RIDERS
-- ============================================================

CREATE TABLE IF NOT EXISTS riders (

    rider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    rider_name VARCHAR(255),

    rider_description TEXT,

    rider_type VARCHAR(100),

    rider_cost NUMERIC,

    rider_sum_insured NUMERIC,

    waiting_period TEXT,

    eligibility TEXT,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- ADD ONS
-- ============================================================

CREATE TABLE IF NOT EXISTS add_ons (

    addon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    addon_name VARCHAR(255),

    addon_description TEXT,

    addon_cost NUMERIC,

    addon_type VARCHAR(100),

    waiting_period TEXT,

    eligibility TEXT,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- ELIGIBILITY
-- ============================================================

CREATE TABLE IF NOT EXISTS eligibility (

    eligibility_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    minimum_age INT,

    maximum_age INT,

    gender VARCHAR(30),

    city TEXT,

    state TEXT,

    country TEXT,

    occupation TEXT,

    minimum_income NUMERIC,

    pre_existing_disease_allowed BOOLEAN,

    family_size INT,

    marital_status VARCHAR(50),

    eligibility_notes TEXT,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- PREMIUMS
-- ============================================================

CREATE TABLE IF NOT EXISTS premiums (

    premium_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    minimum_age INT,

    maximum_age INT,

    gender VARCHAR(30),

    city VARCHAR(100),

    sum_insured NUMERIC,

    premium_amount NUMERIC,

    premium_frequency VARCHAR(30),

    tax_amount NUMERIC,

    gst NUMERIC,

    effective_from DATE,

    effective_to DATE,

    source_document TEXT,

    source_page INT,

    source_url TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- PREMIUM RULES
-- ============================================================

CREATE TABLE IF NOT EXISTS premium_rules (

    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    rule_name VARCHAR(255),

    rule_type VARCHAR(100),

    rule_description TEXT,

    value TEXT,

    effective_from DATE,

    effective_to DATE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- DISEASES
-- ============================================================

CREATE TABLE IF NOT EXISTS diseases (

    disease_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    disease_name VARCHAR(255) UNIQUE,

    disease_category VARCHAR(100),

    icd_code VARCHAR(50),

    description TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- DISEASE COVERAGES
-- ============================================================

CREATE TABLE IF NOT EXISTS disease_coverages (

    disease_coverage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    disease_id UUID NOT NULL,

    policy_id UUID NOT NULL,

    coverage_id UUID,

    coverage_status VARCHAR(50),

    waiting_period TEXT,

    remarks TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- CLAIMS
-- ============================================================

CREATE TABLE IF NOT EXISTS claims (

    claim_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    claim_process TEXT,

    claim_intimation_method TEXT,

    claim_submission_method TEXT,

    claim_document_requirements TEXT,

    claim_deadline TEXT,

    cashless_claim_process TEXT,

    reimbursement_claim_process TEXT,

    claim_assistance TEXT,

    claim_settlement_information TEXT,

    claim_source TEXT,

    claim_source_date DATE,

    claim_settlement_ratio NUMERIC,

    claim_settlement_ratio_year INT,

    claim_ratio_source TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- HOSPITAL NETWORK
-- ============================================================

CREATE TABLE IF NOT EXISTS hospital_network (

    network_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    network_type VARCHAR(100),

    network_available BOOLEAN,

    network_size VARCHAR(100),

    network_hospital_count INT,

    network_location TEXT,

    cashless_available BOOLEAN,

    cashless_conditions TEXT,

    network_source TEXT,

    network_last_updated DATE,

    last_verified_date DATE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);
-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE IF NOT EXISTS users (

    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    full_name VARCHAR(255),

    email VARCHAR(255) UNIQUE,

    phone VARCHAR(20),

    password_hash TEXT,

    auth_provider VARCHAR(50),

    email_verified BOOLEAN DEFAULT FALSE,

    phone_verified BOOLEAN DEFAULT FALSE,

    active BOOLEAN DEFAULT TRUE,

    last_login TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    updated_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- USER PROFILES
-- ============================================================

CREATE TABLE IF NOT EXISTS user_profiles (

    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    date_of_birth DATE,

    gender VARCHAR(20),

    marital_status VARCHAR(50),

    occupation VARCHAR(100),

    annual_income NUMERIC,

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    lifestyle TEXT,

    smoker BOOLEAN,

    alcohol BOOLEAN,

    bmi NUMERIC,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    updated_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- USER REQUIREMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS user_requirements (

    requirement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    budget NUMERIC,

    required_sum_insured NUMERIC,

    family_members INT,

    has_pre_existing_disease BOOLEAN,

    diseases TEXT,

    maternity_required BOOLEAN,

    opd_required BOOLEAN,

    dental_required BOOLEAN,

    ayush_required BOOLEAN,

    critical_illness_required BOOLEAN,

    room_type_preference VARCHAR(100),

    preferred_company TEXT,

    preferred_city TEXT,

    notes TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- RECOMMENDATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS recommendations (

    recommendation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL,

    policy_id UUID NOT NULL,

    overall_score NUMERIC,

    recommendation_rank INT,

    recommendation_summary TEXT,

    ai_reasoning TEXT,

    confidence_score NUMERIC,

    recommended BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- RECOMMENDATION REASONS
-- ============================================================

CREATE TABLE IF NOT EXISTS recommendation_reasons (

    reason_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    recommendation_id UUID NOT NULL,

    reason_title VARCHAR(255),

    reason_description TEXT,

    weight NUMERIC,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- AI SCORES
-- ============================================================

CREATE TABLE IF NOT EXISTS ai_scores (

    score_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID NOT NULL,

    affordability_score NUMERIC,

    coverage_score NUMERIC,

    claim_score NUMERIC,

    hospital_score NUMERIC,

    flexibility_score NUMERIC,

    customer_score NUMERIC,

    overall_score NUMERIC,

    calculated_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- POLICY COMPARISONS
-- ============================================================

CREATE TABLE IF NOT EXISTS policy_comparisons (

    comparison_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID,

    policy_one UUID,

    policy_two UUID,

    comparison_result JSONB,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- DOCUMENT CHUNKS
-- ============================================================

CREATE TABLE IF NOT EXISTS document_chunks (

    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID,

    document_id UUID,

    chunk_number INT,

    page_number INT,

    chunk_text TEXT,

    token_count INT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- VECTOR EMBEDDINGS
-- ============================================================

CREATE TABLE IF NOT EXISTS vector_embeddings (

    embedding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    chunk_id UUID NOT NULL,

    embedding VECTOR(1024),

    embedding_model VARCHAR(100),

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- INGESTION JOBS
-- ============================================================

CREATE TABLE IF NOT EXISTS ingestion_jobs (

    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    file_name TEXT,

    company_name TEXT,

    document_type VARCHAR(100),

    ingestion_status VARCHAR(50),

    started_at TIMESTAMPTZ,

    completed_at TIMESTAMPTZ,

    records_created INT,

    error_message TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- AUDIT LOGS
-- ============================================================

CREATE TABLE IF NOT EXISTS audit_logs (

    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    table_name VARCHAR(100),

    record_id UUID,

    action VARCHAR(50),

    performed_by UUID,

    old_data JSONB,

    new_data JSONB,

    created_at TIMESTAMPTZ DEFAULT NOW()

);

-- ============================================================
-- VERIFICATION STATUS
-- ============================================================

CREATE TABLE IF NOT EXISTS verification_status (

    verification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    policy_id UUID,

    verified_by UUID,

    verification_status VARCHAR(50),

    remarks TEXT,

    verified_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW()

);