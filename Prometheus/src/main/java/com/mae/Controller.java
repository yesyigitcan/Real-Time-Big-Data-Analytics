package com.mae;

import io.prometheus.client.Gauge;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller {

    static final Gauge temp1_4 = Gauge.build()  
    .name("temp1_4").help("help")
    .labelNames("approach").register();

    static final Gauge temp1_2 = Gauge.build()  
    .name("temp1_2").help("help")
    .labelNames("approach").register();

    static final Gauge temp = Gauge.build()  
    .name("temp").help("help")
    .labelNames("approach").register();

    static final Gauge elderlySensor1_4 = Gauge.build()  
    .name("elderlySensor1_4").help("help")
    .labelNames("approach").register();

    static final Gauge elderlySensor1_2 = Gauge.build()  
    .name("elderlySensor1_2").help("help")
    .labelNames("approach").register();

    static final Gauge elderlySensor = Gauge.build()  
    .name("elderlySensor").help("help")
    .labelNames("approach").register();

    @RequestMapping(path= "temp/{size}/{approach}/{value}")
    public String temp(@PathVariable String size,@PathVariable String approach, @PathVariable String value){
        Double d = Double.parseDouble(value);

        switch (Integer.parseInt(size)) {
            case 1:
               temp.labels(approach).set(d);
              break;
            case 2:
              temp1_2.labels(approach).set(d);
              break;
            case 4:
              temp1_4.labels(approach).set(d);
              break;
          }
        return d.toString();
    }
    @RequestMapping(path= "elderlySensor/{size}/{approach}/{value}")
    public String elderlySensor(@PathVariable String size,@PathVariable String approach, @PathVariable String value){
        Double d = Double.parseDouble(value);

        switch (Integer.parseInt(size)) {
            case 1:
               elderlySensor.labels(approach).set(d);
              break;
            case 2:
              elderlySensor1_2.labels(approach).set(d);
              break;
            case 4:
              elderlySensor1_4.labels(approach).set(d);
              break;
          }
        return d.toString();
    }

}
