# Compound Flooding in the Keta Basin, Ghana
### Characterisation of Extreme Events from Multi-Decadal Reanalysis Data

This repository contains the code and analysis for the detection and characterisation of compound flooding events in the Keta Basin (Ghana).
The study investigates the interaction between river discharge and coastal water levels/waves, using reanalysis datasets for the period 2010-2021, with the goal of identifying extreme compound events and providing a first synopsis of their drivers.

## Methodology
The workflow is divided as follows:

 1. `data_load_preprocessing` 
    + Load reanalysis datasets (GloFAS river discharge, coastal water levels).
    + Extract the grid points closest to the Keta Basin, Ghana.
    + Perform basic cleaning: missing values, unit checks, and alignment of datasets on a common timeline.
    + Output: ready-to-use time series of discharge (rd_estuary, rd_lake) and water levels (wl_estuary).

2. `variability_analysis` explores the temporal variability and distribution of the datasets by:
    + Mapping the mean discharge climatology and mark analysis points (estuary, Volta lake).
    + Plotting raw and monthly-mean time series for river discharge (RD) and water level (WL).
    + Computing monthly climatology and monthly anomalies; fitting and remove linear trends; plotting detrended anomalies.
    + Highlighting seasonal behaviour (e.g., Sep–Dec) for RD and WL.
    + Inspecting frequency content with a one-sided FFT (period–amplitude), focusing on sub-annual to multi-year scales.
    + It then compares distributions with PDFs of raw series and detrended anomalies, and estimates joint PDF (RD–WL) to assess co-variability as a prelude to compound analysis.
 
3. `POT_extremes`
    + The Peak Over Threshold (POT) method is applied to detect extreme events, following Hendry et al. 2019 (https://doi.org/10.5194/hess-23-3117-2019).
    + Thresholds are adapted to yield ~2–5 exceedances per year (consistent with Extreme Value Theory).
    + Identify extreme events separately for discharge and water levels.
    + Combine the two dimensions to detect compound flooding events:
        + Univariate extremes (river-only or coastal-only).
        + Compound extremes (simultaneous extremes).

