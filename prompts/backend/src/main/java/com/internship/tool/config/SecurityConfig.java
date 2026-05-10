package com.internship.tool.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import jakarta.servlet.Filter;

@Configuration
public class SecurityConfig {

    @Bean
    public Filter jwtFilter() {
        return new JwtFilter();
    }
}