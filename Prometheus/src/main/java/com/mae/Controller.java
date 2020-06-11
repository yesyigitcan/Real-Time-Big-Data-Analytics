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

    static final Gauge temp1_4_acc = Gauge.build()  
    .name("temp1_4_acc").help("help")
    .labelNames("approach").register();

    static final Gauge temp1_2 = Gauge.build()  
    .name("temp1_2").help("help")
    .labelNames("approach").register();

    static final Gauge temp1_2_acc = Gauge.build()  
    .name("temp1_2_acc").help("help")
    .labelNames("approach").register();

    static final Gauge temp = Gauge.build()  
    .name("temp").help("help")
    .labelNames("approach").register();

    static final Gauge temp_acc = Gauge.build()  
    .name("temp_acc").help("help")
    .labelNames("approach").register();


    static final Gauge elderlySensor = Gauge.build()  
    .name("elderlySensor").help("help")
    .labelNames("approach").register();

    static final Gauge elderlySensor_acc = Gauge.build()  
    .name("elderlySensor_acc").help("help")
    .labelNames("approach").register();

    @RequestMapping(path= "temp/{size}/{approach}/{m}/{value}")
    public String temp(@PathVariable String size,@PathVariable String approach, @PathVariable String m, @PathVariable String value){
        Double d = Double.parseDouble(value);
        boolean mse;
        if (m.equals("mse")) {
          mse = true;
        } else if (m.equals("acc")) {
          mse = false;
        }else{
          return( m + "tipinde bir metrik bulunmamaktadir");
        }

        switch (Integer.parseInt(size)) {
            case 1:
              if(mse){
                temp.labels(approach).set(d);
              }else{
                temp_acc.labels(approach).set(d);
              }
              break;
            case 2:
              if (mse) {
                temp1_2.labels(approach).set(d);  
              } else {
                temp1_2_acc.labels(approach).set(d);
              }
              break;
            case 4:
              if (mse) {
                temp1_4.labels(approach).set(d);  
              } else {
                temp1_4_acc.labels(approach).set(d);
              }
              break;
          }
        return d.toString();
    }
    @RequestMapping(path= "elderlySensor/{size}/{approach}/{m}/{value}")
    public String elderlySensor(@PathVariable String size,@PathVariable String approach,@PathVariable String m, @PathVariable String value){
        Double d = Double.parseDouble(value);
        boolean mse;
        if (m.equals("mse")) {
          mse = true;
        } else if (m.equals("acc")) {
          mse = false;
        }else{
          return( m + "tipinde bir metrik bulunmamaktadir");
        }
        if(mse){
          elderlySensor.labels(approach).set(d);
        }else{
          elderlySensor_acc.labels(approach).set(d);
        }
        

        return d.toString();
    }

}
