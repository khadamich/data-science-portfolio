# Mexico Crop Yield Modeling
## Author: Michell Martinez
You can see the [repository structure](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/references/folder_structure.txt) in the [references](https://github.com/khadamich/data-science-portfolio/tree/main/mexico-crop-yield/references) section.

## Contents
- [Introduction](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/README.md#introduction)
  - [Dataset Overview](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/README.md#dataset-overview)
- [Exploratory Data Analysis](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/README.md#exploratory-data-analysis)
- [Model](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/README.md#model)
- [Results](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/README.md#results)

## Introduction
Agriculture feeds the global community. Discover what’s driving the production, trade, prices, and performance of corn, sugar, soybeans, pork, vegetable oils, and other food commodities, is one of the hottest topics in this area.

In this project I devoloped a `Random Forest Regression` model to predict the yearly crop yield of the primary crops in Mexico. To do this, I made usage of the [Food and Agriculture Organization of the United Nations](https://www.fao.org/faostat/en/#data) dataset to get the crop yield for every primary crop produced in Mexico between 1990 and 2021, as well as the land usage and the pesticidades usage per crop area in the same period.

### Dataset Overview
- **Year** (Numerical): from 1990 to 2021.
- **Crop** (Categorical): more than 100 primary crop types.
- **Crop Yield** (Numerical): kg/ha of crop production per year.
- **Avg. Rainfall** (Numerical): Average mm of rainfall per year in Mexico.
- **Tons of pesticides** (Numerical): total tons of pesticides used per year in Mexico.

## Exploratory Data Analysis

The dataset for exploratory data analysis is in the [iterim](https://github.com/khadamich/data-science-portfolio/tree/main/mexico-crop-yield/data/interim) folder.
Here is a picture of the [dashboard](https://lookerstudio.google.com/s/nMt8RVmK9J4) in `Looker Studio` just to have a brief glance of the features and the behavior of the data.

![Screenshot 2023-08-02 at 12 53 26](https://github.com/khadamich/data-science-portfolio/assets/132023832/d26cab4c-927a-4849-ad2b-2c4e92b10e30)

The following figures are some examples of the plots I made with the [scripts](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/src/visualization/visualize.py) in the [visualization](https://github.com/khadamich/data-science-portfolio/tree/main/mexico-crop-yield/src/visualization) section.

![Lemons and Limes](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/Lemons%20and%20limes_crop_yield.png)

![Crop yield](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/total-crop-yield.png)

## Model

Due the nature of the dataset, where I have a lot different primary crop types, I choosed to modeling the cropy yield with `Random Forest Regressor` [package](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) due it's affordabilty to handle multi colinearity between features. 

### Metrics
The metrics achieved with this model where:

- R2 on training set:  0.995
- R2 on test set:  0.974
- mean_squared_error :  2120.43
- mean_absolute_error :  1146.95

The following figures show a brief overview of the behavior of the model on `test dataset`

### Predict vs. True values (sorted)

![Predict vs. True](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/predicted-vs-true.png)

### Regression Scatter

![Regression scatter](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/regression-scatter.png)

### Histogram with residuals

![residuals](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/residuals.png)

## Results

The following figures shows the predictions of the model for some crops.

![P1](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/total-crop-yield-prediction.png)

![P2](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/prediction-Watermelons.png)

![P3](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/prediction-Raspberries.png)

![P4](https://github.com/khadamich/data-science-portfolio/blob/main/mexico-crop-yield/figures/prediction-Natural%20rubber%20in%20primary%20forms.png)
