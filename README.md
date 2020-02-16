# PP_miRNA_arrays
A post-processing algorithm for miRNA microarray data, http://dx.doi.org/10.3390/ijms21041228.

## Introduction
This repository contains a tool for post-processing miRNA microarray data. Namely, the program calculates score (float between 0 and 1) for each pre-miRNA—mature-miRNA pair based on median miRNA expression level, Spearman correlation between precursor and mature miRNA and MIMAT accession number. The closer score to 1 the more likely that miRNA is really expressed in considered samples.

## Installation
Just clone this repository in your working project. You should have the following dependencies installed:
- python3
- numpy
- scipy.stats

## Usage
The algorithm need to be executed in two steps:
### Step 1 (need to be done only once)
Download and prepare miRBase (http://mirbase.org/) files for the next step by simply running this command:
```
./configure_miRBase.bash
```
miRBase and python versions can be tweaked by editing first lines of the script.
### Step 2
Run the main script:
```
python score.py input_table.tsv
```
Input tab-separated expression table should contain pre-miRNA and mature-miRNA expression values across samples (see example_input.tsv file for a clear example). Please note that the table should contain header and accession IDs should be presented in "MI" / "MIMAT" forms.
All output in format "pre-miRNA | mature miRNA | Score" will be printed to the stdout.
