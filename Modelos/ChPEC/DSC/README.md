# Frequency Adaptive Delayed Signal Cancellation Applied Directly to the Rotating Reference Frames of Dual-Sequence Current Controllers of Power Converters

This repository contains the simulation and data files used in the full paper manuscript "Dual-Sequence Current Controller with Delayed Signal Cancellation in the Rotating Reference Frame" submitted in October 2021 to the "Twenty-second IEEE Workshop on Control and Modeling for Power Electronics (COMPEL 2021)".

## Scripts, models, and figures: 
The files are organized as follows:

 - The "\*_Script.m" runs the Simulink Model "\*.slx". There might be cases to be chosen (hardcoded) in each script.
 - The Simulink Model "\*.slx" produces a comma separated text file "\*_Raw.txt".
 - The comma separated text file "\*_Raw.txt" contains the data necessary for generating the figures.
 
MATLAB Version: 9.4.0.949201 (R2018a) Update 6

All Simulink models use blocks from the library "DSCdq_Library.slx" of this repository.

All charts in the manuscript figures were made in Python (matplotlib) with data from the \*_Raw.txt files. The python code is not present in this repository.

FFTs were calculated with Python using the Empirical Transfer Function Estimation (ETFE) [Lennart Ljung's System Identification: Theory for the User] from the data in \*_Raw.txt. The Python code is not present in this repository.

### Figures: Short Pulse and FFT of DSC and Notch
ShortPulse_Script.m, ShortPulse.slx, ShortPulse_Raw.txt

### Figure: FFT of Two DSCs with Contiguous Delays
FreqAdaptiveFFT_Script.m, FreqAdaptiveFFT.slx, FreqAdaptiveFFT_Raw.txt

### Figure: Unbalanced voltages with varying frequency, DSCdq floor/ceiling/weighted
FreqAdaptive_Script.m, FreqAdaptive.slx, FreqAdaptive_Raw.txt

### Figure: DSCs vs Notch with Unbalanced Grid
Adaptive_Script.m (case=1), Adaptive.slx, Application_Unb_Notch.txt, Application_Unb_DSCab.txt, Application_Unb_DSCdq.txt

### Figure: DSCs vs Notch with Balanced Grid
Adaptive_Script.m (case=2), Adaptive.slx, Application_Bal_Notch.txt, Application_Bal_DSCab.txt, Application_Bal_DSCdq.txt
