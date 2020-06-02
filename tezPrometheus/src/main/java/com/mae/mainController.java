package com.mae;

import io.prometheus.client.spring.boot.EnablePrometheusEndpoint;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
@EnablePrometheusEndpoint
public class mainController {
  
    public static void main(String[] args) {
        SpringApplication.run(mainController.class, args);     
    }

}
