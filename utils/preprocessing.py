
# Step 1: Import pandas
import pandas as pd
new_data = pd.read_csv("data/newPrices.csv")

used_data = pd.read_csv("data/usedPrices.csv")


# Step 4: Display new EV data
print("NEW EV DATA")
print(new_data.head())

# Step 5: Display used EV data
print("\nUSED EV DATA")
print(used_data.head())


# Step 6: Check missing values
print("\nMissing values in New EV data")
print(new_data.isnull().sum())

print("\nMissing values in Used EV data")
print(used_data.isnull().sum())


# Step 7: Remove duplicate records
new_data = new_data.drop_duplicates()
used_data = used_data.drop_duplicates()


# Step 8: Remove rows with missing values
new_data = new_data.dropna()
used_data = used_data.dropna()


# Step 9: Display dataset information
print("\nNew EV dataset size:", new_data.shape)
print("Used EV dataset size:", used_data.shape)


print("\nData preprocessing completed!")
# Understand the datasets

print("\nNEW EV COLUMNS")
print(new_data.columns)

print("\nUSED EV COLUMNS")
print(used_data.columns)
print("\nNEW EV INFORMATION")
new_data.info()

print("\nUSED EV INFORMATION")
used_data.info()

print("\nNEW EV STATISTICS")
print(new_data.describe())

print("\nUSED EV STATISTICS")
print(used_data.describe())
