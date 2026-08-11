-- ============================================================
-- 04_seed.sql
-- MASTER DATA
-- ============================================================

----------------------------
-- POLICY STATUS
----------------------------

INSERT INTO policy_status(status_name, description) VALUES
('Active','Currently available'),
('Discontinued','No longer sold'),
('Coming Soon','Upcoming policy'),
('Under Review','Verification pending')
ON CONFLICT DO NOTHING;

----------------------------
-- CATEGORIES
----------------------------

INSERT INTO categories(category_name,category_description) VALUES
('Health Insurance','Individual Health Plans'),
('Family Floater','Family Health Insurance'),
('Critical Illness','Critical Illness Plans'),
('Personal Accident','Accident Insurance'),
('Senior Citizen','Senior Citizen Plans'),
('Top Up','Top Up Plans'),
('Super Top Up','Super Top Up Plans'),
('Maternity','Maternity Plans'),
('Travel Insurance','Travel Insurance'),
('Cancer Care','Cancer Insurance')
ON CONFLICT DO NOTHING;

----------------------------
-- SAMPLE DISEASES
----------------------------

INSERT INTO diseases(disease_name,disease_category) VALUES
('Diabetes','Metabolic'),
('Hypertension','Cardiac'),
('Asthma','Respiratory'),
('Cancer','Critical Illness'),
('Kidney Failure','Renal'),
('Stroke','Neurology'),
('Heart Attack','Cardiac'),
('Liver Disease','Gastroenterology'),
('Thyroid Disorder','Endocrine'),
('Tuberculosis','Infectious')
ON CONFLICT DO NOTHING;