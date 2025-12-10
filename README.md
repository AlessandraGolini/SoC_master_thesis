# Characterisation of Compound Coastal Flooding in Keta Basin
## Abstract
Low-lying coastal areas such as the Ghanaian coasts are increasingly exposed to multiple, interacting climate hazards that threaten ecosystems, livelihoods, and infrastructures. Compound flooding, where the combination or successive occurrence of two or more flood drivers leads to a greater impact, can exacerbate the adverse consequences of flooding, particularly in coastal–estuarine regions. This thesis delineates a reproducible framework for compound flooding characterisation in data-scarce environments, bridging the climate-informed data analysis to the planning and evaluation of Nature-based Solutions (NbS) for coastal risk reduction. To address this overarching goal, the research assesses and validates multi-source climate datasets, notably the GloFAS hydrological reanalysis and the JRC offshore water level dataset, and then characterises the statistical behaviour of extreme river discharge and water level through univariate and bivariate Extreme Value Analyses (EVA), combining percentile-based thresholding, Peaks-Over-Threshold fitting, and copula-based modelling to identify and quantify compound coastal–fluvial flood events. The results demonstrate that river discharge and coastal water level extremes in the Volta Delta region, where Keta basin is, exhibit strong but asynchronous seasonality, limited long-term trends, and weak tail dependence, indicating that compound events are infrequent and primarily driven by temporal coincidence rather than strong physical coupling. Lastly, a third phase of the framework is conceptually outlined as future work, proposing the generation of synthetic extreme events through the UNprecedented Simulated Extremes using ENsembles (UNSEEN) approach to enrich the historical characterisation of compound flooding, by expanding the observational records with physically plausible, yet historically unobserved, extreme events. This would enable the subsequent evaluation of NbS performance under plausible, non-observed scenarios.

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

**Methods**
The "script" folder contains the reproducible code for the Compound Flooding Analysis in the Keta Basin (Ghana), with the following steps:
    - Phase I - Data acquisition, preprocessing, and exploratory analysis.
    - Phase II – Characterisation of Extremes and Compound Flooding
          - Univariate Extreme Value Analysis, through Block Maxima and Peaks Over Threshold approaches;
          - Bivariate Extreme Value Analysis.

