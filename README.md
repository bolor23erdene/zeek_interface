# zeek_interface

## First converted all .log files into .log.csv files using bro2csv library

## The main.py has 4 main functions

### 1. extract_protocol_names: find all the protocol logs from the zeek official website 

### 2. specs_logs: convert all of the existing protocol logs into panda dataframe

### 3. free_text_func: return all the entries that contain the given free text

### 4. log_and_correlation: perform the log.query and uid matching and save .csv files 
