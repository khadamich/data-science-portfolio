import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

dataset = pd.read_pickle("../../data/interim/01_iterim_dataset.pkl")


def make_dataset(dataset):
    le = LabelEncoder()
    dataset["crop_cat"] = le.fit_transform(dataset["crop"])

    # features = dataset[["yield","year","country_cat","crop_cat","average_rain_fall_mm_per_year","avg_temp", "pesticides_tonnes"]]

    dataset.to_pickle("../../data/processed/01_processed_data.pickle")

    return dataset


make_dataset(dataset)
