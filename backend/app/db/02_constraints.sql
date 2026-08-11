-- ============================================================
-- 02_constraints.sql
-- FOREIGN KEYS
-- ============================================================

-- =========================
-- POLICIES
-- =========================

ALTER TABLE policies
ADD CONSTRAINT fk_policy_company
FOREIGN KEY (company_id)
REFERENCES companies(company_id)
ON DELETE CASCADE;

ALTER TABLE policies
ADD CONSTRAINT fk_policy_category
FOREIGN KEY (category_id)
REFERENCES categories(category_id)
ON DELETE SET NULL;

ALTER TABLE policies
ADD CONSTRAINT fk_policy_status
FOREIGN KEY (status_id)
REFERENCES policy_status(status_id)
ON DELETE SET NULL;

-- =========================
-- POLICY DOCUMENTS
-- =========================

ALTER TABLE policy_documents
ADD CONSTRAINT fk_document_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- COVERAGES
-- =========================

ALTER TABLE coverages
ADD CONSTRAINT fk_coverage_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

ALTER TABLE coverages
ADD CONSTRAINT fk_coverage_disease
FOREIGN KEY (disease_id)
REFERENCES diseases(disease_id)
ON DELETE SET NULL;

-- =========================
-- EXCLUSIONS
-- =========================

ALTER TABLE exclusions
ADD CONSTRAINT fk_exclusion_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

ALTER TABLE exclusions
ADD CONSTRAINT fk_exclusion_disease
FOREIGN KEY (disease_id)
REFERENCES diseases(disease_id)
ON DELETE SET NULL;

-- =========================
-- WAITING PERIODS
-- =========================

ALTER TABLE waiting_periods
ADD CONSTRAINT fk_waiting_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- BENEFITS
-- =========================

ALTER TABLE benefits
ADD CONSTRAINT fk_benefit_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- RIDERS
-- =========================

ALTER TABLE riders
ADD CONSTRAINT fk_rider_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- ADDONS
-- =========================

ALTER TABLE add_ons
ADD CONSTRAINT fk_addon_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- ELIGIBILITY
-- =========================

ALTER TABLE eligibility
ADD CONSTRAINT fk_eligibility_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- PREMIUMS
-- =========================

ALTER TABLE premiums
ADD CONSTRAINT fk_premium_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- PREMIUM RULES
-- =========================

ALTER TABLE premium_rules
ADD CONSTRAINT fk_rule_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- DISEASE COVERAGES
-- =========================

ALTER TABLE disease_coverages
ADD CONSTRAINT fk_dc_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

ALTER TABLE disease_coverages
ADD CONSTRAINT fk_dc_disease
FOREIGN KEY (disease_id)
REFERENCES diseases(disease_id)
ON DELETE CASCADE;

ALTER TABLE disease_coverages
ADD CONSTRAINT fk_dc_coverage
FOREIGN KEY (coverage_id)
REFERENCES coverages(coverage_id)
ON DELETE SET NULL;

-- =========================
-- CLAIMS
-- =========================

ALTER TABLE claims
ADD CONSTRAINT fk_claim_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- HOSPITAL NETWORK
-- =========================

ALTER TABLE hospital_network
ADD CONSTRAINT fk_hospital_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- USER PROFILE
-- =========================

ALTER TABLE user_profiles
ADD CONSTRAINT fk_profile_user
FOREIGN KEY (user_id)
REFERENCES users(user_id)
ON DELETE CASCADE;

-- =========================
-- USER REQUIREMENTS
-- =========================

ALTER TABLE user_requirements
ADD CONSTRAINT fk_requirement_user
FOREIGN KEY (user_id)
REFERENCES users(user_id)
ON DELETE CASCADE;

-- =========================
-- RECOMMENDATIONS
-- =========================

ALTER TABLE recommendations
ADD CONSTRAINT fk_rec_user
FOREIGN KEY (user_id)
REFERENCES users(user_id)
ON DELETE CASCADE;

