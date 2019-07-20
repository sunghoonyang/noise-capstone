# Rapid Response for DEP Noise Complaints
*Abstract is Extracted from the third progress report:*
>In New York City, the Department of Environmental Protection (DEP) handles outdoor noise complaints from sources ranging from construction activity to the jingle of ice cream trucks. In recent years, the growing volume of noise complaints has increased the agency’s response times and hindered enforcement of the city’s noise code. This capstone project aims to provide a data-driven approach to optimize the DEP’s processes to better address noise complaints. To accomplish this, we will cluster noise complaints spatially and temporally. We will then deploy a random forest classifier to assign a priority to each cluster based on enforceability, previous complaint resolutions, and sponsor parameters. Based on our discussion with domain experts and preliminary analysis, we anticipate that our clustering model will more accurately identify enforceable and high-priority complaint clusters than models that assign priority to complaints based on other factors. The intended implications of this work are to shorten complaint time to resolution, reduce the complaint backlog, and increase the issuance of violations.
CUSP Class of 2019 Urban Noise Capstone. 

Team consists of five CUSP graduate students: 
* [Qinyu Goh](https://github.com/qygoh) (qg412@nyu.edu)
* [Zoe Martiniak](https://github.com/zem232) (zem232@nyu.edu)
* [Sam Ovenshine](https://github.com/sgo230) (sgo230@nyu.edu)
* [Siddhanth Shetty](https://github.com/sds695) (sds695@nyu.edu)
* [Sung Hoon Yang](https://github.com/sunghoonyang) (shy256@nyu.edu)

## Documentation & Resources 
Documentation & Resources are open to all NYU community.
* [Report](https://docs.google.com/document/d/1uN8fs5w_1YlJJBLZ3DBpJ3Uq2PPScutX_RQZJz5hgXA/edit?usp=sharing)
* [Homepage](https://zem232.github.io/NoiseCapstone/)
* [Google Drive](https://drive.google.com/drive/u/1/folders/1hE8ACy-bLxxMTJOs6yDrhvv0HL-LEQNd)
  * [Data Repository](https://drive.google.com/drive/u/1/folders/15MM0D5h5BRfnbwTcVhP7jVNy2Tbpr1Oc)
   * [Data aggregated with respect to Neighborhood Tabulation Area](https://drive.google.com/drive/u/1/folders/1V9VlLeKNtd5Dnlim_X-Ri0s4N13TPgMs)

## Tools & Deliverables
* After Hour Variance scraper that collects DOB's [After Hour Variance Permits](https://www1.nyc.gov/site/buildings/business/after-hours-variances.page) data published in [DOB website](http://a810-bisweb.nyc.gov/bisweb/bispi00.jsp).
* Department of Transportation (DOT) permits scraper (please check [README.md](https://github.com/sunghoonyang/noise-capstone/tree/master/dot_scraper) for more info)
* Neural Network for Spatiotemporal Forecasting of Noise Complaint Volume
  * [PyTorch Train & Test Suites](https://github.com/sunghoonyang/noise-capstone/blob/master/analysis/311/nn/vanilla_lstm_model-NTA-MN_ONLY_MSE.ipynb)
  * [Data Wrangling for Neural Network](https://github.com/sunghoonyang/noise-capstone/blob/master/analysis/311/nn/vanilla_lstm_model-NTA-MN_ONLY_data_wrangling.ipynb)
* [Tableau View for dashboarding](https://github.com/sunghoonyang/noise-capstone/tree/master/dashboard)
