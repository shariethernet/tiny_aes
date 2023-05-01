import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

MAX_FREQ_CSV = "/home/local/nu/shg/tiny_aes/max_freq.csv"
POWER_CSV = "/home/local/nu/shg/tiny_aes/out_maxfreq_aes128_200.csv"
CONSOLIDATED_CSV = "consolidated.csv"
CYCLES = 290
# Load the CSV data into a pandas DataFrame
markers = ['o', 's', 'd', '^', '*', 'p', 'h', '>', 'v', '<','x','+','X','P','1','2','3','4']
def plot_max_freq(path):
    data = pd.read_csv(path)
    # Get the unique nfet and pfet bias pairs in the data
    bias_pairs = data[['nfet_bias', 'pfet_bias']].drop_duplicates()
    #print(bias_pairs)
    fig, ax = plt.subplots(figsize=(25, 12))
    # Loop through each bias pair and plot the corresponding data
    marker_idx = 0

    for index, bias_pair in bias_pairs.iterrows():
        nfet_bias = bias_pair['nfet_bias']
        pfet_bias = bias_pair['pfet_bias']

        # Filter the data to only include rows with the desired nfet bias and pfet bias values
        filtered_data = data[(data['nfet_bias'] == nfet_bias) & (data['pfet_bias'] == pfet_bias)]
        filtered_data = filtered_data.sort_values(by='supply_voltage')
        # Create a line plot of supply voltage vs frequency for the filtered data
        ax.plot(filtered_data['supply_voltage'].values[:, np.newaxis], filtered_data['Frequency (Mhz)'].values[:, np.newaxis],'-'+markers[marker_idx%len(markers)],label=f"Bias-NFET: {nfet_bias}, PFET: {pfet_bias}")
        marker_idx += 1
        #ax.scatter(filtered_data['supply_voltage'].values[:, np.newaxis], filtered_data['Frequency (Mhz)'].values[:, np.newaxis],label=f"NFET Bias: {nfet_bias}, PFET Bias: {pfet_bias}")
    # Add labels to the plot
    ax.grid(True)
    ax.set_xlabel('Supply Voltage (V)')
    ax.set_ylabel('Frequency (MHz)')
    ax.set_title('Frequency vs Supply Voltage for Different NFET and PFET Biases')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.4))
    plt.subplots_adjust(wspace=0.4)
    plt.savefig("Max_freq_plot.png")
    # Show the plot
    plt.show()

