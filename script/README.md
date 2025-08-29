# Compound Flooding in the Keta Basin, Ghana
### Characterisation of Extreme Events from Multi-Decadal Reanalysis Data

This repository contains the code and analysis for the detection and characterisation of compound flooding events in the Keta Basin (Ghana).
The study investigates the interaction between river discharge and coastal water levels/waves, using reanalysis datasets for the period 2010-2021, with the goal of identifying extreme compound events and providing a first synopsis of their drivers.

## Methodology
The workflow is divided as follows:

 1. data_load_preprocessing
    + Load reanalysis datasets (GloFAS river discharge, coastal water levels/waves).
    + Extract the grid points closest to the Keta Basin, Ghana.
    + Perform basic cleaning: missing values, unit checks, and alignment of datasets on a common timeline.
    + Output: ready-to-use time series of discharge (rd_estuary, rd_lake) and water levels (wl_estuary).

2. variability_analysis

Explore the temporal variability of the datasets.

Compute basic statistics (mean, standard deviation, seasonal cycles).

Plot time series and variability at different scales (daily, monthly, annual).

Identify potential drivers of variability in river discharge and water levels.

3. POT_extremes

Apply the Peak Over Threshold (POT) method to detect extreme events.

Thresholds adapted to yield ~2–5 exceedances per year (consistent with Extreme Value Theory).

Identify extreme events separately for discharge and water levels.

Combine the two dimensions to detect compound flooding events:

Univariate extremes (river-only or coastal-only).

Compound extremes (simultaneous extremes).

Visualise results using scatter plots and exceedance contours.
