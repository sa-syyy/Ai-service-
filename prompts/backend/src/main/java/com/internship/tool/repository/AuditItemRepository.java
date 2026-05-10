package com.internship.tool.repository;
import java.time.LocalDateTime;
import java.util.List;
import org.springframework.data.jpa.repository.Query;
//import org.springframework.data.repository.query.Param;
import com.internship.tool.entity.AuditItem;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;


import java.time.LocalDateTime;

public interface AuditItemRepository extends JpaRepository<AuditItem, Long> {

    // 🔍 Search with pagination
    @Query("SELECT a FROM AuditItem a WHERE LOWER(a.title) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(a.description) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    Page<AuditItem> search(String keyword, Pageable pageable);

    // 📊 Filter by status (with pagination)
    Page<AuditItem> findByStatus(String status, Pageable pageable);

    // 📅 Date range filter (with pagination)
    Page<AuditItem> findByCreatedAtBetween(LocalDateTime start, LocalDateTime end, Pageable pageable);

    // 🧩 Combined filter (status + date range)
    @Query("SELECT a FROM AuditItem a WHERE a.status = :status AND a.createdAt BETWEEN :start AND :end")
    Page<AuditItem> findByStatusAndDateRange(String status, LocalDateTime start, LocalDateTime end, Pageable pageable);

    // ⚡ Soft delete filter
    Page<AuditItem> findByIsDeletedFalse(Pageable pageable);

    @Query("SELECT a FROM AuditItem a WHERE a.dueDate < :now AND a.status != 'COMPLETED'")
      List<AuditItem> findOverdueItems(LocalDateTime now);

@Query("SELECT a FROM AuditItem a WHERE a.dueDate BETWEEN :start AND :end")
       List<AuditItem> findUpcomingItems(LocalDateTime start, LocalDateTime end);

long countByStatus(String status);
}