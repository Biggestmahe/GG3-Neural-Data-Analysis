import matplotlib.pyplot as plt
import numpy as np

def plot_spikes_and_rates(spikes, rates, trial=0):

    # plot spike raster and rate for first trial

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(rates[trial], label='Firing Rate')
    plt.title(f'Trial {trial} - Firing Rate')
    plt.xlabel('Time (ms)')
    plt.ylabel('Rate (Hz)')
    plt.legend()

    plt.subplot(2, 1, 2)
    
    spike_times = np.where(spikes[trial] > 0)[0] # np.where returns a list of indexes where condition spikes > 0 is true
        
    plt.eventplot(spike_times, lineoffsets=1, linelengths=0.5)
    plt.title(f'Trial {trial} - Spike Raster')
    plt.xlabel('Time (ms)')
    plt.yticks([]) # remove y-axis ticks for raster plot
    plt.tight_layout()
    
    plt.show()



