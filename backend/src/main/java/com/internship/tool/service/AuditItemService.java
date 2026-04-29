package com.internship.tool.service;
import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import com.internship.tool.entity.AuditItem;
import com.internship.tool.repository.AuditItemRepository;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;

@Service
public class AuditItemService {

    private final AuditItemRepository repository;
    private final AuditLogRepository auditLogRepository;
 public AuditItemService(AuditItemRepository repository, AuditLogRepository auditLogRepository) {
    this.repository = repository;
    this.auditLogRepository = auditLogRepository;
}

    // 🔄 UPDATE
    @Transactional
public AuditItem update(Long id, AuditItem updated) {
    AuditItem existing = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Item not found"));

    // Save old value (for audit)
    String oldTitle = existing.getTitle();

    // Update fields
    existing.setTitle(updated.getTitle());
    existing.setDescription(updated.getDescription());
    existing.setStatus(updated.getStatus());
    existing.setPriority(updated.getPriority());
    existing.setScore(updated.getScore());
    existing.setCategory(updated.getCategory());
    existing.setAssignedTo(updated.getAssignedTo());
    existing.setUpdatedAt(LocalDateTime.now());

    AuditItem saved = repository.save(existing);

    // 🔥 ADD THIS (AUDIT LOG)
    AuditLog log = new AuditLog();
    log.setAuditItemId(id);
    log.setAction("UPDATE");
    log.setOldValue(oldTitle);
    log.setNewValue(updated.getTitle());
    log.setChangedBy("system");
    log.setChangedAt(LocalDateTime.now());

    auditLogRepository.save(log);

    return saved;
}

    // ❌ SOFT DELETE
    @Transactional
public void softDelete(Long id) {
    AuditItem item = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Item not found"));

    item.setIsDeleted(true);
    item.setUpdatedAt(LocalDateTime.now());

    repository.save(item);

    // 🔥 ADD THIS (AUDIT LOG)
    AuditLog log = new AuditLog();
    log.setAuditItemId(id);
    log.setAction("DELETE");
    log.setOldValue("ACTIVE");
    log.setNewValue("DELETED");
    log.setChangedBy("system");
    log.setChangedAt(LocalDateTime.now());

    auditLogRepository.save(log);
}
}