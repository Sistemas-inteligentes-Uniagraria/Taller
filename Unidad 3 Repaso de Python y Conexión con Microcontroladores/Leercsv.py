import pandas as pd
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) 
file_name = os.path.join(script_dir, "ldr_data.csv") 

df = pd.read_csv(file_name, names=["Timestamp", "LDR"])

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

plt.style.use("dark_background")

plt.figure(figsize=(10,5))
plt.plot(df["Timestamp"], df["LDR"], label="LDR %", color="blue")
plt.xlabel("Tiempo")
plt.ylabel("Valor LDR")
plt.title("Valores LDR")
plt.legend()
plt.grid()
plt.xticks(rotation=45)

plt.ylim(0, 100)

plt.show()