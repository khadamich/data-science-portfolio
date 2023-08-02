import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

import sys
import os
import datetime

sys.path.append("..")
from utility import plot_settings
from utility.visualize import (
    plot_predicted_vs_true,
    regression_scatter,
    plot_residuals,
)

# ========================================================================================
# functions
# ========================================================================================


# Function to export figures in the correct path and format
def export_figure(filename):
    date = datetime.date.today().strftime("%d-%m-%Y")
    path = f"../../reports/figures/{date}"

    if os.path.exists(path):
        plt.savefig(path + "/" + filename + ".png", bbox_inches="tight")

    if not os.path.exists(path):
        os.makedirs(path)
        plt.savefig(path + "/" + filename + ".png", bbox_inches="tight")

    print(f"Succesfully export {filename}")


# function to plot predicted vs true values
def plot_results_yearly_per_crop(crop, Y, predictions):
    new_sample = dataset.query(f"crop == '{crop}'")

    mean = round(Y.mean(), 2)
    mean_predicted = round(predictions.mean(), 2)
    rscore = round(r2_score(Y, predictions), 3)

    # Create Canvas
    fig, ax1 = plt.subplots()

    # Make plots
    ax1.plot(
        new_sample["year"],
        Y,
        color="#63b6c0",
        label=f"Actual values",
        linewidth=3,
    )

    ax1.plot(
        new_sample["year"],
        predictions,
        color="#c73734",
        label=f"Predicted values",
        linewidth=2,
        linestyle="dashed",
    )
    ax1.plot([], [], " ", label=f"R2 score: {rscore}")

    # Set Legends and formats
    plt.xticks(new_sample["year"].unique())
    fig.autofmt_xdate()
    ax1.legend()

    fig.suptitle(f"Predicted vs True Total crop yield for {crop}")

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])

    print("Mean value: ", mean)
    print("Mean predicted value: ", mean_predicted)

    export_figure(filename=f"prediction-{crop}")


# Function to plot total vals
def plot_results_yearly(Y, predictions):
    dataset["yield_predicted"] = predictions
    df = (
        dataset.groupby("year")
        .aggregate(
            {
                "yield": "sum",
                "yield_predicted": "sum",
            }
        )
        .reset_index()
    )

    mean = round(Y.mean(), 2)
    mean_predicted = round(predictions.mean(), 2)
    rscore = round(r2_score(Y, predictions), 3)

    # Create Canvas
    fig, ax1 = plt.subplots()

    # Make plots
    ax1.plot(
        df["year"],
        df["yield"],
        color="#63b6c0",
        label=f"Actual values",
        linewidth=3,
    )

    ax1.plot(
        df["year"],
        df["yield_predicted"],
        color="#c73734",
        label=f"Predicted values",
        linewidth=2,
        linestyle="dashed",
    )
    ax1.plot([], [], " ", label=f"R2 score: {rscore}")

    # Set Legends and formats
    plt.xticks(df["year"].unique())
    fig.autofmt_xdate()
    ax1.legend()

    fig.suptitle(f"Predicted vs. True Total Crop Yield")

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])

    print("Mean value: ", mean)
    print("Mean predicted value: ", mean_predicted)
    export_figure(filename=f"total-crop-yield-prediction")


# ========================================================================================
# Load Data
# ========================================================================================

dataset = pd.read_pickle("../../data/processed/01_processed_data.pickle")
# crop = "Almonds, in shell"
# new_sample = dataset.query(f"crop == '{crop}'")

# ========================================================================================
# Load Model
# ========================================================================================

model, ref_cols, target = joblib.load("../../models/model.pkl")

# ========================================================================================
# Make Predictions
# ========================================================================================

X = dataset[ref_cols]
Y = dataset[target]
predictions = model.predict(X)

print("R2 on test set: ", r2_score(Y, predictions))
print("mean_squared_error : ", mean_squared_error(Y, predictions, squared=False))
print("mean_absolute_error : ", mean_absolute_error(Y, predictions))

# visualization
plot_predicted_vs_true(Y, predictions)
regression_scatter(Y, predictions)
plot_residuals(Y, predictions)
plot_results_yearly(Y, predictions)

# ========================================================================================
# Function to make predictions for a given crop
# ========================================================================================


def predict_crop(crop):
    new_sample = dataset.query(f"crop == '{crop}'")

    # ========================================================================================
    # Make Predictions
    # ========================================================================================

    X = new_sample[ref_cols]
    Y = new_sample[target]
    predictions = model.predict(X)

    print("R2 on test set: ", r2_score(Y, predictions))
    print("mean_squared_error : ", mean_squared_error(Y, predictions, squared=False))
    print("mean_absolute_error : ", mean_absolute_error(Y, predictions))

    # visualization
    # plot_predicted_vs_true(Y, predictions)
    # regression_scatter(Y, predictions)
    # plot_residuals(Y, predictions)
    plot_results_yearly_per_crop(crop, Y, predictions)


for crop in dataset["crop"].unique():
    predict_crop(crop)


# ========================================================================================
# Most accurate crop
# ========================================================================================


def model_crop_r2score(crop):
    new_sample = dataset.query(f"crop == '{crop}'")

    X = new_sample[ref_cols]
    Y = new_sample[target]
    predictions = model.predict(X)

    r2score = r2_score(Y, predictions)

    return r2score


def most_accurate_crop():
    r2scores = []
    for crop in dataset["crop"].unique():
        if model_crop_r2score(f"{crop}") in range(-1, 1):
            r2scores.append(abs(model_crop_r2score(f"{crop}")))
        else:
            r2scores.append(model_crop_r2score(f"{crop}"))

    for i in range(len(r2scores)):
        if r2scores[i] == max(r2scores):
            print("r2 score: ", max(r2scores))
            return dataset["crop"].unique()[i]


most_accurate_crop()
