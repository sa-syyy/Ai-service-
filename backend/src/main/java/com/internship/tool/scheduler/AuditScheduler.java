package com.internship.tool.scheduler;

import com.internship.tool.entity.AuditItem;
import com.internship.tool.repository.AuditItemRepository;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;

@Component
public class AuditScheduler {

    private final AuditItemRepository repository;

    public AuditScheduler(AuditItemRepository repository) {
        this.repository = repository;
    }

    @Scheduled(cron = "0 30 9 * * ?") // test every 10 sec
    public void checkOverdueItems() {
       LocalDateTime now = LocalDateTime.now();
    LocalDateTime nextWeek = now.plusDays(7);

    List<AuditItem> items = repository.findUpcomingItems(now, nextWeek);

    items.forEach(item -> {
        System.out.println("Upcoming: " + item.getTitle());
    });
    }
}