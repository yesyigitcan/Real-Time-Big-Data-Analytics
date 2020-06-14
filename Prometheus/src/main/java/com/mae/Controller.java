package com.mae;

import io.prometheus.client.Gauge;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class Controller {

    static final Gauge temp1_4_m1 = Gauge.build()  
    .name("temp1_4_m1").help("help")
    .labelNames("approach").register();

    static final Gauge temp1_4_m2 = Gauge.build()  
    .name("temp1_4_m2").help("help")
    .labelNames("approach").register();

    static final Gauge temp1_2_m1 = Gauge.build()  
    .name("temp1_2_m1").help("help")
    .labelNames("approach").register();

    static final Gauge temp1_2_m2 = Gauge.build()  
    .name("temp1_2_m2").help("help")
    .labelNames("approach").register();

    static final Gauge temp_m1 = Gauge.build()  
    .name("temp_m1").help("help")
    .labelNames("approach").register();

    static final Gauge temp_m2 = Gauge.build()  
    .name("temp_m2").help("help")
    .labelNames("approach").register();


    static final Gauge elderlySensor_m1 = Gauge.build()  
    .name("elderlySensor_m1").help("help")
    .labelNames("approach").register();

    static final Gauge elderlySensor_m2 = Gauge.build()  
    .name("elderlySensor_m2").help("help")
    .labelNames("approach").register();

    static final Gauge activity_m1 = Gauge.build()  
    .name("activity_m1").help("help")
    .labelNames("approach").register();

    static final Gauge activity_m2 = Gauge.build()  
    .name("activity_m2").help("help")
    .labelNames("approach").register();

    @RequestMapping(path= "temp/{size}/{approach}/{m}/{value}")
    public String temp(@PathVariable String size,@PathVariable String approach, @PathVariable String m, @PathVariable String value){
        Double d = Double.parseDouble(value);
        boolean mse;
        if (m.equals("m1")) {
          mse = true;
        } else if (m.equals("m2")) {
          mse = false;
        }else{
          return( m + "tipinde bir metrik bulunmamaktadir");
        }

        switch (Integer.parseInt(size)) {
            case 1:
              if(mse){
                temp_m1.labels(approach).set(d);
              }else{
                temp_m2.labels(approach).set(d);
              }
              break;
            case 2:
              if (mse) {
                temp1_2_m1.labels(approach).set(d);  
              } else {
                temp1_2_m2.labels(approach).set(d);
              }
              break;
            case 4:
              if (mse) {
                temp1_4_m1.labels(approach).set(d);  
              } else {
                temp1_4_m2.labels(approach).set(d);
              }
              break;
          }
        return d.toString();
    }
    @RequestMapping(path= "elderlySensor/{size}/{approach}/{m}/{value}")
    public String elderlySensor(@PathVariable String size,@PathVariable String approach,@PathVariable String m, @PathVariable String value){
        Double d = Double.parseDouble(value);
        boolean mse;
        if (m.equals("m1")) {
          mse = true;
        } else if (m.equals("m2")) {
          mse = false;
        }else{
          return( m + "tipinde bir metrik bulunmamaktadir");
        }
        if(mse){
          elderlySensor_m1.labels(approach).set(d);
        }else{
          elderlySensor_m2.labels(approach).set(d);
        }
        return d.toString();
    }

    @RequestMapping(path= "activity/{size}/{approach}/{m}/{value}")
    public String activity(@PathVariable String size,@PathVariable String approach,@PathVariable String m, @PathVariable String value){
        Double d = Double.parseDouble(value);
        boolean mse;
        if (m.equals("m1")) {
          mse = true;
        } else if (m.equals("m2")) {
          mse = false;
        }else{
          return( m + "tipinde bir metrik bulunmamaktadir");
        }
        if(mse){
          activity_m1.labels(approach).set(d);
        }else{
          activity_m2.labels(approach).set(d);
        }
        return d.toString();
    }

}
