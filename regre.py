import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF


try:
    df = pd.read_csv('products.csv')
    df.columns = df.columns.str.strip()


    required_columns = {'Total_Revenue', 'Total_Profit', 'Units_Sold'}
    if not required_columns.issubset(df.columns):
        raise ValueError("Missing required columns in the dataset")
except Exception as e:
    messagebox.showerror("Error", f"Failed to load dataset")
    exit()

#y=mx + c

y = df['Units_Sold']
x = df[['Total_Revenue', 'Total_Profit']]
model = sm.OLS(y, x).fit()
summary_str = model.summary().as_text()

root = tk.Tk()
root.title('OLS Regression App')
root.geometry("950x950")

data_frame = ttk.Frame(root)
data_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)


data_cols = ["Total_Revenue", "Total_Profit", "Units_Sold"]
data_tree = ttk.Treeview(data_frame, columns=data_cols, show='headings', height=10)
for col in data_cols:
    data_tree.heading(col, text=col)
    data_tree.column(col, width=100)

scrollbar = ttk.Scrollbar(data_frame, orient='vertical', command=data_tree.yview)
data_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
data_tree.pack()


def load_data(rows=10):
    data_tree.delete(*data_tree.get_children())
    data_subset = df[['Total_Revenue', 'Total_Profit', 'Units_Sold']].head(rows)
    for index, row in data_subset.iterrows():
        data_tree.insert("", "end", values=(row["Total_Revenue"], row["Total_Profit"], row["Units_Sold"]))


def update_data():
    try:
        rows = int(row_entry.get())
        load_data(rows)
    except ValueError:
        pass


def show_example_graph():
    plt.figure()
    plt.scatter(y, model.predict(x))
    plt.xlabel('Actual Quantity')
    plt.ylabel('Predicted Quantity')
    plt.title('Actual vs Predicted')
    plt.show()


def show_profit_vs_sales_regression():
    plt.figure()
    sns.regplot(data=df, x='Total_Revenue', y='Total_Profit')
    plt.title('Sales vs Profits')
    plt.show()


def show_smooth_scatter_chart():
    plt.figure()
    sns.kdeplot(data=df, x='Total_Revenue', y='Total_Profit', fill=True)
    plt.title('Density Chart')
    plt.show()


load_data()

summary_frame = ttk.Frame(root)
summary_frame.pack(pady=10)

cols = ['Index', 'Details']
tree = ttk.Treeview(summary_frame, columns=cols, show='headings', height=15)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=300 if col == 'Index' else 500)

summary_scrollbar = ttk.Scrollbar(summary_frame, orient='vertical', command=tree.yview)
tree.configure(yscroll=summary_scrollbar.set)
summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack()

summary_lines = summary_str.split('\n')
for i, line in enumerate(summary_lines):
    tree.insert("", "end", values=(i, line))

row_selection_frame = ttk.Frame(root)
row_selection_frame.pack(pady=5)

ttk.Label(row_selection_frame, text='rows to display;').pack(side=tk.LEFT, padx=5)

row_entry = ttk.Entry(row_selection_frame, width=5)
row_entry.insert(0, '10')
row_entry.pack(side=tk.LEFT)

ttk.Button(row_selection_frame, text='load Data', command=update_data).pack(side=tk.LEFT, padx=5)

btn_example = tk.Button(root, text='Show Example Regrssion Graph', command=show_example_graph)
btn_example.pack(pady=5)

btn_profit_sales = tk.Button(root, text='Show profit vs Regression Graph', command=show_profit_vs_sales_regression)
btn_profit_sales.pack(pady=5)

btn_smooth_scatter = tk.Button(root, text='Show smooth scatter chart', command=show_smooth_scatter_chart)
btn_smooth_scatter.pack(pady=5)


def dataframe_to_pdf(dataframe, pdf_path, title="Data Report"):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()


    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", size=5)
    col_width = pdf.epw / len(dataframe.columns)
    row_height = 8


    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Helvetica", style="B", size=5)
    for column in dataframe.columns:
        pdf.cell(col_width, row_height, str(column), border=1, align="C", fill=True)
    pdf.ln(row_height)


    pdf.set_font("Helvetica", style="", size=5)
    for index, row in dataframe.iterrows():
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1, align="C")
        pdf.ln(row_height)

    pdf.output(pdf_path)

def generate_pdf_report():
    dataframe_to_pdf(df, "report.pdf", "Product Data Report")
    messagebox.showinfo("Export Successful", "Data matrix successfully saved to 'report.pdf'")


btn_pdf = tk.Button(root, text=' Export Clean Table Data to PDF', command=generate_pdf_report)
btn_pdf.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()



    #instead of productdata create the data for sales revenue percentage and sells percentage

