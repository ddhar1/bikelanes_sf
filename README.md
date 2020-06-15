# Understanding impact of bike lanes vs Traffic Accidents

I used data the city of San Francisco to see if there was correlations between the number of traffic accidents and whether or not a bike lane was on a road.

## Data
* Bike lane Data (where bike lanes are, when installed, length of bike lane) was from DataSF
* Traffic Accidents data, was subsetted from a list of Police Reports, again from DataSF

## Outline of analysis vs Files
`01_DataCleaning.ipynb` - This python workbook is the preliminary data cleaning work I have been doing in order to examine the impact of additional bike lanesin SF on accident rates. I use bike lane data, traffic reports filed by the police.
`02_Analysis` - preliminary charts to show how bike lanes vary with bike lane data, given time of day, neighborhood in SF, and year
`03_Analysis_StdMetric' - I realize in the previous analysis that there is a lot more roads without a bike lane than with a bike lane. I standardize the number of accidents by amount of road type (by bike lane length of group if on a bike lane vs regular road if not on a bike lane). 
* I notice that while there are more accidents off a bike lane with this metric when aggregated by district
* but effect reverses when we split data on time of day and by district 
* A regression (with controls for year, length of road) estimates that there are more accidents off a bike lane than on a bike lane, and bike lanes decrease accidents

## Next Steps:
Overall, it's hard to estimate the impact of bike lanes on accidents because there is a lot of variation in the data. A simple regrssion. But possible next steps I would do are
* Cut standardized metric data by district and by Year
* Add to the regression
	* add a control for ratio of bike lane to length of road 