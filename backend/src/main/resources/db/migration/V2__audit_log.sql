CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,

    audit_item_id BIGINT,

    action VARCHAR(50), -- CREATE, UPDATE, DELETE

    old_value TEXT,
    new_value TEXT,

    changed_by VARCHAR(100),

    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_item ON audit_log(audit_item_id);
CREATE INDEX idx_audit_log_action ON audit_log(action);
CREATE INDEX idx_audit_log_time ON audit_log(changed_at);