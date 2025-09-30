# Extreme Value Analysis
## Univariate EVA
### Block Maxima - Empirical return periods
Following the Block Maxima approach (Coles, 2001), the observation record is here divided into non-overlapping periods of equal length and restricts attention to the maximum observation in each block. The resulting series of annual maxima is then fitted with the GEV distribution, allowing the estimation for return levels, defined as quantiles corresponding to specidic return periods. In this way, observed extremes are associated with probabilities, and extrapolation beyond the observed record becomes possible. It should be said, however, that while GEV distribution provides the theoretical foundation for modeling block maxima, its derivation assumes underlying stationarity. Coles (2001, §6) emphasizes that environmental processes rarely satisfy this assumption due to seasonal cycles and long-term trends. In fact, non-stationary time series are characterized by statistical properties that vary in time due to changes in the dynamic system (Mentaschi et al., 2016). As pointed out by Coles (2001), a general theory about non-stationary extreme value analysis (EVA) has not been formulated. Instead, different methodologies has been developed to analyze the extreme values in series that do not respect the statioarity assumption: from the expression of extreme value distribution parameters as time-varying parametric functions to model extremes of the non-stationary series, to the "stationary on slice" method, which divides those series into quasi-stationary and apply the stationary theory to each slice. In this study, the method used is the one proposed by Mentaschi et al. (2016): the transformed-stationary (TS) extreme value methodology. This approach consists of (i) transforming a non-stationary time series into a stationary series, (ii) performing a stationary EVA, and (iii) reverse transforming the resulting extreme value distribution into a time-dependent one.

In practice, the data here are divided into annual blocks, from which only the **annual maximum** value is considered, creating a shorter series of 12 values for 2010-2021 (1). The **GEV distribution is then fitted to these annual maxima** (2), with shape, location and scale parameters estimated through maxima likelihood estimation (MLE). Then, the return periods are computed as the reciprocal of exceedance probability, T = 1/p. The corresponding return level (3) q = 1 - 1/T is the quantile of the fitted GEV distribution that is exceeded with probability 1/T in any given year (Coles, 2001, §3.2).

In the code, once the GEV parameters are estimated, each observed annual maximum is assigned to an empirical return period using the Weibull plotting position (4): Temp = (n+1)/m, where n is the number of annual maxima and m is the rank of the maximum (from the largest = 1, to the smallest = n). At the same time, the fitted GEV is used to compute the theoretical return level curve across a smooth grid of return periods up to a safe maximum (≈3× record length).

Lastly, the comparison of the empirical estimates from data (points) with the fitted model (curve) is here paralelly proposed for both the raw time series and the detrended anomalies.

<img width="1189" height="397" alt="image" src="https://github.com/user-attachments/assets/fc2fe1f1-1c93-4fab-9226-33164c1d9611" />

Given the very short block maxima series, with only 12 years of data, the Maximum Likelihood Estimation method to estiamte the GEV parameters is very unstable. This is evident in the Volta Estuary River dicharge Return Levels for raw data: here the GEV curve explodes upwards very fast, wich is an unrealistic extrapolation.

Therefore, for short records such as this one, it is convinent to use Probability Weighted Moments (or L-moments), which is a much more robust method with short hydrological recors, and which produces more stable and realistic return levels.

<img width="1189" height="397" alt="image" src="https://github.com/user-attachments/assets/a7865918-9a89-4b51-9331-5a8f6075a972" />

Both panels show that the GEV estimate with L-moments provides a relatively more stable and theoretically consistent fit. However, the GEV curve is estimated here on an extremely small sample, since the dataset spans only over 12 years (2010-2021). The Block Maxima approach, then, implieas a significant loss of information, since it only uses annual maxima, ignoring all other extreme events that might happen in the same year. In small datasets, as the one in exam, this means wasting great part of the information contained in the series. This highly limits the GEV capability to well represent the tail distribution of extremes, leading to eventual underestimates or overestimates of the return periods, expecially for the longer ones (>10 years). To avoid this limit, and estimate return periods of 15-30 years in a robust way, it is convinient to consider another extreme analysis method.

