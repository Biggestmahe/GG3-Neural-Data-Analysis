import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


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


def fano_factor(spikes, T = 1000, binsize=10, multifano=False, spikes2=None, spikes3=None):

    #calculate Fano factor to understand variability in spike counts across trials

    #find loactions of spikes
    #iterate through bins and trials
    # cout number of spikes in each bin for each trial
    # calculate mean and variance of spike counts across trials for each bin
    #Fano factor = variance / mean

    fano_factors = []
    fano_factors2 = []
    fano_factors3 = []

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
    
    if multifano:
        for bin in range(int(T / binsize)):
            spike_counts2 = []
            for trial in range(spikes2.shape[0]):
                trial_spikes2 = np.where(spikes2[trial] > 0)[0]
                count2 = np.sum((trial_spikes2 >= bin * binsize) & (trial_spikes2 < (bin + 1) * binsize))
                spike_counts2.append(count2)

            mean_count2 = np.mean(spike_counts2)
            variance_count2 = np.var(spike_counts2)
            fano_factor2 = round((variance_count2 / mean_count2 if mean_count2 > 0 else 0), 3)
            fano_factors2.append(fano_factor2)

        for bin in range(int(T / binsize)):
            spike_counts3 = []
            for trial in range(spikes3.shape[0]):
                trial_spikes3 = np.where(spikes3[trial] > 0)[0]
                count3 = np.sum((trial_spikes3 >= bin * binsize) & (trial_spikes3 < (bin + 1) * binsize))
                spike_counts3.append(count3)

            mean_count3 = np.mean(spike_counts3)
            variance_count3 = np.var(spike_counts3)
            fano_factor3 = round((variance_count3 / mean_count3 if mean_count3 > 0 else 0), 3)
            fano_factors3.append(fano_factor3)


    #plot with legend if multifano is true, otherwise just plot one line

    plt.figure(figsize=(10, 4))
    plt.plot(fano_factors, marker='o', label='beta = 1, sigma = 0.04')
    if multifano:
        plt.plot(fano_factors2, marker='s', label='beta = 1, sigma = 0.5')
        plt.plot(fano_factors3, marker='^', label='beta = 1, sigma = 4')
        plt.legend()
    plt.title('Fano Factor Over Time')
    plt.xlabel('Time Bin')
    plt.ylabel('Fano Factor')



    plt.show()

### Grad based classifier not used ####

def grad_based_classifier(spikes, T=1000, binsize=50, Ntrials=400, smoothing=0.5):

    all_spike_times = []
    for trial in range(Ntrials):
        trial_spikes = np.where(spikes[trial] > 0)[0]
        all_spike_times.extend(trial_spikes)

    plt.figure(figsize=(10, 4))

    ax = sns.histplot(all_spike_times, bins=np.arange(0, max(all_spike_times) + binsize, binsize), 
                      stat="density", kde=True, kde_kws={'bw_adjust': smoothing})

    if len(ax.lines) > 0:
        kde_line = ax.lines[0]
        x_line = kde_line.get_xdata()  # Time points
        y_line = kde_line.get_ydata()  # Firing rate density

        gradients = np.gradient(y_line, x_line)

        start_time = T / 4
        end_time = (3 * T) / 4

        in_range_indices = np.where((x_line >= start_time) & (x_line <= end_time))[0]

        if len(in_range_indices) > 0:
            gradients_in_range = gradients[in_range_indices]
            x_in_range = x_line[in_range_indices]

            max_grad = np.max(gradients_in_range)
            max_grad_idx = np.argmax(gradients_in_range)
            time_of_max_grad = x_in_range[max_grad_idx]
            
            y_of_max_grad = y_line[in_range_indices[max_grad_idx]]

            plt.scatter(time_of_max_grad, y_of_max_grad, color='red', s=100, zorder=5, 
                        label=f'Max Slope: {max_grad:.6f} at {time_of_max_grad:.1f}ms')
            plt.legend()
            
            print(f"Max Gradient in range [{start_time}ms, {end_time}ms]: {max_grad:.6f} at {time_of_max_grad:.1f} ms")
        else:
            max_grad = None
            print("Specified time range was outside of the plotted data bounds.")
    else:
        max_grad = None
        print("Warning: Could not extract KDE line. Make sure data is non-empty.")

    plt.title('Spike Time Distribution with KDE & Max Gradient Spotting')
    plt.xlabel('Time (ms)')
    plt.ylabel('Density')
    plt.show()


    if max_grad > 0.000005:
        print("Step Model")
    else:
        print("Ramp Model")

    # Return the value so you can pass it to your decision matrix logic
    return max_grad


