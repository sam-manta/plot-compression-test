import os, re
import matplotlib.pyplot as plt
import numpy as np

def get_titles_from_files(directory):
    # Initialize a list to hold titles
      # List all files in the given directory
    file_path = []
    for filename in os.listdir(directory):
        # Check if the file is a .txt file
        if filename.endswith(".txt"):
           path_sing = os.path.join(directory, filename)
           file_path.append(path_sing)
    return file_path

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
    
    # Calculate means and standard deviations
    mm_mean, mm_std = np.mean(mm), np.std(mm)
    kn_mean, kn_std = np.mean(kn), np.std(kn)

    # Filter out values that are outside the specified range of standard deviations
    filtered_mm = []
    filtered_kn = []
    for m, k in zip(mm, kn):
        if (mm_mean - num_std_dev * mm_std <= m <= mm_mean + num_std_dev * mm_std) and \
           (kn_mean - num_std_dev * kn_std <= k <= kn_mean + num_std_dev * kn_std):
            filtered_mm.append(m)
            filtered_kn.append(k)
    
    return filtered_mm, filtered_kn

def read_file_content(filep):
    # Initialize a list to hold titles
    table_data = {'mm': [], 'kN': [], 's': []}
    with open(filep) as file:
        content = file.read()
                
        # Use regex to find all occurrences of text in quotes starting with "Crac"
        specimen_match = re.search(r'"Specimen ID";"([^"]+)"', content)
        if specimen_match:
                    title = specimen_match.group(1)

        table_started = False
        for line in content.splitlines():
            if table_started:
                data = line.split(';')
                if len(data) >= 3:
                    table_data['mm'].append(data[0].strip())
                    table_data['kN'].append(data[1].strip())
                    table_data['s'].append(data[2].strip())
            if re.match(r'"mm";\s*"?kN"?;\s*"?s"?', line):
                table_started = True

    return title, table_data

def plot_mm_vs_kn(mm, kn, title):
    # Convert mm and kN to float for plotting
    [mm,kn] = filter_outliers(mm, kn)
    radius = 0.05 #m
    Area = (radius**2)* np.pi /2
    kn_array = np.array(kn)
    stress = kn_array / Area / 1000 /2
    max_stress = np.max(stress)
    max_mm = mm[np.argmax(stress)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(mm, stress, marker='.', linestyle='None', color='#2C7FB8', label= title, markersize = 4)
    plt.title(r'Compression test', fontsize = 14 )
    plt.xlabel(r'Displacement [mm]',fontsize = 12)
    plt.ylabel(r'Stress [MPa]',fontsize = 12)
    plt.grid(True)
    plt.minorticks_on()
    plt.legend(fontsize=12)
    plt.annotate(f'Max Value: {max_stress:.2f}', xy=(max_mm, max_stress), xytext=(max_mm, max_stress - 8),
             arrowprops=dict(facecolor='#7FCDBB', shrink=0.2, width = 0.5, headwidth = 5, edgecolor ='#7FCDBB'), fontsize = 12)
    # Save the plot in PDF format
    filename = f"{title}{'.pdf'}"
    plt.savefig(filename, format='pdf')
    # plt.show()
    plt.close()

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
directory = 'data'
file_path = get_titles_from_files(directory)
for i in range(len(file_path)):
    filep = file_path[i]
    title, table_data= read_file_content(filep)
#print(table_data)
    plot_mm_vs_kn(table_data['mm'], table_data['kN'],title)

## Att göra : iterate through the files in the folder and save image
# Calculate in MPa based on geometry
# Make the graphs nicer
# One single graph per type of specimen.