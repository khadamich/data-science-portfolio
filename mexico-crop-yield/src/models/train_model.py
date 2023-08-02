import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib

import sys

sys.path.append("..")
from utility import plot_settings
from utility.visualize import (
    plot_predicted_vs_true,
    regression_scatter,
    plot_residuals,
    plot_results_yearly,
)


dataset = pd.read_pickle("../../data/processed/01_processed_data.pickle")

dataset = dataset.drop(columns="crop", axis=1)

train, test = train_test_split(
    dataset, train_size=0.70, test_size=0.30, random_state=42
)


def get_labels(df):
    result = df.pop("yield")
    result = np.array(result)

    return result


train_Y = get_labels(train)
test_Y = get_labels(test)

# ========================================================================================
# Random Forest Rregression
# ========================================================================================
rf_base = RandomForestRegressor(random_state=42)

rf_base.fit(train, train_Y)

predictions = rf_base.predict(test)

print("R2 on training set: ", round(rf_base.score(train, train_Y), 3))
print("R2 on test set: ", round(rf_base.score(test, test_Y), 3))

print("mean_squared_error : ", mean_squared_error(test_Y, predictions, squared=False))
print("mean_absolute_error : ", mean_absolute_error(test_Y, predictions))

# visualization
plot_predicted_vs_true(test_Y, predictions)
regression_scatter(test_Y, predictions)
plot_residuals(test_Y, predictions)
plot_results_yearly(test, test_Y, predictions)

# ========================================================================================
# Exporting Model
# ========================================================================================

ref_cols = list(train.columns)
target = "yield"
joblib.dump(value=[rf_base, ref_cols, target], filename="../../models/model.pkl")