def analyze_fano_dft(spikes, T=1000, binsize=10, label="Model Data"):


    #calculates dft of fano factor graphs looking for low freq wave

    fano_factors = []
    num_bins = int(T / binsize)
    
    for bin_idx in range(num_bins):
        spike_counts = []
        for trial in range(spikes.shape[0]):
            trial_spikes = np.where(spikes[trial] > 0)[0]
            count = np.sum((trial_spikes >= bin_idx * binsize) & (trial_spikes < (bin_idx + 1) * binsize))
            spike_counts.append(count)

        mean_count = np.mean(spike_counts)
        variance_count = np.var(spike_counts)
        ff = variance_count / mean_count if mean_count > 0 else 0
        fano_factors.append(ff)
        
    fano_factors = np.array(fano_factors)

    ### Conmpute DFT

    dt_seconds = binsize / 1000.0
    
    fft_coeffs = np.fft.fft(fano_factors)

    power_spectrum = np.abs(fft_coeffs) ** 2    # Calculate the Power Spectrum
    

    frequencies = np.fft.fftfreq(num_bins, d=dt_seconds)    # Get the corresponding frequencies in Hz
    

    positive_indices = np.where(frequencies >= 0)[0]    # use only positive frequencies
    frequencies = frequencies[positive_indices]
    power_spectrum = power_spectrum[positive_indices]

    plt.figure(figsize=(14, 5)) # Time-domain Fano Factor curve

    plt.subplot(1, 2, 1)
    time_axis = np.arange(num_bins) * binsize
    plt.plot(time_axis, fano_factors, marker='o', color='C0', linewidth=2)
    plt.title(f'Fano Factor')
    plt.xlabel('Time (ms)')
    plt.ylabel('Fano Factor')
    plt.grid(True, alpha=0.3)

    
    plt.subplot(1, 2, 2) # Frequency-domain Power Spectrum
   
    non_zero_idx = frequencies > 0    # Filter out the 0 Hz
    
    plt.stem(frequencies[non_zero_idx], power_spectrum[non_zero_idx], 
             linefmt='C1-', markerfmt='C1o', basefmt='k-')
    plt.title('DFT Power Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')

    plt.xlim(0, 15)     # Zoom in on the low frequencies
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    
    freq_1hz_idx = np.argmin(np.abs(frequencies - 1.0))
    power_at_1hz = power_spectrum[freq_1hz_idx]
        
    if power_at_1hz > 5.5:
        print(f"Step Model")
    else:

        print(f"Drift Diffusion Model")


