package com.mae;

import io.prometheus.client.Gauge;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller {

    static final Gauge classical = Gauge.build()    
    .name("classical").help("help")
    .labelNames("size").register();

    static final Gauge incremental = Gauge.build()  
    .name("incremental").help("help")
    .labelNames("size").register();

    static final Gauge temp1_4 = Gauge.build()  
    .name("temp1_4").help("help")
    .labelNames("approach").register();

    static final Gauge temp1_2 = Gauge.build()  
    .name("temp1_2").help("help")
    .labelNames("approach").register();

    static final Gauge temp = Gauge.build()  
    .name("temp").help("help")
    .labelNames("approach", "size").register();

    @RequestMapping(path= "temp/{size}/{approach}/{value}")
    public String temp(@PathVariable String size,@PathVariable String approach, @PathVariable String value){

        temp.labels(approach, size).set(Double.valueOf(value));

        return classical.toString();

    }

    @RequestMapping(path= "temp1_4/{approach}/{value}")
    public String temp1_4cont(@PathVariable String approach, @PathVariable String value){

        temp1_4.labels(approach).set(Double.valueOf(value));

        return classical.toString();

    }
    @RequestMapping(path= "temp1_2/{approach}/{value}")
    public String temp1_2cont(@PathVariable String approach, @PathVariable String value){

        temp1_2.labels(approach).set(Double.valueOf(value));

        return classical.toString();

    }


    @RequestMapping(path= "/classical/{size}")
    public String classicController(@PathVariable String size){

        classical.labels(size).inc();

        return classical.toString();

    }

    @RequestMapping(path= "/incremental/{size}")
    public String incrementalController(@PathVariable String size){

        incremental.labels(size).inc();

        return(incremental.toString());
    }

    @RequestMapping(path= "set/incremental/{size}")
    public String setincrementalController(@PathVariable String size){

        incremental.labels(size).set(160);

        return(incremental.toString());
    }

}
