import parameters
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

prm = parameters.Parameters()

# set global parameters



# Load sleep state score
def load_state_data(state_data_path):

    # Load sleep state score from .csv
    data = pd.read_csv(state_data_path, delimiter=",") # read .csv file with sleep score

    return data

def plot_power_basic(df):
    fig, axs = plt.subplots(1, 1, figsize=(20, 15))
    sns.lineplot(data=df, x='Frequency', y='Power', hue='Br_State',
                 errorbar=("se"), linewidth=2)
    axs.set_yscale('log')
    fig.show()
    fig.savefig('basic_power_plot.jpg')

    sns.set_style("white")
    fig, axs = plt.subplots(1, 1, figsize=(20,15), sharex = True, sharey = True)
    sns.lineplot(data = df, x = 'Frequency', y = 'Power', hue = 'Br_State',
                 errorbar = ('se'), linewidth = 4)

    #remove the figure border
    sns.despine()

    #set limits and labels for the x and y axis
    axs.set_yscale('log')
    axs.set_xlim(1, 48)
    axs.set_ylim(10**-2, 10**3)
    axs.set_xlabel("Frequency (Hz)")
    axs.set_ylabel("log Power (\\u03bc$\\mathregular{V^{2}}$)")

    #save figure
    fig.show()
    fig.savefig('basic_plot.jpg')

    sns.set_style("white", rc = {'font.size': 20})
    fig, axs = plt.subplots(1, 1, figsize=(20,15), sharex = True, sharey = True)
    sns.lineplot(data = df, x = 'Frequency', y = 'Power', hue = 'Br_State',
    errorbar = ('se'), linewidth = 4, ax = axs)

    #remove outer border
    sns.despine()

    #axes customisation
    axs.set_yscale('log')
    axs.set_xlim(1, 48)
    axs.set_ylim(10**-2, 10**3)
    axs.set_xlabel("Frequency (Hz)", fontsize = 25)
    axs.set_ylabel("log Power (\\u03bc$\\mathregular{V^{2}}$)", fontsize = 25)

    #update the fontsize of all characters on x and y axis
    plt.rcParams.update({'font.size': 20})

    #changing x-ticks
    tick_values = list(range(1, 54, 6))
    label_list = ['1', '6', '12', '18', '24', '30', '36', '42', '48']
    axs.set_xticks(ticks = tick_values, labels = label_list)

    #include an overall plot title
    plt.suptitle('Condition 1 Overall Average', fontsize = 30, fontweight = 'bold')

    #customise the legend
    leg = plt.legend(loc = 'upper right', frameon = False)
    leg.set_title('Brain State', prop = {'size': 25})
    leg_lines = leg.get_lines()
    leg_texts = leg.get_texts()
    plt.setp(leg_lines[0], linewidth = 8)
    plt.setp(leg_lines[1], linewidth = 8)
    plt.setp(leg_texts, fontsize = 20)

    #increase the width of the x and y axis
    for axis in ['bottom', 'left']:
        axs.spines[axis].set_linewidth(3)

    #save figure
    fig.show()
    fig.savefig('detailed_reformatting_plot.jpg')

def main():
    print('-------------------------------------------------------------')
    print('-------------------------------------------------------------')

    #path to the recording .dat file
    file_path = '/Users/sarahtennant/Work_Alfredo/Analysis/Ezrie/power_csv/842_clean_power.csv'

    # load data
    data = load_state_data(file_path)

    plot_power_basic(data)

if __name__ == '__main__':
    main()

