import pandas as pd

# ---------------------------------------------------------------------------------------
# Importing all the datasets
# Sources: https://www.fao.org/faostat, https://tradingeconomics.com/mexico/precipitation
# ---------------------------------------------------------------------------------------

temperature = pd.read_csv("../../data/raw/mexico_average_temperature.csv")
rainfall = pd.read_csv("../../data/raw/mexico_avg_precipitation.csv")
pesticides_per_crop_area = pd.read_csv("../../data/raw/mexico_pesticides_per_crop_area.csv") #kg/ha pf pesticides
crop_land = pd.read_csv("../../data/raw/mexico_crop_land.csv") #1000ha units
crop_yield = pd.read_csv("../../data/raw/mexico_crop_yield.csv")

# ---------------------------------------------------------------------------------------
# Calculating the total tones of pesticides used per year
# ---------------------------------------------------------------------------------------

pests = pesticides_per_crop_area[["Year","Value"]]
cropl = crop_land[["Year", "Value"]].query("Year > 1989").reset_index(drop = True)

years = [x for x in range(1990,2022)]
tonnes_of_pesticides = []

for i in range(len(pests)):
    
    val = round((pests["Value"].iloc[i])*(cropl["Value"].iloc[i])*(1000)*0.00110231,2)
    tonnes_of_pesticides.append(val)

dic = {"year": years, "pesticides_tones": tonnes_of_pesticides}

pesticides = pd.DataFrame(data=dic)

# ---------------------------------------------------------------------------------------
# Making a new crop yield dataset
# ---------------------------------------------------------------------------------------

crop_yield = crop_yield.query("Year > 1989")[["Item", "Year", "Value"]].reset_index(drop = True)
crop_yield.rename(columns = {'Item':'crop', 'Year':'year', 'Value':'yield'}, inplace = True)

# Converting yield from 100g/ha to kg/ha
crop_yield['yield'] =  crop_yield['yield']/10

# ---------------------------------------------------------------------------------------
# Making pretty the temperature and rainfall datasets
# ---------------------------------------------------------------------------------------

temperature.rename(columns = {'Category':'year', 'Annual Mean':'avg_temp'}, inplace = True)
temperature.drop(columns='5-yr smooth', inplace=True)
temperature = temperature.query("year > 1989").reset_index(drop = True)

rainfall = rainfall[["year","precipitation_mm"]]

# ---------------------------------------------------------------------------------------
# Mergin all the datasets together
# ---------------------------------------------------------------------------------------

dataset = pd.merge(crop_yield, rainfall)
dataset = pd.merge(dataset, pesticides)
dataset = pd.merge(dataset, temperature)

dataset = dataset.sort_values(by = ['crop','year']).reset_index(drop = True)

#yield (kg/ha)
dataset.to_pickle("../../data/interim/01_iterim_dataset.pkl")

dataset.to_csv("../../data/dashboard/dataset.csv", index=False)
temperature.to_csv("../../data/dashboard/temperature.csv", index=False)
rainfall.to_csv("../../data/dashboard/rainfall.csv", index=False)
pesticides.to_csv("../../data/dashboard/pesticides.csv", index=False)

