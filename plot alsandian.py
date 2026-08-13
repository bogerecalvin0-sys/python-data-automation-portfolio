import pandas as pd
import matplotlib.pyplot as plt

# --- COPY THIS DATASET ---
store_data = {
    "City": [
        "New York", "New York",
        "Los Angeles", "Los Angeles",
        "Chicago", "Chicago",
        "Houston", "Houston"
    ],
    "Quarter": ["Q1", "Q2", "Q1", "Q2", "Q1", "Q2", "Q1", "Q2"],
    "Revenue": [15000, 18000, 12000, 14500, 9000, 11000, 8500, 9500]
}

df = pd.DataFrame(store_data)
# -------------------------
mydf = df.groupby(["City","Quarter"])["Revenue"].sum()
mydf.unstack().plot(kind="barh", color="darkorange")

plt.title("Revenue per City")
plt.xlabel("Revenue")
plt.ylabel("City")
plt.grid(axis="x",linestyle=":")
plt.tight_layout()


plt.show()