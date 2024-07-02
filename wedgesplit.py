import os, re
import matplotlib.pyplot as plt
import numpy as np
def read_file_content(filep):
    # Initialize a list to hold titles
    table_data = {'CMOD': [], 'Displacement': [], 'Force': [], 'Time': []}
    dat_file = [file for file in filep if file.endswith('.dat')]
    file_path = os.path.join(filep, dat_file)
       
    with open(file_path) as file:
        content = file.read()
        table_started = False
        for line in content.splitlines():
            if table_started:
                data = line.split(None)
                if len(data) >= 3:
                    table_data['mm'].append(data[0].strip())
                    table_data['mm'].append(data[1].strip())
                    table_data['kN'].append(data[2].strip())
                    table_data['s'].append(data[3].strip())
            if re.match(r'"mm"\s*"mm"\s*"?kN"?\s*"?s"?', line):
                table_started = True
    
        return table_data

def convert_to_float(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def filter_outliers(mm, kn, num_std_dev=2):
    # Convert mm and kN to float, handling decimal commas
    mm = [convert_to_float(value) for value in mm if is_float(value.replace(',', '.'))]
    kn = [convert_to_float(value) for value in kn if is_float(value.replace(',', '.'))]

def plot_mm_vs_kn(mm, kn, title):
    # Convert mm and kN to float for plotting
    [mm,kn] = filter_outliers(mm, kn)
    max_Force = np.max(kn)
    max_mm = mm[np.argmax(kn)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(mm, kn, marker='.', linestyle='None', color='#2C7FB8', label= title, markersize = 4)
    plt.title(r'Wedge Splitting Test', fontsize = 14 )
    plt.xlabel(r'Crack opening [mm]',fontsize = 12)
    plt.ylabel(r'Force [MPa]',fontsize = 12)
    plt.grid(True)
    plt.minorticks_on()
    plt.legend(fontsize=12)
    plt.annotate(f'Max Value: {max_Force:.2f}', xy=(max_mm, max_Force), xytext=(max_mm, max_Force - 8),
             arrowprops=dict(facecolor='#7FCDBB', shrink=0.2, width = 0.5, headwidth = 5, edgecolor ='#7FCDBB'), fontsize = 12)
    # Save the plot in PDF format
    filename = f"{title}{'.pdf'}"
    plt.savefig(filename, format='pdf')
    plt.show()
    plt.close()


#define plotting
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
directory = os.getcwd()
all_items = os.listdir(directory)
folders = [item for item in all_items if os.path.isdir(os.path.join(directory, item))]
# Store the folder names in a variable
headers = ["Ch 1 CMOD (mm)", "Ch 1 Displacement (mm)", "Ch 1 Force (kN)", "Time (s)"]
for i in range(len(folders)):
    title = folders[i]
    filep = os.path.join(directory, title)
    table_data= read_file_content(filep)    
#print(table_data)
    plot_mm_vs_kn(table_data['CMOD'], table_data['Force'],title)