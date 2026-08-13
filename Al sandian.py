import pandas as pd
import tkinter as tk
from pandastable import Table

# 1. Raw Data Lists
employees = [
    'M.Daryah', 'Ozan Kabalik', 'Mohammad Elnoubi', 'Monther', 'Amir',
    'Ashiq', 'Islam mansur', 'Calvin', 'Najat', 'Noryah', 'Asiimwe', 'Saponah'
]
salary = [
    '20000', '15000', '4000', '3500', '3500', '2500', '2500',
    '1700', '3000', '2500', '1700', '2500'
]
position = [
    'General_Manager', 'Show_Room_Manager', 'Sales_Man', 'Sales_Man', 'Sales_Man',
    'Fixer', 'Fixer', 'Fixer', 'Maid', 'Maid', 'Fixer', 'Maid'
]

# 2. Create the Table (DataFrame)
df = pd.DataFrame({
    'Employees': employees,
    'Salary': salary,
    'Position': position
})

# 3. Clean up the Data
df['Salary'] = df['Salary'].astype(int)  # Convert text numbers to real math numbers
df = df.sort_values(by='Salary', ascending=False).reset_index(drop=True)  # Sort highest to lowest

print("--- Full Employee List ---")
print(df)

# 4. --- Group Employees and Salaries Under Each Sector ---
print("\n🏢 EMPLOYEES AND SALARIES BY SECTOR:")

# .groupby('Position') splits the table into sectors automatically
for sector, group in df.groupby('Position'):
    print(f"\n📁 SECTOR: {sector.upper()}")
    print("-" * 45)

    # Loop through the employees inside this specific sector
    for index, row in group.iterrows():
        print(f"   👤 {row['Employees']:<20} | 💰 Salary: {row['Salary']}")

    print("-" * 45)

# 5. --- Filters ---

# Filter 1: Find employees earning more than 3000
high_salary_df = df[df['Salary'] > 3000]
print('\n💰 Employees earning more than 3000:')
print(high_salary_df)

# Filter 2: Find employees earning more than 1500
above_1500_df = df[df['Salary'] > 1500]
print('\n📈 Employees earning more than 1500:')
print(above_1500_df)

# Filter 3: Find employees whose position is Sales_Man
sales_df = df[df['Position'].str.upper() == "SALES_MAN"]
print('\n💼 Employees in Sales:')
print(sales_df)

# Filter 4: Get the top 3 highest earners using index positions
top_3_df = df.head(3)
print('\n🏆 Top 3 Highest Earners:')
print(top_3_df)

# 6. Export Results to CSV File
df.to_csv('employees.csv', index=False)
print("\n💾 Data successfully saved to employees.csv")

# 7. Open the Visual GUI Window
print("\n🖥️ Opening the visual table window... Close the window to stop the script.")
root = tk.Tk()
root.title("Employee Management System")
root.geometry("600x400")  # Sets a nice start window size

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

pt = Table(frame)
pt.model.df = pd.read_csv('employees.csv')  # Loads the saved data file
pt.show()

root.mainloop()





