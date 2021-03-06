# Hearing Noise Complaints

## Data Driven Optimization of Rapid Response to Urban Noise Complaints

*Abstract as extracted from the report:*
> In New York City, the Department of Environmental Protection (DEP) handles outdoor noise
complaints from sources ranging from construction activity to the jingle of ice cream trucks. Since 2010, the growing volume of noise complaints has increased the agency’s response times and hindered enforcement of the city’s noise code. This capstone project provides a data-driven approach to optimize the DEP’s processes to better address noise complaints. To accomplish this, we deployed two machine learning models: an LSTM neural network to predict spatial and temporal complaint volume, and a random forest classifier model to predict complaint enforceability. Model features were 311 complaints, socioeconomics, PLUTO land use, weather conditions, and construction variances. Based on sponsor feedback, we opted for the random forest classifier model and to optimize its performance for recall. In evaluation, the model precision was 9.3% and recall was 91.1%. The model’s enforceability predictions were incorporated into an interactive data visualization for DEP inspectors to identify clusters of unresolved noise complaints with a high likelihood of enforceability. The implications of our work are to improve noise code enforcement and reduce the DEP backlog.

## Team 
Team consists of five CUSP graduate students: 
* [Qinyu Goh](https://github.com/qygoh) (qg412@nyu.edu)
* [Zoe Martiniak](https://github.com/zem232) (zem232@nyu.edu)
* [Sam Ovenshine](https://github.com/sgo230) (sgo230@nyu.edu)
* [Siddhanth Shetty](https://github.com/sds695) (sds695@nyu.edu)
* [Sung Hoon Yang](https://github.com/sunghoonyang) (shy256@nyu.edu)

## Documentation & Resources 
Documentation & Resources are open to all NYU community.
* [Report](./report)
* [Website](https://zem232.github.io/NoiseCapstone/)
* [Exploratory Studies](./analysis/explorative_studies)
  * Exploratory analysis on 311 noise complaints and its relationship with chosen datasets in New York City
* [Data Wrangling Scripts](./data_gen)
* [Google Drive](https://drive.google.com/drive/u/1/folders/1hE8ACy-bLxxMTJOs6yDrhvv0HL-LEQNd)
  * [Data Repository](https://drive.google.com/drive/u/1/folders/15MM0D5h5BRfnbwTcVhP7jVNy2Tbpr1Oc)
    * [Counts of Noise Complaints: Data aggregated with respect to Neighborhood Tabulation Area](https://drive.google.com/drive/u/1/folders/1V9VlLeKNtd5Dnlim_X-Ri0s4N13TPgMs)
    * [National Oceanic and Atmospheric Administration: Weather Data](https://drive.google.com/drive/u/1/folders/1x-fc6ATYnlPxj6ZtLr4FNqhBpCroFXVB)
    * [Census data aggregated with Pluto demarcation](https://drive.google.com/drive/u/1/folders/1rPLzdxa2Wqiifimd5vxwRaqhbZadpPCS)
    * [Zoning District](https://drive.google.com/drive/u/1/folders/187LS_mM0_mMaFlYZaO-0-AHNMOgybnWd)
    * [After Hour Variance Data](https://drive.google.com/open?id=1Qek6XScZBaWsnpAoJOMVvmD8-EKMi82i)

## Tools & Deliverables
* Scrapers
  * After Hour Variance scraper that collects DOB's [After Hour Variance Permits](https://www1.nyc.gov/site/buildings/business/after-hours-variances.page) data published in [DOB website](http://a810-bisweb.nyc.gov/bisweb/bispi00.jsp).
  * Department of Transportation (DOT) permits scraper (please check [README.md](./dot_scraper) for more info)
* Machine Learning Models
  * Neural Network for Spatiotemporal Forecasting of Noise Complaint Volume
    * [PyTorch Train & Test Suites](./analysis/modelling/neural_network/vanilla_lstm_model-NTA-MN_ONLY_MSE.ipynb)
    * [Data Wrangling for Neural Network](./analysis/modelling/neural_network/vanilla_lstm_model-NTA-MN_ONLY_data_wrangling.ipynb)
  * [Random Forest Classifier](./analysis/modelling/random_forest_classifier) to predict enforceability of incoming complaints
* [Tableau View for dashboarding](./dashboard)