ALTER TABLE recommendations
ADD CONSTRAINT fk_rec_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- RECOMMENDATION REASONS
-- =========================

ALTER TABLE recommendation_reasons
ADD CONSTRAINT fk_reason
FOREIGN KEY (recommendation_id)
REFERENCES recommendations(recommendation_id)
ON DELETE CASCADE;

-- =========================
-- AI SCORES
-- =========================

ALTER TABLE ai_scores
ADD CONSTRAINT fk_score_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- POLICY COMPARISON
-- =========================

ALTER TABLE policy_comparisons
ADD CONSTRAINT fk_compare_user
FOREIGN KEY (user_id)
REFERENCES users(user_id)
ON DELETE CASCADE;

ALTER TABLE policy_comparisons
ADD CONSTRAINT fk_compare_policy1
FOREIGN KEY (policy_one)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

ALTER TABLE policy_comparisons
ADD CONSTRAINT fk_compare_policy2
FOREIGN KEY (policy_two)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

-- =========================
-- DOCUMENT CHUNKS
-- =========================

ALTER TABLE document_chunks
ADD CONSTRAINT fk_chunk_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

ALTER TABLE document_chunks
ADD CONSTRAINT fk_chunk_document
FOREIGN KEY (document_id)
REFERENCES policy_documents(document_id)
ON DELETE CASCADE;

-- =========================
-- VECTOR EMBEDDINGS
-- =========================

ALTER TABLE vector_embeddings
ADD CONSTRAINT fk_embedding_chunk
FOREIGN KEY (chunk_id)
REFERENCES document_chunks(chunk_id)
ON DELETE CASCADE;

-- =========================
-- VERIFICATION
-- =========================

ALTER TABLE verification_status
ADD CONSTRAINT fk_verify_policy
FOREIGN KEY (policy_id)
REFERENCES policies(policy_id)
ON DELETE CASCADE;

ALTER TABLE verification_status
ADD CONSTRAINT fk_verify_user
FOREIGN KEY (verified_by)
REFERENCES users(user_id)
ON DELETE SET NULL;

-- =========================
-- AUDIT
-- =========================

ALTER TABLE audit_logs
ADD CONSTRAINT fk_audit_user
FOREIGN KEY (performed_by)
REFERENCES users(user_id)
ON DELETE SET NULL;

-- ============================================================
-- UNIQUE CONSTRAINTS
-- ============================================================

ALTER TABLE companies
ADD CONSTRAINT uq_company_name UNIQUE(company_name);

ALTER TABLE categories
ADD CONSTRAINT uq_category UNIQUE(category_name);

ALTER TABLE diseases
ADD CONSTRAINT uq_disease UNIQUE(disease_name);

ALTER TABLE policy_status
ADD CONSTRAINT uq_status UNIQUE(status_name);

ALTER TABLE users
ADD CONSTRAINT uq_user_email UNIQUE(email);

-- ============================================================
-- CHECK CONSTRAINTS
-- ============================================================

ALTER TABLE premiums
ADD CONSTRAINT chk_premium_positive
CHECK (premium_amount >= 0);

ALTER TABLE premiums
ADD CONSTRAINT chk_suminsured_positive
CHECK (sum_insured >= 0);

ALTER TABLE policies
ADD CONSTRAINT chk_age
CHECK (
minimum_entry_age IS NULL
OR
maximum_entry_age IS NULL
OR
minimum_entry_age <= maximum_entry_age
);

ALTER TABLE recommendations
ADD CONSTRAINT chk_rank
CHECK (recommendation_rank > 0);

ALTER TABLE ai_scores
ADD CONSTRAINT chk_overall_score
CHECK (
overall_score >= 0
AND
overall_score <= 100
);

ALTER TABLE companies
ADD CONSTRAINT chk_founded_year
CHECK (
founded_year IS NULL
OR
founded_year >= 1800
);

ALTER TABLE premiums
ADD CONSTRAINT chk_gst
CHECK (
gst IS NULL
OR
gst >= 0
);