### Peaks-Over-Threshold
An alternative to the block maxima approach is the Peaks-Over-Threshold (POT) method, which avoids discharding potentially useful information by considering all observations that exceed a sufficiently high threshold. Instead of retaining only the single maximum value within each block (e.g., one per year), the POT approach models the **distribution of threshold exceedances**. Extreme value theory shows that, for a suitably high threshold, the distribution of excesses over the threshold converges to the Generalized Pareto Distribution (GPD), that is the theoretical distribution of threshold exceedances (Coles, 2001, §5.3). Thus, the POT method provides a more efficient use of the data, since multiple extreme observations within the same year may be included, rather than only the annual maximum.

In hydrological applications, the POT method is particularly valuable when the observation record is relatively short, as this is our case, or when several significant flood peaks occur within a single year. A key practical challenge, however, is the choice of threshold: it must be high enough for the GPD approximation to hold, yet low enough to retain a sufficient number of exceedances for reliable inference (Dupuis, 1999; Naess, 2024).

To find the suitable threshold values for the non-stationary data sereis in exam the following workflow is proposed.

1) Initial statioary thresholds will be tested, using the empirical quantiles of the series and in particular the percentiles between 95th and 98th for the detrended series anomalies (taken instead of the raw data to overcome the non-stationarity inconvinient).
2) Diagnostic tools for threshold adequacy will be used to ensure linearity above candidate thresholds (which suggests a reasonable GPD), stability, and approximate independence of threshold exceedances.
3) If diagnostics show residual seasonality (e.g., non-uniform exceedance rates by month), move to a time-varying threshold.

#### Threshold selection
##### Stationary thresholds

In the following (step 1 of thrshold selection process), a function loops first through the raw time series and then through the detrended anomaly series, finds and selects all days where discharge or water level exceed a high threshold, fixed for different percentile values (95th, 98th, 99th). For each exceedance, it starts a cluster, creating groups of consecutive exceedances to avoid counting one long flood or surge as multile events. These clusters continue until the series has been below the threshold value for a period of ≥ `run` days (3 for water level, 7 for river discharge), where `run` is the minimum gap to separate two clusters. From each cluster, the function `decluster` extracts only the single maximum (the representative extreme). Then, it returns the timestamps and values of these cluster peaks.

Raw data with 95th percentile
- RD peaks (capped): 11  | rate ≈ 0.92 events/yr;
- WL peaks (capped): 29  | rate ≈ 2.42 events/yr;
- Observed joint days: 15.
<img width="987" height="490" alt="image" src="https://github.com/user-attachments/assets/46735b2c-2384-47bc-a5e0-4f80f5ab17f7" />
<img width="539" height="490" alt="image" src="https://github.com/user-attachments/assets/23db6618-8d20-4388-8ba8-7033459fa812" />

Raw data with 98th percentile
- RD peaks (capped): 5  | rate ≈ 0.42 events/yr
- WL peaks (capped): 18  | rate ≈ 1.50 events/yr
- Observed joint days: 3
<img width="987" height="490" alt="image" src="https://github.com/user-attachments/assets/e01afa4c-206d-44dc-bfbd-46e32d05aba4" />
<img width="539" height="490" alt="image" src="https://github.com/user-attachments/assets/e455b2ed-c5c6-4a6e-938f-6f7f8702b2b5" />

Raw data with 99th percentile
- RD peaks (capped): 4  | rate ≈ 0.33 events/yr
- WL peaks (capped): 13  | rate ≈ 1.08 events/yr
- Observed joint days: 0
<img width="987" height="490" alt="image" src="https://github.com/user-attachments/assets/cbb1f6ac-6f96-4946-8752-a1e9bc6ffc30" />
<img width="539" height="490" alt="image" src="https://github.com/user-attachments/assets/15b158a0-075c-435d-8e71-cda41b25a96a" />

##### POT diagnostics: MRL, parameter stability, exceedance rate