def compare_HMM_to_real(rates_continuous, rates_hmm, dt, no_of_plotted_trials=3):
    """Plots and compares firing rate trajectories between the continuous ramp

    model and the discrete HMM approximation.

    Parameters:
    -----------
    rates_continuous : np.ndarray
        Shape (Ntrials, Nsteps) containing rates from the continuous model.
    rates_hmm : np.ndarray
        Shape (Ntrials, Nsteps) containing rates from the discrete HMM simulation.
    dt : float
        Time step size in seconds (e.g., 0.001 for 1ms steps).
    no_of_plotted_trials : int
        Number of individual trial trajectories to overlay.
    """
    n_trials, n_steps = rates_continuous.shape
    time_axis = np.arange(n_steps) * (dt * 1000)  # Convert to ms for plotting

    plt.figure(figsize=(14, 10))

    # --- SUBPLOT 1: Individual Continuous Model Trials ---
    plt.subplot(2, 2, 1)
    for i in range(min(no_of_plotted_trials, n_trials)):
        plt.plot(time_axis, rates_continuous[i], alpha=0.8, label=f"Trial {i}")
    plt.title("Continuous Ramp Model: Individual Trials")
    plt.xlabel("Time (ms)")
    plt.ylabel("Firing Rate (Hz)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    # --- SUBPLOT 2: Individual Discrete HMM Trials ---
    plt.subplot(2, 2, 2)
    for i in range(min(no_of_plotted_trials, n_trials)):
        plt.plot(
            time_axis,
            rates_hmm[i],
            alpha=0.8,
            linestyle="-",
            label=f"HMM Trial {i}",
        )
    plt.title(f"Discrete HMM (K={rates_hmm.shape[0]}) Trials")
    plt.xlabel("Time (ms)")
    plt.ylabel("Firing Rate (Hz)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    # --- SUBPLOT 3: Single Trial Direct Overlay Comparison ---
    plt.subplot(2, 2, 3)
    plt.plot(
        time_axis,
        rates_continuous[0],
        color="C0",
        linewidth=2,
        label="Continuous (Trial 0)",
    )
    plt.plot(
        time_axis,
        rates_hmm[0],
        color="C1",
        linewidth=2,
        linestyle="--",
        label="HMM (Trial 0)",
    )
    plt.title("Direct Path Overlay (Trial 0)")
    plt.xlabel("Time (ms)")
    plt.ylabel("Firing Rate (Hz)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    # --- SUBPLOT 4: Grand Trial Average (The Ultimate Sanity Check) ---
    mean_continuous = np.mean(rates_continuous, axis=0)
    mean_hmm = np.mean(rates_hmm, axis=0)

    plt.subplot(2, 2, 4)
    plt.plot(
        time_axis,
        mean_continuous,
        color="navy",
        linewidth=2.5,
        label="Continuous Grand Mean",
    )
    plt.plot(
        time_axis,
        mean_hmm,
        color="darkorange",
        linewidth=2.5,
        linestyle="--",
        label="HMM Grand Mean",
    )
    plt.title(f"Grand Average Across {n_trials} Trials")
    plt.xlabel("Time (ms)")
    plt.ylabel("Firing Rate (Hz)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_step_model_comparison(
    continuous_rates, HMM_rates, continuous_jumps, HMM_jumps, dt=0.001, num_plotted_trials = 5
):

    # calculate time array in milliseconds
    T = continuous_rates.shape[1]
    time_ms = np.arange(T) * (dt * 1000)
    num_trials = continuous_rates.shape[0]

    # calculate grand means across all simulated trials
    mean_continuous_rate = np.mean(continuous_rates, axis=0)
    mean_HMM_rate = np.mean(HMM_rates, axis=0)

    # convert raw step jump indices to milliseconds
    continuous_jumps_ms = continuous_jumps * (dt * 1000)
    HMM_jumps_ms = HMM_jumps * (dt * 1000)

    # initialize a 2x2 square grid layout
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- row 0, col 0: continuous individual trials ---
    for trial in range(num_plotted_trials):
        axes[0, 0].plot(time_ms, continuous_rates[trial, :], color="navy", alpha=1, linewidth=1)
    axes[0, 0].set_title(f"Continuous Trials ({num_trials})", fontsize=12)
    axes[0, 0].set_xlabel("Time (ms)", fontsize=11)
    axes[0, 0].set_ylabel("Firing Rate (Hz)", fontsize=11)
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].set_ylim(-5, 55)

    # --- row 0, col 1: hmm individual trials ---
    for trial in range(num_plotted_trials):
        axes[0, 1].plot(time_ms, HMM_rates[trial, :], color="darkorange", alpha=1, linewidth=1)
    axes[0, 1].set_title(f"HMM Trials ({num_trials})", fontsize=12)
    axes[0, 1].set_xlabel("Time (ms)", fontsize=11)
    axes[0, 1].set_ylabel("Firing Rate (Hz)", fontsize=11)
    axes[0, 1].grid(alpha=0.3)
    axes[0, 1].set_ylim(-5, 55)

    # --- row 1, col 0: grand mean comparison ---
    axes[1, 0].plot(
        time_ms,
        mean_continuous_rate,
        label="Continuous Mean",
        color="navy",
        linewidth=2.5,
    )
    axes[1, 0].plot(
        time_ms,
        mean_HMM_rate,
        label="HMM Mean",
        color="darkorange",
        linestyle="--",
        linewidth=2.5,
    )
    axes[1, 0].set_title("Grand Mean Comparison", fontsize=12)
    axes[1, 0].set_xlabel("Time (ms)", fontsize=11)
    axes[1, 0].set_ylabel("Firing Rate (Hz)", fontsize=11)
    axes[1, 0].legend(loc="lower right")
    axes[1, 0].grid(alpha=0.3)
    axes[1, 0].set_ylim(-5, 55)

    # --- row 1, col 1: jump time histograms ---
    min_time = min(np.min(continuous_jumps_ms), np.min(HMM_jumps_ms))
    max_time = max(np.max(continuous_jumps_ms), np.max(HMM_jumps_ms))
    bins = np.linspace(min_time, max_time, 20)

    axes[1, 1].hist(
        continuous_jumps_ms,
        bins=bins,
        alpha=0.5,
        label="Continuous",
        color="navy",
        edgecolor="black",
    )
    axes[1, 1].hist(
        HMM_jumps_ms,
        bins=bins,
        alpha=0.5,
        label="HMM",
        color="darkorange",
        edgecolor="black",
    )
    axes[1, 1].set_title("Distribution of Jump Times", fontsize=12)
    axes[1, 1].set_xlabel("Jump Time (ms)", fontsize=11)
    axes[1, 1].set_ylabel("Trial Count", fontsize=11)
    axes[1, 1].legend(loc="upper right")
    axes[1, 1].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()




def plot_multistate_model_comparison(
    continuous_rates, HMM_multi_rates, continuous_jumps, HMM_multi_jumps, dt=0.001, num_plotted_trials = 5
):

    # calculate time array in milliseconds
    T = continuous_rates.shape[1]
    time_ms = np.arange(T) * (dt * 1000)
    num_trials = continuous_rates.shape[0]

    # calculate grand means across all simulated trials
    mean_continuous_rate = np.mean(continuous_rates, axis=0)
    mean_HMM_multi_rate = np.mean(HMM_multi_rates, axis=0)

    # convert raw step jump indices to milliseconds
    continuous_jumps_ms = continuous_jumps * (dt * 1000)
    HMM_multi_jumps_ms = HMM_multi_jumps * (dt * 1000)

    # initialize a 2x2 square grid layout
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- row 0, col 0: continuous individual trials ---
    for trial in range(num_plotted_trials):
        axes[0, 0].plot(time_ms, continuous_rates[trial, :], color="navy", alpha=1, linewidth=1)
    axes[0, 0].set_title(f"Continuous Model Trials ({num_trials})", fontsize=12)
    axes[0, 0].set_xlabel("Time (ms)", fontsize=11)
    axes[0, 0].set_ylabel("Firing Rate (Hz)", fontsize=11)
    axes[0, 0].grid(alpha=0.3)
    axes[0, 0].set_ylim(-5, 55)

    # --- row 0, col 1: multi-state hmm individual trials ---
    for trial in range(num_plotted_trials):
        axes[0, 1].plot(time_ms, HMM_multi_rates[trial, :], color="forestgreen", alpha=1, linewidth=1)
    axes[0, 1].set_title(f"Multi-state HMM Trials ({num_trials})", fontsize=12)
    axes[0, 1].set_xlabel("Time (ms)", fontsize=11)
    axes[0, 1].set_ylabel("Firing Rate (Hz)", fontsize=11)
    axes[0, 1].grid(alpha=0.3)
    axes[0, 1].set_ylim(-5, 55)

    # --- row 1, col 0: grand mean comparison ---
    axes[1, 0].plot(
        time_ms,
        mean_continuous_rate,
        label="Continuous Mean",
        color="navy",
        linewidth=2.5,
    )
    axes[1, 0].plot(
        time_ms,
        mean_HMM_multi_rate,
        label="Multi-state HMM Mean",
        color="forestgreen",
        linestyle="--",
        linewidth=2.5,
    )
    axes[1, 0].set_title("Grand Mean Comparison", fontsize=12)
    axes[1, 0].set_xlabel("Time (ms)", fontsize=11)
    axes[1, 0].set_ylabel("Firing Rate (Hz)", fontsize=11)
    axes[1, 0].legend(loc="lower right")
    axes[1, 0].grid(alpha=0.3)
    axes[1, 0].set_ylim(-5, 55)

    # --- row 1, col 1: jump time histograms ---
    min_time = min(np.min(continuous_jumps_ms), np.min(HMM_multi_jumps_ms))
    max_time = max(np.max(continuous_jumps_ms), np.max(HMM_multi_jumps_ms))
    bins = np.linspace(min_time, max_time, 20)

    axes[1, 1].hist(
        continuous_jumps_ms,
        bins=bins,
        alpha=0.5,
        label="Continuous",
        color="navy",
        edgecolor="black",
    )
    axes[1, 1].hist(
        HMM_multi_jumps_ms,
        bins=bins,
        alpha=0.5,
        label="Multi-state HMM",
        color="forestgreen",
        edgecolor="black",
    )
    axes[1, 1].set_title("Distribution of Jump Times", fontsize=12)
    axes[1, 1].set_xlabel("Jump Time (ms)", fontsize=11)
    axes[1, 1].set_ylabel("Trial Count", fontsize=11)
    axes[1, 1].legend(loc="upper right")
    axes[1, 1].grid(alpha=0.3)

    plt.tight_layout()
    plt.show()




###