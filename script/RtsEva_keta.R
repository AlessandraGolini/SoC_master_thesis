##### Transformed Stationary approach to Extreme Value Analysis (Mentaschi et al. 2016)

### Installation of the adaptation of the Matalb tsEVA toolbox developed by Lorenzo Mentaschi.
# https://github.com/Alowis/RtsEva 

# install.packages("RtsEva")
library("RtsEva")


### Argument selection

timeWindow_days <- 6*365.25   # running window for trend/scale (~6 yrs)
trendtypes <- c("trend","trendPeaks","trendCIPercentile")
transfType <- "trendPeaks"    # "trend" for std
tail_type  <- "high"          # floods and surges hazard: high tail
ciPercentile <- 90            # only used by some plotting/CI routines
minPeak_RD <- 7               # declustering gap (days) for RD
minPeak_WL <- 3               # declustering gap (days) for WL
trans_code <- "ori"           # 'ori' for high tails; 'rev' for low tails

# Limit POT return times to Tmax (~3x data series length, of 12 years)
limit_T_in_pot <- function(nseva, Tmax = 30) {
  rl  <- nseva$potObj$returnLevels
  Tvec <- rl$T
  keep <- which(Tvec <= Tmax)
  
  # update T vector
  rl$T <- Tvec[keep]
  
  # update all components that have the size to T
  for (nm in setdiff(names(rl), "T")) {
    x <- rl[[nm]]
    if (is.matrix(x) && ncol(x) == length(Tvec)) {
      rl[[nm]] <- x[, keep, drop = FALSE]
    } else if (is.vector(x) && length(x) == length(Tvec)) {
      rl[[nm]] <- x[keep]
    } 
  }
  
  nseva$potObj$returnLevels <- rl
  nseva
}


### Prepare inputs for TSEVA

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



###  Run TSEVA

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


### Plot results

## --- RD ---
nonStationaryEvaParams_RD <- NonStat_RD[[1]]  # EVA results (POT/GPD and GEV) already re-transformed into the original domain
stationaryTransformData_RD <- NonStat_RD[[2]] # TS transformation

ExRange_RD <- c(min(nonStationaryEvaParams_RD$potObj$parameters$peaks, na.rm=TRUE),
                max(nonStationaryEvaParams_RD$potObj$parameters$peaks, na.rm=TRUE)) # range of declustered peaks used in POT (GPD
wr2_RD <- seq(min(ExRange_RD), max(ExRange_RD), length.out=700)                     # dense grid of flow rate values (in m³/s) on which the plot will evaluate the time-varying GPD queue.

minYear_RD <- format(min(stationaryTransformData_RD$timeStamps, na.rm=TRUE), "%Y")

Plot1_RD <- tsEvaPlotGPDImageScFromAnalysisObj(
  wr2_RD, nonStationaryEvaParams_RD, stationaryTransformData_RD,
  minYear = minYear_RD, trans = "ori"
)
Plot1_RD


timeIndex_RD <- 1
nonStationaryEvaParams_RD_30 <- limit_T_in_pot(nonStationaryEvaParams_RD, Tmax = 30)

Plot2_RD <- tsEvaPlotReturnLevelsGPDFromAnalysisObj(
  nonStationaryEvaParams_RD_30, stationaryTransformData_RD, timeIndex_RD,
  trans = "ori", ylabel = "Discharge (m3/s)"
)
Plot2_RD

Plot3_RD <- tsEvaPlotReturnLevelsGEVFromAnalysisObj(
  nonStationaryEvaParams_RD, stationaryTransformData_RD, timeIndex_RD,
  trans = "ori", ylabel = "Discharge (m3/s)"
); Plot3_RD


## --- WL ---
nonStationaryEvaParams_WL <- NonStat_WL[[1]]
stationaryTransformData_WL <- NonStat_WL[[2]]

ExRange_WL <- range(nonStationaryEvaParams_WL$potObj$parameters$peaks, na.rm=TRUE)
wr2_WL     <- seq(ExRange_WL[1], ExRange_WL[2], length.out=700)

minYear_WL <- format(min(stationaryTransformData_WL$timeStamps, na.rm=TRUE), "%Y")
timeIndex_WL <- 1

Plot1_WL <- tsEvaPlotGPDImageScFromAnalysisObj(
  wr2_WL, nonStationaryEvaParams_WL, stationaryTransformData_WL,
  minYear = minYear_WL, trans = "ori"
); Plot1_WL

Plot2_WL <- tsEvaPlotReturnLevelsGPDFromAnalysisObj(
  nonStationaryEvaParams_WL, stationaryTransformData_WL, timeIndex_WL,
  trans = "ori", ylabel = "Water level (m)"
); Plot2_WL

Plot3_WL <- tsEvaPlotReturnLevelsGEVFromAnalysisObj(
  nonStationaryEvaParams_WL, stationaryTransformData_WL, timeIndex_WL,
  trans = "ori", ylabel = "Water level (m)"
); Plot3_WL
