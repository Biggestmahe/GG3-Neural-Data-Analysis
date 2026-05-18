import matplotlib.pyplot as plt
import numpy as np

def plot_spikes_and_rates(spikes, rates, no_of_plotted_trials=1):

    # plot spike raster and rate for first trial

    spike_times = []

    for trial in range(no_of_plotted_trials):
        trial_spikes = np.where(spikes[trial] > 0)[0] # np.where returns a list of indexes where condition spikes > 0 is true
        spike_times.append(trial_spikes)


    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    for trial in range(no_of_plotted_trials):
        plt.plot(rates[trial], label=f'Trial {trial}')
    plt.title('Firing Rate')
    plt.xlabel('Time (ms)')
    plt.ylabel('Rate (Hz)')
    plt.legend()



    plt.subplot(2, 1, 2)

    offsets = np.arange(1, no_of_plotted_trials + 1)

    plt.eventplot(spike_times, lineoffsets=offsets, linelengths=0.5)
    plt.title(f'Trial {trial} - Spike Raster')
    plt.xlabel('Time (ms)')
    plt.yticks(offsets, [f'Trial {i}' for i in range(no_of_plotted_trials)])
    plt.tight_layout()
    
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








