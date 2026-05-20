import matplotlib.pyplot as plt
import numpy as np

def plot_spikes_and_rates(spikes, rates, no_of_plotted_trials=1, Step_Times=None, multiparams=False, spikes2=None, rates2=None, Step_Times2=None, histograms=False):

    # plot spike raster and rate for first trial

    spike_times = []

    for trial in range(no_of_plotted_trials):
        trial_spikes = np.where(spikes[trial] > 0)[0] # np.where returns a list of indexes where condition spikes > 0 is true
        spike_times.append(trial_spikes)

    if multiparams and spikes2 is not None and rates2 is not None:
        spike_times2 = []
        for trial in range(no_of_plotted_trials):
            trial_spikes2 = np.where(spikes2[trial] > 0)[0]
            spike_times2.append(trial_spikes2)


    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    for trial in range(no_of_plotted_trials):
        plt.plot(rates[trial], label=f'Trial {trial}')

    if multiparams and rates2 is not None:
        for trial in range(no_of_plotted_trials):
            plt.plot(rates2[trial], label=f'Trial {trial} - Param Set 2', linestyle='--')
            plt.title('Firing Rate Comparison')
    else:
        plt.title('Firing Rate')
    plt.xlabel('Time (ms)')
    plt.ylabel('Rate (Hz)')
    plt.legend()



    plt.subplot(2, 1, 2)

    if multiparams and spikes2 is not None:
        # 1. Total rows = 2 sources * trials per source
        total_rows = no_of_plotted_trials * 2
        offsets_all = np.arange(1, total_rows + 1)
        
        # 2. Split offsets: first half for Set 1, second half for Set 2
        offsets1 = offsets_all[:no_of_plotted_trials]
        offsets2 = offsets_all[no_of_plotted_trials:]
        
        # 3. Plot Parameter Set 1 (using a clean default blue color 'C0')
        plt.eventplot(spike_times, lineoffsets=offsets1, linelengths=0.5, colors='C0')
        if Step_Times is not None:
            for trial in range(no_of_plotted_trials):
                plt.scatter(Step_Times[trial], offsets1[trial], color='blue', marker='|', s=300, linewidth=4, zorder=10)
                
        # 4. Plot Parameter Set 2 (using a clean default orange color 'C1')
        plt.eventplot(spike_times2, lineoffsets=offsets2, linelengths=0.5, colors='C1')
        if Step_Times2 is not None:
            for trial in range(no_of_plotted_trials):
                plt.scatter(Step_Times2[trial], offsets2[trial], color='red', marker='|', s=300, linewidth=4, zorder=10)
        
        # 5. Create distinct labels for the Y-ticks to show which is which
        y_labels = [f'P1 Tr{i}' for i in range(no_of_plotted_trials)] + [f'P2 Tr{i}' for i in range(no_of_plotted_trials)]
        plt.yticks(offsets_all, y_labels)
        plt.ylim(0.5, total_rows + 0.5)
        plt.title('Spike Rasters: Parameter Set 1 vs 2')

    else:
        # --- Fallback to your original single-parameter setup ---
        offsets = np.arange(1, no_of_plotted_trials + 1)
        plt.eventplot(spike_times, lineoffsets=offsets, linelengths=0.5)
        
        if Step_Times is not None:
            for trial in range(no_of_plotted_trials):
                plt.scatter(Step_Times[trial], offsets[trial], color='red', marker='|', s=300, linewidth=4, zorder=10)
                
        plt.yticks(offsets, [f'Trial {i}' for i in range(no_of_plotted_trials)])
        plt.title('Spike Raster')

    plt.xlabel('Time (ms)')
    plt.tight_layout()
    plt.show()


def histogram_step_times(Step_Times, binsize=10):

    # plot histogram of step times across trials

    plt.figure(figsize=(10, 4))
    plt.hist(Step_Times, bins=np.arange(0, max(Step_Times) + binsize, binsize), density=True)
    plt.title('Histogram of Step Times')
    plt.xlabel('Time (ms)')
    plt.ylabel('Density')
    plt.show()

def histogram_Rh_times(rates, binsize=10):
    # plot histogram of times when rates reach Rh across trials

    Rh_times = []
    for trial in range(rates.shape[0]):
        Rh_time = np.where(rates[trial] >= np.max(rates[trial]))[0][0]  # find first time index where rate reaches max (Rh)
        Rh_times.append(Rh_time)

    plt.figure(figsize=(10, 4))
    plt.hist(Rh_times, bins=np.arange(0, max(Rh_times) + binsize, binsize), density=True)
    plt.title('Histogram of Times When Rates Reach Rh')
    plt.xlabel('Time (ms)')
    plt.ylabel('Density')
    plt.show()


def plot_PSTH(spikes, Ntrials=10, binsize=10):

    #histogram spikes from multiple trials to understand average firing rates

    all_spike_times = []
    for trial in range(Ntrials):
        trial_spikes = np.where(spikes[trial] > 0)[0]
        all_spike_times.extend(trial_spikes)
    
    plt.figure(figsize=(10, 4))
    plt.hist(all_spike_times, bins=np.arange(0, max(all_spike_times) + binsize, binsize), density=True)
    plt.title('Peri-Stimulus Time Histogram (PSTH)')
    plt.xlabel('Time (ms)')
    plt.ylabel('Firing Rate (Hz)')
    plt.show()


def fano_factor(spikes, T = 1000, binsize=10):

    #calculate Fano factor to understand variability in spike counts across trials

    #find loactions of spikes
    #iterate through bins and trials
    # cout number of spikes in each bin for each trial
    # calculate mean and variance of spike counts across trials for each bin
    #Fano factor = variance / mean

    fano_factors = []

    for bin in range(int(T / binsize)):

        spike_counts = []
        for trial in range(spikes.shape[0]):
            trial_spikes = np.where(spikes[trial] > 0)[0]
            count = np.sum((trial_spikes >= bin * binsize) & (trial_spikes < (bin + 1) * binsize))
            spike_counts.append(count)

        mean_count = np.mean(spike_counts)
        variance_count = np.var(spike_counts)
        fano_factor = round((variance_count / mean_count if mean_count > 0 else 0), 3)
        fano_factors.append(fano_factor)
    
    plt.figure(figsize=(10, 4))
    plt.plot(fano_factors, marker='o')
    plt.title('Fano Factor Over Time')
    plt.xlabel('Time Bin')
    plt.ylabel('Fano Factor')
    plt.show()











