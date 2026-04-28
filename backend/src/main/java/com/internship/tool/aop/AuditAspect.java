package com.internship.tool.aop;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Aspect
@Component
public class AuditAspect {

    private final AuditLogRepository auditLogRepository;

    public AuditAspect(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    @AfterReturning("execution(* com.internship.tool.service.AuditItemService.update(..))")
    public void logUpdate(JoinPoint joinPoint) {

        Long id = (Long) joinPoint.getArgs()[0];

        AuditLog log = new AuditLog();
        log.setAuditItemId(id);
        log.setAction("UPDATE");
        log.setChangedAt(LocalDateTime.now());
        log.setChangedBy("SYSTEM");

        auditLogRepository.save(log);

        System.out.println("AOP: Update logged for ID " + id);
    }

    @AfterReturning("execution(* com.internship.tool.service.AuditItemService.softDelete(..))")
    public void logDelete(JoinPoint joinPoint) {

        Long id = (Long) joinPoint.getArgs()[0];

        AuditLog log = new AuditLog();
        log.setAuditItemId(id);
        log.setAction("DELETE");
        log.setChangedAt(LocalDateTime.now());
        log.setChangedBy("SYSTEM");

        auditLogRepository.save(log);

        System.out.println("AOP: Delete logged for ID " + id);
    }
}