After trying different percentiles as stationary thresholds, the second step of this selection process consists in ascertaining threshold adequacy. This means to make **MRL (mean residual life) curves**, since linearity with MRL above candidate threshold suggests GPD is reasonable, and **parameter-stability plots (ξ, σ)** across a grid of high thresholds, preferably on the detrended anomalies and using declustered peaks so the i.i.d. assumption is less violated. Lastly, the exceedance rate is comparted to the thresholds as a **sanity check** trade-off between bias (too low threshold) and variance (too high threshold).

The reslunting plots examine the sensitivity of GP parameter estimates to the threshold, as described in Coles (2001, chapter 4) and Scarrott and MacDonald (2012). Over a range of values of thresholds = u, estimates ξ of the shape and σ − ξ of the modified scale are plotted against u with pointwise 95% symmetric confidence intervals (Northrop & Coleman, 2014). The lowest threshold above which these quantities are judged to be approximately constant in u is selected, taking into account sampling variability summarized by the confidence intervals.

<img width="630" height="399" alt="image" src="https://github.com/user-attachments/assets/8f4261e4-8059-4a14-85f9-bf5d2a157605" />
<img width="989" height="390" alt="image" src="https://github.com/user-attachments/assets/e1760ed1-bae4-4d77-ac97-dde19237b028" />
<img width="629" height="399" alt="image" src="https://github.com/user-attachments/assets/788edf61-0567-4a57-9181-6154784503ef" />

<img width="629" height="399" alt="image" src="https://github.com/user-attachments/assets/2b14985b-c6d8-4c30-9dd2-deb12abfd59c" />
<img width="989" height="390" alt="image" src="https://github.com/user-attachments/assets/cb75a809-994c-4b1e-a95c-05e5e4da2d21" />
<img width="629" height="399" alt="image" src="https://github.com/user-attachments/assets/7388fb74-0b42-483c-a323-26c2fe304e30" />

##### Fit GPD to exceeadnce
<img width="630" height="420" alt="image" src="https://github.com/user-attachments/assets/4377cbea-2126-4998-a033-956e07be02a1" />
<img width="630" height="420" alt="image" src="https://github.com/user-attachments/assets/b59fff49-40e3-49fa-bd0e-da25ed55bb8b" />

## Bivariate Extreme Analysis
### Identification of compound events

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>quantile_q</th>
      <th>lag_days</th>
      <th>u_RD</th>
      <th>u_WL</th>
      <th>n_AND_days (A)</th>
      <th>n_lagged_episodes (B)</th>
      <th>n_OR_days (C)</th>
      <th>n_A_intersect_B</th>
      <th>n_A_intersect_C</th>
      <th>n_B_intersect_C</th>
      <th>n_A_intersect_B_intersect_C</th>
      <th>jaccard_A_B</th>
      <th>jaccard_A_C</th>
      <th>jaccard_B_C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.90</td>
      <td>0</td>
      <td>4336.023438</td>
      <td>0.0750</td>
      <td>42</td>
      <td>0</td>
      <td>147</td>
      <td>0</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.285714</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.90</td>
      <td>1</td>
      <td>4336.023438</td>
      <td>0.0750</td>
      <td>42</td>
      <td>0</td>
      <td>147</td>
      <td>0</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.285714</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.90</td>
      <td>2</td>
      <td>4336.023438</td>
      <td>0.0750</td>
      <td>42</td>
      <td>0</td>
      <td>147</td>
      <td>0</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.285714</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.90</td>
      <td>3</td>
      <td>4336.023438</td>
      <td>0.0750</td>
      <td>42</td>
      <td>0</td>
      <td>147</td>
      <td>0</td>
      <td>42</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.285714</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.95</td>
      <td>0</td>
      <td>6597.639062</td>
      <td>0.0840</td>
      <td>15</td>
      <td>0</td>
      <td>80</td>
      <td>0</td>
      <td>15</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.187500</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.95</td>
      <td>1</td>
      <td>6597.639062</td>
      <td>0.0840</td>
      <td>15</td>
      <td>0</td>
      <td>80</td>
      <td>0</td>
      <td>15</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.187500</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.95</td>
      <td>2</td>
      <td>6597.639062</td>
      <td>0.0840</td>
      <td>15</td>
      <td>0</td>
      <td>80</td>
      <td>0</td>
      <td>15</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.187500</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.95</td>
      <td>3</td>
      <td>6597.639062</td>
      <td>0.0840</td>
      <td>15</td>
      <td>0</td>
      <td>80</td>
      <td>0</td>
      <td>15</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.187500</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.98</td>
      <td>0</td>
      <td>8814.505937</td>
      <td>0.0941</td>
      <td>3</td>
      <td>0</td>
      <td>37</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.081081</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.98</td>
      <td>1</td>
      <td>8814.505937</td>
      <td>0.0941</td>
      <td>3</td>
      <td>0</td>
      <td>37</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.081081</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.98</td>
      <td>2</td>
      <td>8814.505937</td>
      <td>0.0941</td>
      <td>3</td>
      <td>0</td>
      <td>37</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.081081</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0.98</td>
      <td>3</td>
      <td>8814.505937</td>
      <td>0.0941</td>
      <td>3</td>
      <td>0</td>
      <td>37</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
      <td>0.081081</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>

