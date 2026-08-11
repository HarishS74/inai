-- ============================================================
-- 03_indexes.sql
-- PERFORMANCE INDEXES
-- ============================================================

-- =========================
-- COMPANIES
-- =========================

CREATE INDEX IF NOT EXISTS idx_company_name
ON companies(company_name);

CREATE INDEX IF NOT EXISTS idx_company_active
ON companies(active);

-- =========================
-- POLICIES
-- =========================

CREATE INDEX IF NOT EXISTS idx_policy_company
ON policies(company_id);

CREATE INDEX IF NOT EXISTS idx_policy_category
ON policies(category_id);

CREATE INDEX IF NOT EXISTS idx_policy_status
ON policies(status_id);

CREATE INDEX IF NOT EXISTS idx_policy_name
ON policies(policy_name);

CREATE INDEX IF NOT EXISTS idx_policy_type
ON policies(policy_type);

CREATE INDEX IF NOT EXISTS idx_policy_active
ON policies(active);

CREATE INDEX IF NOT EXISTS idx_policy_uin
ON policies(uin);

-- =========================
-- DOCUMENTS
-- =========================

CREATE INDEX IF NOT EXISTS idx_document_policy
ON policy_documents(policy_id);

CREATE INDEX IF NOT EXISTS idx_document_type
ON policy_documents(document_type);

-- =========================
-- COVERAGES
-- =========================

CREATE INDEX IF NOT EXISTS idx_coverage_policy
ON coverages(policy_id);

CREATE INDEX IF NOT EXISTS idx_coverage_name
ON coverages(coverage_name);

CREATE INDEX IF NOT EXISTS idx_coverage_category
ON coverages(coverage_category);

CREATE INDEX IF NOT EXISTS idx_coverage_disease
ON coverages(disease_id);

CREATE INDEX IF NOT EXISTS idx_coverage_active
ON coverages(active);

-- =========================
-- EXCLUSIONS
-- =========================

CREATE INDEX IF NOT EXISTS idx_exclusion_policy
ON exclusions(policy_id);

CREATE INDEX IF NOT EXISTS idx_exclusion_name
ON exclusions(exclusion_name);

CREATE INDEX IF NOT EXISTS idx_exclusion_category
ON exclusions(exclusion_category);

CREATE INDEX IF NOT EXISTS idx_exclusion_disease
ON exclusions(disease_id);

-- =========================
-- WAITING PERIODS
-- =========================

CREATE INDEX IF NOT EXISTS idx_waiting_policy
ON waiting_periods(policy_id);

CREATE INDEX IF NOT EXISTS idx_waiting_type
ON waiting_periods(waiting_period_type);

-- =========================
-- BENEFITS
-- =========================

CREATE INDEX IF NOT EXISTS idx_benefit_policy
ON benefits(policy_id);

CREATE INDEX IF NOT EXISTS idx_benefit_name
ON benefits(benefit_name);

-- =========================
-- RIDERS
-- =========================

CREATE INDEX IF NOT EXISTS idx_rider_policy
ON riders(policy_id);

-- =========================
-- ADD ONS
-- =========================

CREATE INDEX IF NOT EXISTS idx_addon_policy
ON add_ons(policy_id);

-- =========================
-- ELIGIBILITY
-- =========================

CREATE INDEX IF NOT EXISTS idx_eligibility_policy
ON eligibility(policy_id);

-- =========================
-- PREMIUMS
-- =========================

CREATE INDEX IF NOT EXISTS idx_premium_policy
ON premiums(policy_id);

CREATE INDEX IF NOT EXISTS idx_premium_age
ON premiums(minimum_age, maximum_age);

CREATE INDEX IF NOT EXISTS idx_premium_suminsured
ON premiums(sum_insured);

-- =========================
-- PREMIUM RULES
-- =========================

CREATE INDEX IF NOT EXISTS idx_rule_policy
ON premium_rules(policy_id);

-- =========================
-- DISEASES
-- =========================

