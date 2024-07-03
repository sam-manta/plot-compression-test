import os, re
import matplotlib.pyplot as plt
import numpy as np
import glob
import pandas as pd
import math


def read_file_content(filep):
    headers = ("CMOD", "Displacement", "Force", "Time")
    dat_file = glob.glob(os.path.join(filep, "*.dat"))
    content = pd.read_csv(dat_file[0], sep="\t", decimal=",", skiprows=5, names=headers)
    df = pd.DataFrame(content)
    # Convert all values in the DataFrame to numeric
    df = df.apply(pd.to_numeric)
    return df


def plot_mm_vs_kn(mm, kn, title):
    # Convert mm and kN to float for plotting
    # [mm,kn] = filter_outliers(mm, kn)
    kn = -kn
    max_Force = np.max(kn)
    max_mm = mm[np.argmax(kn)]

    plt.figure(figsize=(10, 6))
    plt.plot(
        mm, kn, marker=".", linestyle="None", color="#2C7FB8", label=title, markersize=4
    )
    plt.title(r"Wedge Splitting Test", fontsize=14)
    plt.xlabel(r"Crack opening [mm]", fontsize=12)
    plt.ylabel(r"Force [kN]", fontsize=12)
    plt.grid(True)
    plt.minorticks_on()
    plt.legend(fontsize=12)
    plt.annotate(
        f"Max Value: {max_Force:.2f}",
        xy=(max_mm, max_Force),
        xytext=(max_mm, max_Force - 1),
        arrowprops=dict(
            facecolor="#7FCDBB", shrink=0.2, width=0.5, headwidth=4, edgecolor="#7FCDBB"
        ),
        fontsize=12,
    )
    # Save the plot in PDF format
    filename = f"{title}{'.pdf'}"
    plt.savefig(filename, format="pdf")
    plt.show()
    plt.close()


def plot_mm_vs_Fs(mm, kn, title):
    # Convert mm and kN to float for plotting
    # [mm,kn] = filter_outliers(mm, kn)
    kn = -kn * 1.866
    max_Force = np.max(kn)
    max_mm = mm[np.argmax(kn)]
    mm_int = mm - mm[0]
    kn_int = kn - kn[0]
    integral = np.trapz(kn_int, mm_int)
    # Area can be taken from a separate file
    h_cut = 75
    l = 150
    fracture_energy = integral / h_cut / l * 1000000  # (kN*mm/mm^2-> N/m)

    plt.figure(figsize=(10, 6))
    plt.plot(
        mm, kn, marker=".", linestyle="None", color="#2C7FB8", label=title, markersize=4
    )
    plt.title(r"Wedge Splitting Test", fontsize=14)
    plt.xlabel(r"Crack opening [mm]", fontsize=12)
    plt.ylabel(r"Force [kN]", fontsize=12)
    plt.grid(True)
    plt.minorticks_on()
    plt.legend(fontsize=12)
    plt.annotate(
        f"Max Value: {max_Force:.2f}",
        xy=(max_mm, max_Force),
        xytext=(max_mm, max_Force - 0.5),
        arrowprops=dict(
            facecolor="#7FCDBB", shrink=0.2, width=0.5, headwidth=5, edgecolor="#7FCDBB"
        ),
        fontsize=12,
    )
    plt.annotate(f"Fracture energy: {fracture_energy:.2f} N/m", xy=(0.5, 5))
    # Save the plot in PDF format
    # Save the plot in PDF format
    filename = f"{title}{'wedge.pdf'}"
    plt.savefig(filename, format="pdf")
    plt.show()

    plt.close()


# define plotting
plt.rc("text", usetex=True)
plt.rc("font", family="serif")
directory = os.getcwd()
all_items = os.listdir(directory)
folders = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]
# Store the folder names in a variable
# headers = ["Ch 1 CMOD (mm)", "Ch 1 Displacement (mm)", "Ch 1 Force (kN)", "Time (s)"]
for i in range(len(folders)):
    title = folders[i]
    filep = os.path.join(directory, title)
    table_data = read_file_content(filep)
    print(table_data["Force"])
    #   plot_mm_vs_kn(table_data['CMOD'], table_data['Force'],title)
    plot_mm_vs_Fs(table_data["CMOD"], table_data["Force"], title)
