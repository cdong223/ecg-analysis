# ECG Analysis Assignment

## Description
The purpose of this program is to read in and analyze a csv file containing a strip of ECG data. The program determines certain metrics for each strip:

- Time duration <br/>
- Minimum and maximum lead voltages <br/>
- Number of detected beats
- Average heart rate over length of strip <br/>
- List of the different time points at which a beat occurred <br/>

These metrics are outputted as a JSON file whose name corresponds to that of the original file.  

## Instructions for Use
Fork the project repository (`ecg-analysis-cdong223`) and create a local copy using the `git clone` command. To run the program, navigate within the repository and locate the project file: `ecg_analysis.py`. The csv files are also located within this repository, but are contained within a folder called test_data, and their names are formatted as follows: `test_data#.csv`, where # is a unique identification number.

Once the file is run, the user is prompted to enter a filename: `Enter filename: `. Enter the name of the file to be analyzed, e.g. `test_data/test_data2.csv`. The program then parses through and analyzes the file, retrieving the metrics mentioned above. These metrics are then outputted into a corresponding JSON file (e.g. `test_data2.json`) located within the same respository.

In addition, the program generates a logging file, called `sequence.log`, which details certain information, errors, and warnings related to the program, including:

- `INFO`: when the program is starting analysis of a new ECG data file
- `INFO`: when the program has finished reading the file
- `ERROR`: if the data file contains incomplete or bad data, i.e. either a value in a time, voltage pair is missing, contains a non-numeric string, or is NaN
- `WARNING`: if the data file contains a voltage reading outside the normal range (+/- 300mV)
- `INFO`: when the program is assigning a dictionary entry containing the appropriate metrics
- `INFO`: when the program has generated a corresponding JSON file

## Beat (Peak) detection
The program detects heart beats based on the Pan-Tompkins algorithm, which is commonly used to isolate and detect QRS complexes in the ECG signal. The algorithm consists of four general steps:

- bandpass filter: minimize baseline wander and noise
- differentiation: emphasize R peaks, which have steeper slopes than P/T waves
- squaring: further enhance the dominant (R) peaks
- integration: smooth out the signal for more accurate peak detection

Bandpass filtering is performed using a forward-backward Butterworth digital filter defined within the SciPy module. The Butterworth filter provides a flat passband with a 20 dB roll-off, and the forward-backward method was used to avoid a significant phase delay. Differentiation is performed using `numpy.ediff1d`, while integration was performed using `numpy.convolve`.

After this signal transformation is performed, the QRS peaks are detected using `scipy.signal.find_peaks`, which allows detection of peaks based on parameters such as height, threshold, distance, prominence, and width. The two parameters used in this program was distance (since there is a minimum distance between sequential QRS complexes) and prominence. Height is not used because the heights of peaks varied significantly between files.

## Heart Rate Calculation
The average heart rate is calculated using what is returned by the function in the program that detects QRS complexes, which is an array containing the indices corresponding to detected R peaks. The associated `calc_bpm` function also utilizes the sampling frequency of the ECG strip.

First, the average period of each beat is calculated: ((index of last peak)-(index of first peak))/(number of beats). This period is in terms of the number of indices, and is then converted to seconds by dividing by the sampling frequency (which is essentially the number of indices per second). 

Subsequently, the average heart rate in bpm is calculated as 60 (sec/min) divided by the period of each beat in seconds (sec/beat).

## References
- https://en.wikipedia.org/wiki/Pan-Tompkins_algorithm
- https://biopac.com/knowledge-base/extracting-heart-rate-from-a-noisy-ecg-signal/
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.sosfiltfilt.html#scipy.signal.sosfiltfilt
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
- https://github.com/marianpetruk/ECG_analysis
