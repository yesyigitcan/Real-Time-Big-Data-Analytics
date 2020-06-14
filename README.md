# Real-Time-Big-Data-Analytics


## Change Log
- Temperature dataset transferred to the database
- Created views for 1/4 and 1/2 of the dataset
- Compared classical regression algorithms (SVR, Random Forest, KNN, Linear Regression, Decision Tree, BayesianRidge) 
- Compared incremental regression algorithms (KNN, Linear Regression)
- Results are stored in log files
- Metrics used to monitor are determined
- Java Spring Boot, Prometheus and Grafana has been set
- Communication of model between server is established

### Comparision (KNN - MSE)
<table>
  <tr>
    <td>Size</td>
    <td>Classical</td>
    <td>Incremental</td>
  </tr>
  <tr>
    <td>1/4</td>
    <td>0.0023362620786537875</td>
    <td>0.0017933643463437154</td>
  </tr>
  <tr>
    <td>1/2</td>
    <td>0.002533177912238008</td>
    <td>0.0006445322069547691</td>
  </tr>
  <tr>
    <td>1</td>
    <td>0.0013868631250914226</td>
    <td>0.0002303573580481708</td>
  </tr>
</table>

### Dataset Links
Activity Recognition Exp (Classification, Real-Time) - https://archive.ics.uci.edu/ml/datasets/Heterogeneity+Activity+Recognition
Elderly Sensor Data (Classification, Real-Time) - https://archive.ics.uci.edu/ml/datasets/Activity+recognition+with+healthy+older+people+using+a+batteryless+wearable+sensor<br>
Electric Motor Temperature (Regression) - https://www.kaggle.com/wkirgsn/electric-motor-temperature
