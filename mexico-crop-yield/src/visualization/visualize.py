import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
import sys
import os
import datetime

import plot_settings


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


dataset = pd.read_pickle("../../data/interim/01_iterim_dataset.pkl")

# -----------------------------------------------------------------------------------------
# Function to create the plots of all features per year
# -------------------------------------------------------------------------------------


def yearly_data(dataset):
    df = (
        dataset.groupby("year")
        .aggregate(
            {
                "yield": "sum",
                "precipitation_mm": "mean",
                "pesticides_tones": "mean",
                "avg_temp": "mean",
            }
        )
        .reset_index()
    )
    # -------------------------------------------------------------------------------------
    # Total Crop Yield
    # -------------------------------------------------------------------------------------
    mean = df["yield"].mean()

    # Create Canvas
    fig, ax1 = plt.subplots()

    # Make plots
    ax1.plot(
        df["year"],
        df["yield"],
        color="#63b6c0",
        label="Crop Yield (hg/ha)",
        linewidth=2,
    )
    ax1.axhline(
        y=mean, color="#c73734", linestyle="dashed", label="Mean Value", linewidth=2
    )

    # Set Legends and formats
    plt.xticks(df["year"].unique())
    fig.autofmt_xdate()
    ax1.legend()

    fig.suptitle(f"Total crop yield in Mexico between 1990 and 2021")

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])

    export_figure(filename=f"total-crop-yield")

    # -------------------------------------------------------------------------------------
    # Rainfall
    # -------------------------------------------------------------------------------------
    fig, ax1 = plt.subplots()

    # Make plots
    ax1.bar(df["year"], df["precipitation_mm"], color="#63b6c0", label="Rainfall (mm)")

    # Set Legends and formats
    # ax1.set_ylabel('mm of rain', color = 'black')
    plt.xticks(df["year"].unique())
    fig.autofmt_xdate()
    # ax1.legend()
    ax1.set_ylim(600, 900)
    fig.suptitle(f"Average Rainfall in Mexico between 1990 and 2021")

    export_figure(filename=f"avg-rainfall")

    # -------------------------------------------------------------------------------------
    # Pesticides Tones
    # -------------------------------------------------------------------------------------
    fig, ax1 = plt.subplots()

    # Make plots
    ax1.bar(df["year"], df["pesticides_tones"], color="#c73734", label="Rainfall (mm)")

    # Set Legends and formats
    # ax1.set_ylabel('mm of rain', color = 'black')
    plt.xticks(df["year"].unique())
    fig.autofmt_xdate()
    # ax1.legend()
    # ax1.set_ylim(600,900)
    fig.suptitle(f"Total tons of pesticides used in Mexico between 1990 and 2021")

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])

    export_figure(filename=f"tons-of-pesticides")

    # -------------------------------------------------------------------------------------
    # Avg Temperature
    # -------------------------------------------------------------------------------------
    # Create Canvas
    fig, ax1 = plt.subplots()

    # Make plots
    ax1.bar(df["year"], df["avg_temp"], color="#63b6c0")

    # Set Legends and formats
    ax1.set_ylim(20.5, 22.25)
    plt.xticks(df["year"].unique())
    fig.autofmt_xdate()

    fig.suptitle(f"Average temperature in Mexico between 1990 and 2021")

    export_figure(filename=f"avg-temperature")


def yield_per_crop(dataset):
    # country = dataset["country"].unique()[0]
    for crop in dataset["crop"].unique():
        df = dataset.query(f"crop == '{crop}'")

        # Get the mean for plots
        mean = df["yield"].mean()

        # Create Canvas
        fig, ax1 = plt.subplots()

        # Make plots
        ax1.plot(
            df["year"],
            df["yield"],
            color="#63b6c0",
            label="Crop Yield (hg/ha)",
            linewidth=2,
        )
        ax1.axhline(
            y=mean, color="#c73734", linestyle="dashed", label="Mean Value", linewidth=2
        )

        # Set Legends and formats
        # ax1.set_xlabel('Year', color = 'black')
        plt.xticks(df["year"].unique())
        fig.autofmt_xdate()
        ax1.legend()

        fig.suptitle(f"{crop} crop yield in Mexico between 1990 and 2021")

        current_values = plt.gca().get_yticks()
        plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])

        # Export figure
        export_figure(filename=f"{crop}_crop_yield")


df = (
    dataset.groupby("crop")["yield"]
    .sum()
    .reset_index()
    .sort_values(by="yield", ascending=False)
)
