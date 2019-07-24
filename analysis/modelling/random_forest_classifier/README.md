# Modelling enforceability- A Random Forest Classifier Approach 
This main goal of this segment is to factor in features based on the location and times of the noise complaints so as to be able to guess whether new complaints will be enforcable or not. 

## This segment is divided into three sections:

### Feature Engineering
The first section deals with getting 2016 complaints and features related to each complaint. Here we join the complaints to:
* American Community Survey(ACS) based on the location of complaints
* Primary Land Use Tax Lot Output(PLUTO) based on the location of complaints
* NOAA Weather data based on the time of complaints
* After Hour Variance(AHV) permits: AHV permits are what allow construction jobs to take place after hours. A construction taking place after this without a permit would be enforceable by the DEP. These permits are not publicly available so we had to make use of a scraper to obtain these permits. For historical data we made use of the scraper  Assigning AHV permits to complaints was done in another notebook.

A key step in the feature engineering was mapping the resolution description of the closed complaints to 1 or 2 based on enforceability. For example the resolution description "The Department of Environmental Protection observed a violation of the New York City Air/Noise Code at the time of inspection and issued a notice of violation." was assigned as 1 whereas "The Department of Environmental Protection scheduled an inspection." was assigned to 2 as the goal is to close more complaints.


AHV Assignment:

The after hour variance permits are what allows a construction to be done after hours. The DEP indicated that this could be a useful tool to identify enforceable complaints. However since this data is not publicly available we had to make use of data scraped by NYU researcher Fabio Miranda(https://engineering.nyu.edu/student/fabio-miranda). This scraper had complaints only until mid-2017 and we had to scrape the permits for the 2019 data. Each of these files had differences in format and were tackled in separate notebooks(ahv_assignment_2016.ipynb and ahv_assignment_2019.ipynb).


### Modelling
In the second section we test out models to maximize the F1-Score which is the harmonic mean between Precision and Accuracy. Here we decided to use the random forest classifier as we had multiple variables and wanted our model to be robust to noise in the data.

The problem we faced with the the data from 2016 was that out of 46332 only 1470 complaints were enforceable. Training on the data with random sampling gives us a model that misclassifies a lot of enforceable complaints as unenforceable(high precision, low recall). To be able to capture more of the enforceable complaints at the risk of classifying unenforceable complaints as enforceable(low precision, high recall) we built a training set with equal number of enforceable and unenforceable complaints. We received feeback from the DEP that they think the second model would be more useful to them as they can then verify if these complaints are actually enforceable.

Our initial training was done using 660 features which could be overfitting the training data. We trained another model on the top 10 features by feature importance from the first model which performed better than the model with 660 features.

We finally tested our models on only construction complaints to see if that would improve our performance which we learned it did not.

In the end we decided to go with the model trained on all types of noise complaints using training data containing equal number of enforceable and uneforceable complaints with the top 10 features by feature importance.

### Testing on newer data
The third section uses the model trained on 2016 data and tests it on the last week of 2019 June. Here we increased the enforceability probabilities based on whether construction related complaints took place after hours and if they had a permit. We also created a field that would identify if two construction complaints were within 300 metres of each other(approxiamately one block) as this could mean they are from the same source of noise.  

Note: The notebooks were written following PEP8 guidelines.