### Dependence analysis 
To investigate the co-occurrence and statistical dependence of extreme river discharge (RD) and water level (WL), it is proposed here a combination of correlation metrics (2), tail dependence measures (3), and event coincidence analysis (4).
1) **Identify compound events**
<img width="1173" height="558" alt="image" src="https://github.com/user-attachments/assets/8b4b0cb4-246e-4f09-98a9-9519cdf62b26" />
<img width="828" height="329" alt="image" src="https://github.com/user-attachments/assets/dd55988f-6d5a-4cd7-a873-5f60811c31bf" />
<img width="828" height="329" alt="image" src="https://github.com/user-attachments/assets/792d032c-e4b0-4ce3-b13a-2913ee98deac" />
<img width="615" height="509" alt="image" src="https://github.com/user-attachments/assets/339269ae-f3de-497f-860a-7e493e5a24cd" />

2) **Dependence Analysis**
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>metric</th>
      <th>estimate</th>
      <th>lo95</th>
      <th>hi95</th>
      <th>n</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Spearman rho (all)</td>
      <td>-0.214773</td>
      <td>-0.315238</td>
      <td>-0.101617</td>
      <td>4383</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Kendall tau (all)</td>
      <td>-0.140350</td>
      <td>-0.204338</td>
      <td>-0.067315</td>
      <td>4383</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Pearson r log (all)</td>
      <td>-0.126264</td>
      <td>-0.232502</td>
      <td>-0.008320</td>
      <td>4383</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Spearman rho (Union exceed (q=0.95))</td>
      <td>-0.692725</td>
      <td>-0.761582</td>
      <td>-0.510314</td>
      <td>424</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Kendall tau  (Union exceed (q=0.95))</td>
      <td>-0.460757</td>
      <td>-0.525091</td>
      <td>-0.321931</td>
      <td>424</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Pearson r log (Union exceed (q=0.95))</td>
      <td>-0.762069</td>
      <td>-0.880994</td>
      <td>-0.624546</td>
      <td>424</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Spearman rho (AND exceed (q=0.95))</td>
      <td>0.071429</td>
      <td>-0.628865</td>
      <td>0.710454</td>
      <td>15</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Kendall tau  (AND exceed (q=0.95))</td>
      <td>0.104762</td>
      <td>-0.460000</td>
      <td>0.500000</td>
      <td>15</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Pearson r log (AND exceed (q=0.95))</td>
      <td>0.048047</td>
      <td>-0.494754</td>
      <td>0.693120</td>
      <td>15</td>
    </tr>
  </tbody>
</table>
</div>


To remove marginal effects and focus on dependence, raw values are transformed into pseudo-observations using the empirical probability integral transform, i.e., ranks scaled by sample size (r/(n+1)) as in Bevacqua et al., 2019.

