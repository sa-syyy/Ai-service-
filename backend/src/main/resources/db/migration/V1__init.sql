CREATE TABLE audit_item (
    id BIGSERIAL PRIMARY KEY,

    title VARCHAR(255) NOT NULL,
    description TEXT,

    status VARCHAR(50) NOT NULL,
    priority VARCHAR(50),

    score NUMERIC(5,2),
    category VARCHAR(100),

    assigned_to VARCHAR(100),

    due_date TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    created_by VARCHAR(100),
    updated_by VARCHAR(100),

    is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_audit_status ON audit_item(status);
CREATE INDEX idx_audit_category ON audit_item(category);
CREATE INDEX idx_audit_due_date ON audit_item(due_date);
CREATE INDEX idx_audit_created_at ON audit_item(created_at);