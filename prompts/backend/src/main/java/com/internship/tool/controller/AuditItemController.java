package com.internship.tool.controller;

import com.internship.tool.entity.AuditItem;
import com.internship.tool.service.AuditItemService;

import jakarta.servlet.http.HttpServletRequest;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/audit")
public class AuditItemController {

    private final AuditItemService service;

    public AuditItemController(AuditItemService service) {
        this.service = service;
    }

    // 🔄 UPDATE API
    @PutMapping("/{id}")
    public AuditItem update(@PathVariable Long id, @RequestBody AuditItem item) {
        return service.update(id, item);
    }

    // ❌ DELETE API (soft delete)
   @DeleteMapping("/{id}")
public String delete(@PathVariable Long id, HttpServletRequest request) {

    String role = (String) request.getAttribute("role");

    if (!"ADMIN".equals(role)) {
        throw new RuntimeException("Access Denied");
    }

    service.softDelete(id);
    return "Deleted successfully";
}
}