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
