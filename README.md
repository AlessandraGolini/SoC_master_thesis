# Master thesis project

## In this repo:
+ In the "script" folder:
  + the code for the compound flooding analysis in the Keta Basin.
 
(to be added):
+ In the "main results" folder:
  + the results obtained from the analysis are birefly described and discussed.
+ In the "document" folder:
  + uptdating drafts of the thesis document are saved.

## Compound Flooding Analysis 
**Objective:** Quantify the relationship between river discharge and offshore water level extremes at the Volta River Estuary, in the Keta Basin (Ghana), to assess compound flooding potential.

**Study Area:**
- Volta River Estuary, Ghana
- Estuary bounds: lat [5.73, 5.83]°, lon [0.64, 0.75]°
- Context bounds for maps: lat [3, 9]°, lon [−3, 3]°
- Reference points: at the mouth river (0.667E  5.77N) and at the Volta Lake (0.117E, 6.5N)

**Datasets:**
- **GloFAS v4.0**: provided by the CEMS Early Warning Data Store, the GloFAS dataset contains the **daily river discharge in the last 24 hours [m³ s⁻¹]** (`dis24`) for the period 2010–2021. 
- **JRC Maximum Daily Global Open Ocean Water Level**: the “Maximum Daily Global Open Ocean Water Level” dataset (JRC) provides a daily time series of offshore maximum water level reconstructed with a statistical PCVAR model. It combines: DUACS altimetry sea-level anomalies (sparse satellite observations), and ERA5 atmospheric predictors (10-m winds, mean sea-level pressure, pressure gradients), to produce a continuous daily record even where satellites didn’t pass on a given day. The key variable is  `waterLevelreanalysis(pointsSAT, time_1959_2021)`, whichi is an open-ocean daily maximum water level signal. The units of this daily maximum offshore water level is 10⁻⁴ m (to be converted in m by multiplying by 1e-4).