CREATE INDEX IF NOT EXISTS idx_disease_name
ON diseases(disease_name);

CREATE INDEX IF NOT EXISTS idx_disease_category
ON diseases(disease_category);

-- =========================
-- DISEASE COVERAGES
-- =========================

CREATE INDEX IF NOT EXISTS idx_dc_policy
ON disease_coverages(policy_id);

CREATE INDEX IF NOT EXISTS idx_dc_disease
ON disease_coverages(disease_id);

-- =========================
-- CLAIMS
-- =========================

CREATE INDEX IF NOT EXISTS idx_claim_policy
ON claims(policy_id);

-- =========================
-- HOSPITAL NETWORK
-- =========================

CREATE INDEX IF NOT EXISTS idx_hospital_policy
ON hospital_network(policy_id);

CREATE INDEX IF NOT EXISTS idx_cashless
ON hospital_network(cashless_available);

-- =========================
-- USERS
-- =========================

CREATE INDEX IF NOT EXISTS idx_user_email
ON users(email);

CREATE INDEX IF NOT EXISTS idx_user_active
ON users(active);

-- =========================
-- USER PROFILE
-- =========================

CREATE INDEX IF NOT EXISTS idx_profile_user
ON user_profiles(user_id);

CREATE INDEX IF NOT EXISTS idx_profile_city
ON user_profiles(city);

-- =========================
-- USER REQUIREMENTS
-- =========================

CREATE INDEX IF NOT EXISTS idx_requirement_user
ON user_requirements(user_id);

-- =========================
-- RECOMMENDATIONS
-- =========================

CREATE INDEX IF NOT EXISTS idx_rec_user
ON recommendations(user_id);

CREATE INDEX IF NOT EXISTS idx_rec_policy
ON recommendations(policy_id);

CREATE INDEX IF NOT EXISTS idx_rec_score
ON recommendations(overall_score DESC);

-- =========================
-- AI SCORES
-- =========================

CREATE INDEX IF NOT EXISTS idx_score_policy
ON ai_scores(policy_id);

CREATE INDEX IF NOT EXISTS idx_score_overall
ON ai_scores(overall_score DESC);

-- =========================
-- DOCUMENT CHUNKS
-- =========================

CREATE INDEX IF NOT EXISTS idx_chunk_policy
ON document_chunks(policy_id);

CREATE INDEX IF NOT EXISTS idx_chunk_document
ON document_chunks(document_id);

-- =========================
-- VECTOR SEARCH
-- =========================

CREATE INDEX IF NOT EXISTS idx_embedding_chunk
ON vector_embeddings(chunk_id);

CREATE INDEX IF NOT EXISTS idx_embedding_vector
ON vector_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- =========================
-- INGESTION
-- =========================

CREATE INDEX IF NOT EXISTS idx_job_status
ON ingestion_jobs(ingestion_status);

CREATE INDEX IF NOT EXISTS idx_job_company
ON ingestion_jobs(company_name);

-- =========================
-- AUDIT
-- =========================

CREATE INDEX IF NOT EXISTS idx_audit_table
ON audit_logs(table_name);

CREATE INDEX IF NOT EXISTS idx_audit_record
ON audit_logs(record_id);

-- =========================
-- VERIFICATION
-- =========================

CREATE INDEX IF NOT EXISTS idx_verify_policy
ON verification_status(policy_id);

CREATE INDEX IF NOT EXISTS idx_verify_status
ON verification_status(verification_status);

-- ============================================================
-- FULL TEXT SEARCH
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_policy_search
ON policies
USING GIN(to_tsvector('english', searchable_text));

CREATE INDEX IF NOT EXISTS idx_coverage_search
ON coverages
USING GIN(to_tsvector('english', searchable_text));

CREATE INDEX IF NOT EXISTS idx_exclusion_search
ON exclusions
USING GIN(to_tsvector('english', searchable_text));

CREATE INDEX IF NOT EXISTS idx_benefit_search
ON benefits
USING GIN(to_tsvector('english', searchable_text));