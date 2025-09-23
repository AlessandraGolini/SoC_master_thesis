##### Transformed Stationary approach to Extreme Value Analysis (Mentaschi et al. 2016)

# install.packages("RtsEva")   # run only the first time
library(RtsEva)

### 1) Argument selection ------------------------------------------------------
timeWindow_days <- 6*365.25         # running window for trend/scale (~6 yrs)
transfType      <- "trendPeaks"     # "trend" for std | "trendPeaks" | "trendCIPercentile"
tail_type       <- "high"           # floods and surges hazard: high tail
minPeak_RD      <- 7                # declustering per RD
minPeak_WL      <- 3                # declustering per WL
trans_code      <- "ori"            # 'ori' per code alte
TrendTh_use     <- 0.90             # soglia su percentili per trendPeaks (0–1)
Tmax_plot       <- 30               # limite per i ritorni POT (anni)


### 2) Prepare inputs for TSEVA

# FILE RD e WL (already exported from Python with columns: time, series)
DATADIR <- "C:/Users/aless/Desktop/tesi/SoC_master_thesis_git/script"
keta_RD <- file.path(DATADIR, "keta_RD_daily.csv")
keta_WL <- file.path(DATADIR, "keta_WL_daily.csv")

read_series <- function(path_csv){
  df <- read.csv(path_csv)
  stopifnot(all(c("time","series") %in% names(df)))
  df$time <- as.Date(df$time)
  full <- data.frame(time = seq(min(df$time, na.rm=TRUE),
                                max(df$time, na.rm=TRUE),
                                by="day"))
  df <- merge(full, df, by="time", all.x=TRUE)
  names(df) <- c("timestamp","data")
  df <- max_daily_value(df) # the series already is daily 
  df
}

timeAndSeries_RD <- read_series(keta_RD)
timeAndSeries_WL <- read_series(keta_WL)


###  3) Run TSEVA

# RD: minPeakDistanceInDays tuned for hydrograph separation (~7d)
NonStat_RD <- TsEvaNs(
  timeAndSeries = timeAndSeries_RD,
  timeWindow    = timeWindow_days,
  transfType    = "trendPeaks",
  TrendTh       = 0.90,          # <-- 0.90 = 90° percentile
  tail          = tail_type,
  minPeakDistanceInDays = minPeak_RD,
  trans         = "ori"
)

# WL: shorter separation for surge events (~3d)
NonStat_WL <- TsEvaNs(
  timeAndSeries = timeAndSeries_WL,
  timeWindow    = timeWindow_days,
  transfType    = "trendPeaks",
  TrendTh       = 0.90,          # <-- 0.90 = 90° percentile
  tail          = tail_type,
  minPeakDistanceInDays = minPeak_WL,
  trans         = "ori"
)

### 4) Extract objects and delete NA without dropping rows

# Extraction
nonStationaryEvaParams_RD <- NonStat_RD[[1]]  # EVA results (POT/GPD and GEV) already re-transformed into the original domain
stationaryTransformData_RD <- NonStat_RD[[2]] # TS transformation

nonStationaryEvaParams_WL <- NonStat_WL[[1]]
stationaryTransformData_WL <- NonStat_WL[[2]]

# helper: fill NA with linear interpolation (without changing the length)
.fill_na_linear <- function(x) {
  i <- which(!is.na(x))
  if (length(i) < 2) return(x)
  xx <- seq_along(x)
  x[is.na(x)] <- approx(xx[i], x[i], xout = xx[is.na(x)], rule = 2)$y
  x
}

fix_stationary_no_drop <- function(st) {
  st$timeStamps <- as.Date(st$timeStamps)
  L <- length(st$timeStamps)
  # prendi tutte le serie numeriche con stessa lunghezza di timeStamps
  fields <- names(st)[vapply(st, function(v) is.numeric(v) && length(v)==L, logical(1))]
  for (nm in fields) st[[nm]] <- .fill_na_linear(st[[nm]])
  st
}

# apply fix (no drop, interpolation only)
stationaryTransformData_RD <- fix_stationary_no_drop(stationaryTransformData_RD)
stationaryTransformData_WL <- fix_stationary_no_drop(stationaryTransformData_WL)

# sanity check: no NA and same lengths
stopifnot(
  length(stationaryTransformData_RD$timeStamps) ==
    length(stationaryTransformData_RD$nonStatSeries),
  all(!is.na(stationaryTransformData_RD$nonStatSeries)),
  length(stationaryTransformData_WL$timeStamps) ==
    length(stationaryTransformData_WL$nonStatSeries))
  all(!is.na(stationaryTransformData_WL$nonStatSeries))
)

### %) Plot results

## --- RD ---
# esempio RD - immagine GPD
tsEvaPlotGPDImageScFromAnalysisObj_safe <- function(Y, nonStationaryEvaParams, stationaryTransformData,
                                                    trans = "ori", ...) {
  # time e serie originali
  timeStamps <- as.Date(stationaryTransformData$timeStamps)
  serix      <- as.numeric(stationaryTransformData$nonStatSeries)
  
  # imputazione NA extra di sicurezza
  .fill_na_linear <- function(x) {
    i <- which(!is.na(x)); xx <- seq_along(x)
    if (length(i) >= 2) x[is.na(x)] <- approx(xx[i], x[i], xout = xx[is.na(x)], rule = 2)$y
    x
  }
  serix <- .fill_na_linear(serix)
  
  # se (per qualunque motivo) le lunghezze differiscono, le rendiamo uguali
  L <- min(length(timeStamps), length(serix))
  if (length(timeStamps) != L) timeStamps <- timeStamps[seq_len(L)]
  if (length(serix)      != L) serix      <- serix[seq_len(L)]
  
  # parametri tempo-varianti della GPD
  epsilon   <- nonStationaryEvaParams[[2]]$parameters$epsilon
  sigma     <- nonStationaryEvaParams[[2]]$parameters$sigma
  threshold <- nonStationaryEvaParams[[2]]$parameters$threshold
  
  # picchi e loro tempi (salviamo da out-of-range)
  peax   <- nonStationaryEvaParams[[2]]$parameters$peaks
  peaxID <- pmin(pmax(nonStationaryEvaParams[[2]]$parameters$peakID, 1L), L)
  peakplot <- data.frame(time = timeStamps[peaxID], value = peax)
  
  # chiamiamo la funzione base
  tsEvaPlotGPDImageSc(Y, timeStamps, serix, epsilon, sigma, threshold, peakplot, trans, list(...))
}

# --- RD ---
ExRange_RD <- range(nonStationaryEvaParams_RD$potObj$parameters$peaks, na.rm=TRUE)
wr2_RD     <- seq(ExRange_RD[1], ExRange_RD[2], length.out=700)
minYear_RD <- format(min(stationaryTransformData_RD$timeStamps, na.rm=TRUE), "%Y")

Plot1_RD <- tsEvaPlotGPDImageScFromAnalysisObj_safe(
  wr2_RD, nonStationaryEvaParams_RD, stationaryTransformData_RD,
  trans = "ori", minYear = minYear_RD
)
Plot1_RD