import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def plot_predicted_vs_true(y_test, y_pred, sort=True):
    """
    Plot the results from a regression model in a plot to compare the prediction vs. acutal values

    Args:
        y_test : actual values
        y_pred : model predictions
        sort (bool, optional): Sort the values. Defaults to True.
    """
    # Create canvas
    plt.figure(figsize=(20, 5))

    t = pd.DataFrame({"y_pred": y_pred, "y_test": y_test})
    if sort:
        t = t.sort_values(by=["y_test"])

    plt.plot(t["y_test"].to_list(), label="True", marker="o", linestyle="none")
    plt.plot(
        t["y_pred"].to_list(),
        label="Prediction",
        marker="o",
        linestyle="none",
        color="purple",
    )
    plt.ylabel("Value")
    plt.xlabel("Observations")
    plt.title("Predict vs. True")
    plt.legend()
    plt.show()


def regression_scatter(y_test, y_pred):
    """
    Plot the results from a regression model in a scatter plot to compare the prediction vs. acutal values.
    Additionally, plots the regression line and ideal fit line.

    Args:
        y_test : actual values
        y_pred : model predictions
    """

    # Create canvas
    plt.figure(figsize=(20, 5))

    # Plot scatter
    plt.scatter(y_test, y_pred)

    # Plot diagonal line (perfect fit)
    z = np.polyfit(y_test, y_test, 1)
    p = np.poly1d(z)
    plt.plot(
        y_test, p(y_test), color="gray", linestyle="dotted", linewidth=3, label="Ideal"
    )

    # Overlay the regression line
    z = np.polyfit(y_test, y_pred, 1)
    p = np.poly1d(z)
    plt.plot(y_test, p(y_test), color="#4353ff", label="Predicted", alpha=0.5)

    plt.xlabel("Actual Value")
    plt.ylabel("Predicted Value")
    plt.title("Predicted vs. True")
    plt.legend()
    plt.show()


def plot_residuals(y_test, y_pred, bins=25):
    """
    Plot residuals of a regression model. A good model will have a residuals
    distribution that peaks at zero with few residuals at the extremes.

    Args:
        y_test : actual values
        y_pred : model predictions
        bins (int, optional). Defaults to 25.
    """

    residuals = y_test - y_pred

    plt.figure(figsize=(20, 5))
    plt.hist(residuals, bins=bins, rwidth=0.95)
    plt.title("Residual Histogram")
    plt.show()


def plot_results_yearly(test, test_Y, predictions):
    df = test.copy()
    df["yield"] = test_Y
    df["yield_predicted"] = predictions

    df = (
        df.groupby("year")
        .aggregate(
            {
                "yield": "sum",
                "yield_predicted": "sum",
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
    mean_predicted = df["yield_predicted"].mean()

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

    ax1.plot(
        df["year"],
        df["yield_predicted"],
        color="#33658c",
        label="Crop Yield Predicted",
        linewidth=2,
    )

    # Set Legends and formats
    plt.xticks(df["year"].unique())
    fig.autofmt_xdate()
    ax1.legend()

    fig.suptitle(f"Total crop yield: Predicted vs True")

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])

    print("Mean value: ", mean)
    print("Mean predicted value: ", mean_predicted)

    plt.show()


# Export figures
def export_figure(filename):
    date = datetime.date.today().strftime("%d-%m-%Y")
    path = f"../../reports/figures/{date}"

    if os.path.exists(path):
        plt.savefig(path + "/" + filename + ".png", bbox_inches="tight")

    if not os.path.exists(path):
        os.makedirs(path)
        plt.savefig(path + "/" + filename + ".png", bbox_inches="tight")

    print(f"Succesfully export {filename}")