def plot_energy(freq_csv_path,power_csv_path,cycles):
    data = pd.read_csv(power_csv_path)
    freq_data = pd.read_csv(freq_csv_path)
    # Get the unique nfet and pfet bias pairs in the data
    bias_pairs = data[['nfet_bias', 'pfet_bias']].drop_duplicates()
    #print(bias_pairs)
    fig, ax = plt.subplots(3,1,figsize=(40, 40))
    # Loop through each bias pair and plot the corresponding data

    new_data = pd.DataFrame(columns=['supply_voltage', 'nfet_bias', 'pfet_bias', 
                                     'Clock Period (ns)', 'Frequency (MHz)', 'total dynamic power', 
                                     'leakage power','total power', 'total dynamic energy',
                                     'leakage energy','total energy'])
    
    marker_idx = 0
    for index, bias_pair in bias_pairs.iterrows():
        nfet_bias = bias_pair['nfet_bias']
        pfet_bias = bias_pair['pfet_bias']
        print(f"--------nfet:{nfet_bias} pfet:{pfet_bias}-----------")
        # Filter the data to only include rows with the desired nfet bias and pfet bias values
        filtered_data = data[(data['nfet_bias'] == nfet_bias) & (data['pfet_bias'] == pfet_bias)]
        print("----filtered data----")
        
        filtered_data = filtered_data.sort_values(by='supply_voltage')
        print(filtered_data)
        print("filt_data",len(filtered_data))
        print("filtered_data['supply_voltage']",len(filtered_data['supply_voltage']))

        # Get the clock period for the current bias pair from the frequency data
        freq_row = freq_data[(freq_data['nfet_bias'] == nfet_bias) & (freq_data['pfet_bias'] == pfet_bias)]
        print("----freq row data----")
        
        freq_row = freq_row.sort_values(by='supply_voltage')
        print(freq_row)
        print("freq_row",len(freq_row))

        clock_period = freq_row['Clock Period (ns)']
        freq_mhz = freq_row['Frequency (Mhz)']
        dynamic_power = filtered_data['Net Switching Power'] + filtered_data['Cell Internal Power']
        leakage_power = filtered_data['Cell Leakage Power']
        total_power = filtered_data['Total Power']
        total_leakage_energy = leakage_power.values * cycles * 10e-9 * clock_period.values
        total_dynamic_energy = dynamic_power.values * cycles * 10e-9 * clock_period.values
        print("tot_dynamic_energy:",len(total_dynamic_energy))
        print("tot_leakage_energy:",len(total_leakage_energy))
        print("dynamic_power:",len(dynamic_power))
        print("leakage_power:",len(leakage_power))
        print("clock_pd:",len(clock_period))
        total_energy = total_power.values * cycles * 10e-9 * clock_period.values
        #print(dynamic_power)
        new_row = pd.DataFrame({'supply_voltage': filtered_data['supply_voltage'].values,
                                'nfet_bias': nfet_bias,
                                'pfet_bias': pfet_bias,
                                'Clock Period (ns)': clock_period,
                                'Frequency (MHz)': freq_mhz,
                                'total dynamic power': dynamic_power.values,
                                'leakage power':leakage_power.values,
                                'total power':total_power.values,
                                'total dynamic energy': total_dynamic_energy,
                                'leakage energy': total_leakage_energy,
                                'total energy': total_energy

                                })
        new_data = pd.concat([new_data,new_row],ignore_index=True)
        # Create a line plot of supply voltage vs frequency for the filtered data
        ax[0].plot(filtered_data['supply_voltage'].values[:, np.newaxis], total_dynamic_energy,'-'+markers[marker_idx%len(markers)],label=f"Bias-NFET: {nfet_bias}, PFET: {pfet_bias}")
        ax[1].plot(filtered_data['supply_voltage'].values[:, np.newaxis], total_leakage_energy,'-'+markers[marker_idx%len(markers)],label=f"Bias-NFET: {nfet_bias}, PFET: {pfet_bias}")
        ax[2].plot(filtered_data['supply_voltage'].values[:, np.newaxis], total_energy,'-'+markers[marker_idx%len(markers)],label=f"Bias-NFET: {nfet_bias}, PFET: {pfet_bias}")
        marker_idx +=1
        print(f"----------------------------------")
        #ax.scatter(filtered_data['supply_voltage'].values[:, np.newaxis], filtered_data['Frequency (Mhz)'].values[:, np.newaxis],label=f"NFET Bias: {nfet_bias}, PFET Bias: {pfet_bias}")
    # Save the new DataFrame to a CSV file
    new_data.to_csv(CONSOLIDATED_CSV, index=False)
    # Add labels to the plot

    ax[0].grid(True)
    ax[1].grid(True)
    ax[2].grid(True)
    ax[0].set_xlabel('Supply Voltage (V)')
    ax[0].set_ylabel('Dynamic Energy (J)')
    ax[0].set_title(' Dynamic Energy vs Supply Voltage for Different NFET and PFET Biases')
    ax[0].legend(loc='center left', bbox_to_anchor=(1, 0.4))

    ax[1].set_xlabel('Supply Voltage (V)')
    ax[1].set_ylabel('Leakage Energy (J)')
    ax[1].set_title(' Leakage Energy vs Supply Voltage for Different NFET and PFET Biases')
    #ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.4))

    ax[2].set_xlabel('Supply Voltage (V)')
    ax[2].set_ylabel('Total Energy (J)')
    ax[2].set_title(' Total Energy vs Supply Voltage for Different NFET and PFET Biases')
    #ax[2].legend(loc='center left', bbox_to_anchor=(1, 0.4))
    plt.subplots_adjust(wspace=0.4)
    plt.savefig("energy_plot.png")
    # Show the plot
    plt.show()
if __name__ == "__main__":
    plot_max_freq(MAX_FREQ_CSV)
    #plot_energy(POWER_CSV,"Dynamic",CYCLES)
    #plot_energy(POWER_CSV,"Leakage",CYCLES)
    plot_energy(MAX_FREQ_CSV,POWER_CSV,CYCLES)