This code sets up a block bootstrap: a procedure adapted for serially dependent data (such as time series) to construct confidence intervals of tail dependence metrics. Both Gilleland (2020) and Wilks (2011) discuss block bootstrap methods in the context of dependent (time‐correlated) atmospheric data. They specified the importance of this technique, as standard i.i.d. bootstrap assumes independence, which is violated in time series with autocorrelation. Here, the Circular Block Bootstrap is implemented, ansuring every index is elegible. 

<img width="610" height="409" alt="image" src="https://github.com/user-attachments/assets/6614eba2-c9d5-4fe1-9aca-f4f1f87e3622" />
<img width="609" height="409" alt="image" src="https://github.com/user-attachments/assets/f1ffbcf1-e6d3-4a2d-9dcc-abfff2dc3821" />
<img width="610" height="409" alt="image" src="https://github.com/user-attachments/assets/a94839ff-7ba4-44a2-8d60-25feacff94bf" />


3) **Multivariate and joint probability modeling**

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>family</th>
      <th>loglik</th>
      <th>AIC</th>
      <th>BIC</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Gaussian</td>
      <td>-8.881784e-14</td>
      <td>2.000000</td>
      <td>7.382124</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Student-t(df=40)</td>
      <td>-5.861207e+00</td>
      <td>15.722413</td>
      <td>26.486662</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Frank</td>
      <td>-1.818601e+02</td>
      <td>365.720242</td>
      <td>371.102367</td>
    </tr>
  </tbody>
</table>
</div>

[best copula] Gaussian
RD: u=6.6e+03, xi=-0.132, sigma=2.79e+03, n_exc=220, daily p>u=0.0502
WL: u=0.084, xi=-0.161, sigma=0.0116, n_exc=219, daily p>u=0.0500
[AND @ (RD=6.6e+03, WL=0.084)] p=2.508e-03 → T≈398.73 yrs  (u=0.950, v=0.950, C(u,v)=0.902, copula=Gaussian)

<Figure size 640x480 with 1 Axes><img width="629" height="470" alt="image" src="https://github.com/user-attachments/assets/774e839a-f672-4a37-a344-7e601ab3081f" />
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>target</th>
      <th>RD</th>
      <th>WL</th>
      <th>p_AND</th>
      <th>T_years</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>q95 per-margin</td>
      <td>6597.639062</td>
      <td>0.0840</td>
      <td>0.002508</td>
      <td>398.727460</td>
    </tr>
    <tr>
      <th>1</th>
      <td>q98 per-margin</td>
      <td>8814.505937</td>
      <td>0.0941</td>
      <td>0.000423</td>
      <td>2366.487977</td>
    </tr>
  </tbody>
</table>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>family</th>
      <th>loglik</th>
      <th>AIC</th>
      <th>BIC</th>
      <th>info</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Gaussian</td>
      <td>-4.252154e-14</td>
      <td>2.000000</td>
      <td>6.726233</td>
      <td>{'rho': [[1.0, 0.0], [0.0, 1.0]]}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Student-t</td>
      <td>-1.270292e+00</td>
      <td>6.540583</td>
      <td>15.993050</td>
      <td>{'rho': [[1.0, 0.0], [0.0, 1.0]], 'df': 40}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BB1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>BB1 unavailable (pip install copulae)</td>
    </tr>
  </tbody>
</table>
</div>

<img width="669" height="530" alt="image" src="https://github.com/user-attachments/assets/818d9667-c157-4e21-b1eb-75cb473a5dd4" />
<img width="669" height="530" alt="image" src="https://github.com/user-attachments/assets/6a1b675f-85b0-4eb0-8cf9-1b634dd0558b" />
[notes]
• Marginals: semi-parametric (empirical below 95th pct; POT-GPD above).
• Dependence fitted on union exceedances (q_dep=0.90) to focus on the tail.
• BB1 fit uses copulae (method='mpl'); if unavailable, only Gaussian & Student-t are used.
• Joint AND return periods are capped to 50 years in the summaries and plots.
• To enable BB1:  pip install copulae   # then restart kernel and re-run.












