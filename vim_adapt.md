# Use vim as my only editor

## Text (writing) 
- installing texlive to compile offline


## Coding with Python
The biggest problem would be how to NOT use jupyter notebook. 
The only feature that I need from jupyter is the cache of variables. Once I load the data, and make changes to the analysis or visualization, I don't want to reload data again. Therefore, several options:
- Run program, cache data. Load data, run program, cache data. ......
- What structure to use for caching data? Probably dict to json. 
    - shelve

So for each project, there should be several files:
- subprograms that contain key functions
- main file that assembly subprograms
- data cache

`[shelve](https://docs.python.org/3/library/shelve.html)` is pretty good. Here is an example. 

```python
# flag to force reprocessing data
force_reprocess = []
force_reprocess.append(False) # If the data beforehand is processed, then undoubtly this piece of data should also be processed.
with shelve.open(shelve_filename) as db:
    if not all(force_reprocess) and all(var in db for var in ['df', 'filtered_ch1', 'filtered_ch2', 'filtered_ch3']):
        print("Loading data from shelve...")
        df = db['df']
        filtered_ch1 = db['filtered_ch1']
        filtered_ch2 = db['filtered_ch2']
        filtered_ch3 = db['filtered_ch3']
    else:
        print('Reprocessing data')
        # Get the first element and import CSV data to a pandas DataFrame
        df = pd.read_csv(csv_files[0], skiprows=20)
        
        # Apply the median filter to the 'CH1' and 'CH2' columns
        filtered_ch1 = median_filter(df['CH1'], kernel_size=41)
        filtered_ch1 = lowpass_filter(filtered_ch1, cutoff_freq, sampling_rate)
        filtered_ch2 = median_filter(df['CH2'], kernel_size=51)
        filtered_ch2 = lowpass_filter(filtered_ch2, cutoff_freq, sampling_rate)
        filtered_ch3 = median_filter(df['CH3'], kernel_size=11)
        filtered_ch3 = lowpass_filter(filtered_ch3, cutoff_freq, sampling_rate)
    
        # Save the processed data to shelve
        db['df'] = df
        db['filtered_ch1'] = filtered_ch1
        db['filtered_ch2'] = filtered_ch2
        db['filtered_ch3'] = filtered_ch3
```
