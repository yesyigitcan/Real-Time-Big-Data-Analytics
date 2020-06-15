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

### Comparision Electric Motor Temperature (KNN - MSE)
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

### Comparision Elderly Sensor (DecisionTreeClassifier - Accuracy - Multiclass F Beta Score - MSE)
<table>
  <tr>
    <td>Metric</td>
    <td>Classical</td>
    <td>Incremental</td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td>0.9898358407615052</td>
    <td>0.8471368101589304</td>
  </tr>
  <tr>
    <td>Multiclass F Beta Score</td>
    <td>0.9547341032426812</td>
    <td>0.48519272539744446</td>
  </tr>
  <tr>
    <td>MSE</td>
    <td>0.07498084136651474</td>
    <td>0.46642973138460797</td>
  </tr>
</table>

### Comparision Activity Recognition by Phone Acceloremeter Dataset (DecisionTreeClassifier - Accuracy - Multiclass F Beta Score)
### Comparision Elderly Sensor (DecisionTreeClassifier - Accuracy - Multiclass FBeta Score)
<table>
  <tr>
    <td>Record Number</td>
    <td style="text-align: center; vertical-align: middle;">6000</td>
    <td colspan = "3" style="text-align: center; vertical-align: middle;">348844</td>
  </tr>
  <tr>
    <td>Metric</td>
    <td>Classical</td>
    <td>Incremental (Full Update)</td>
    <td>Incremental (Stop Train when All Class Type is Experienced)</td>
    <td>Incremental (Update Model with Data Rows Catched by System - Randomness)</td>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td>0.8117706747843734</td>
    <td>0.9995518094856023</td>
    <td>0.7003</td>
    <td>0.8912000802729175</td>
  </tr>
  <tr>
    <td>Multiclass F Beta Score</td>
    <td>0.8143</td>
    <td>0.9995290401759328</td>
    <td>0.8219</td>
    <td>0.883180158164952</td>
  </tr>
</table>

### Dataset Links
Activity Recognition Exp (Classification, Real-Time) - https://archive.ics.uci.edu/ml/datasets/Heterogeneity+Activity+Recognition
Elderly Sensor Data (Classification, Real-Time) - https://archive.ics.uci.edu/ml/datasets/Activity+recognition+with+healthy+older+people+using+a+batteryless+wearable+sensor<br>
Electric Motor Temperature (Regression) - https://www.kaggle.com/wkirgsn/electric-motor-temperature
