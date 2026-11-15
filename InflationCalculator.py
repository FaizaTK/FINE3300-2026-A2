'''
Assignment-2- Consumer Price Index (CPI) and Inflation Calculator
Faiza Tasnim Khandaker
'''

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#PART-1: Reading and preparing CPI Data

def load_cpi_data(folder):
    df = pd.read_csv(folder / "STATIC_INFLATIONCALC.csv", skiprows=8)

    #Dropping any duplicate data and only keeping the first one each month 
    df["month"] = df["date"].str[:7]
    df = df.drop_duplicates(subset="month", keep="first")
    return df

#PART-2: Calculating Yearly CPI Changes 
def calculate_yearly_changes(df):

    cpi_values = np.array(df["STATIC_INFLATIONCALC"])

    changes = []
    for i in range(len(cpi_values)):
        if i < 12:
            changes.append(None)  #The first 12 months in the data have no previous year CPI for comparison
        else:
            current = cpi_values[i]
            old = cpi_values[i - 12]
            change = (current / old - 1) * 100
            changes.append(change)

    df["Yearly Change (%)"] = changes
    return df

#PART-3: Plotting and saving the CPI graph as per assignment requirement

def create_graph(df, folder):
    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df["date"], df["STATIC_INFLATIONCALC"], label="CPI")

    #Adding a dotted line at the CPI base level
    ax.axhline(y=100, color="gray", linestyle=":", label="CPI Base Level")

    #Plotting annual CPI change on the right axis
    ax2 = ax.twinx()
    ax2.plot(df["date"], df["Yearly Change (%)"], color="red", label="Yearly CPI Change")
    ax2.set_ylabel("Yearly CPI Change (%)")

    ax.set_title("Canadian Consumer Price Index (1914–2026)")
    ax.set_xlabel("Year")
    ax.set_ylabel("CPI (2002 = 100)")

    fig.subplots_adjust(bottom=0.25)
    fig.legend(loc="lower center", ncol=3)

    fig.savefig (folder/"CPI_Inflation_Graph.png", dpi=200)

    #plt.show()  #To open it in Matplotlib viewer

#PART-4: Building the Inflation Calculator like Bank of Canada webpage

def inflation_calculator(df):  

    #Asking the user for and validating the original price and then dates
    try:
        price = input("Enter the original price (CAD): ")
        price = price.replace(",", "").replace(" ", "") #replicating the Bank of Canada input style
        price = float(price)
    except ValueError:
        print("Invalid price. Please enter a number.")
        return

    if price < 0:
        print("Invalid price. Please enter a valid non-negative amount.")
        return

    #Removing spaces before and after the entered dates to match the CPI dataset using strip
    start_date = input("Enter the starting month and year (YYYY-MM): ").strip()
    end_date = input("Enter the ending month and year (YYYY-MM): ").strip()

    #Finding the CPI data for the given months
    start_row = df[df["month"] == start_date]
    end_row = df[df["month"] == end_date]

    #Checking whether both dates exist in the dataset
    if len(start_row) == 0 or len(end_row) == 0:
        print("Invalid date. Please use the required format and a date available in the dataset.")
        return

    beginning_cpi = start_row["STATIC_INFLATIONCALC"].iloc[0]
    closing_cpi = end_row["STATIC_INFLATIONCALC"].iloc[0]

    print("Starting CPI:", beginning_cpi)
    print("Ending CPI:", closing_cpi)

    #Finding the years between the two dates
    year_start = int(start_date[:4])
    month_start = int(start_date[5:7])

    year_end = int(end_date[:4])
    month_end = int(end_date[5:7])

    months = (year_end - year_start) * 12 + (month_end - month_start)
    years = abs(months) / 12  #To keep the year difference positive

    print(f"Difference in years: {years:.2f}")

    #Calculating the inflation adjusted price
    inflation_adjusted_price = price * (closing_cpi / beginning_cpi)
    print(f"Adjusted price: CAD ${inflation_adjusted_price:,.2f}")
    
    #Calculating the percentage change in the prices
    percentage_change = (closing_cpi / beginning_cpi - 1) * 100
    print(f"Percentage change: {percentage_change:.2f}%")
    
    #Calculating the average annual inflation/change rate
    if months == 0:
        annual_rate = 0
    else:
        annual_rate = ((closing_cpi / beginning_cpi) ** (12 / abs(months)) - 1) * 100

    print(f"Average Annual Rate Of Change: {annual_rate:.2f}%")

#Running the four functions in the program
folder = Path(__file__).resolve().parent
df = load_cpi_data(folder)
df = calculate_yearly_changes(df)
create_graph(df, folder)
inflation_calculator(df)
