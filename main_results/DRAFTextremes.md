<img width="1189" height="397" alt="immagine" src="https://github.com/user-attachments/assets/f50d06d8-8d56-4b1e-84b5-c5ea4385f4ec" />
<img width="1189" height="397" alt="immagine" src="https://github.com/user-attachments/assets/725e768b-a0dc-49ec-be05-3161a13310c4" />
These two sets of plots illustrate the difference between fitting a GEV model to raw non-stationary data versus to detrended anomalies.

RIVER DICHARGE: 
The return levels explode (10^6, 10^8, 10^9) → this is a classic symptom of unstable GEV fits due to non-stationarity + very few data points (12 annual maxima).
Computing the bootstrap CIs it becomes evident that they are absurdly wide (e.g., 4,472 – 2.3×10^7 for T=10), confirming the fit is unreliable.
This output is showing you that the GEV assumption is broken for the raw series.

For detrended anomaly, the central return levels look plausible (2-yr ≈ 2000 m³/s, 30-yr ≈ 19,000 m³/s), but the bootstrap CIs are still enormous: from ~200 up to 10^12 in the 30-yr case!
This means that even after detrending, the very limited length of available data (with only 12 data points) causes the parameter estimates, especially the shape ξ, to be very unstable.

WATER LEVEL:
On the other hand, return levels for water level increase smoothly (0.09 → 0.35 m across 2–30 years) and bootstrap intervals are tight (reasonable stability).
This is much more realistic and indicates the water level series is closer to stationary, so the GEV fit works.

Return levels for detrended anomalies of water level rise smoothly (0.035 → 0.16 m over 2–30 years), and CIs are relatively narrow, especially compared to discharge. This looks reliable and interpretable.
