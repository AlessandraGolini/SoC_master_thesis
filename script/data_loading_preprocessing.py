# Compound Flooding Analysis in the Keta Basin, Ghana

##### Import libraries #####
# Standard library
import os
import glob

# Scientific computing
import numpy as np
import pandas as pd
import xarray as xr
from netCDF4 import Dataset

# Visualization
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Geospatial
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# cds
from cds_request import cds_request_keta

##### Define useful functions #####
def detrend_dim(da, dim="time", deg=1, baseline=None, return_trend=False, skipna=True):
    """
    Polynomial detrend along `dim` using xarray's native datetime handling.
    Optionally fit on a `baseline=(start, end)` window, apply to full series.
    """
    da_fit = da.sel({dim: slice(*baseline)}) if baseline else da
    p = da_fit.polyfit(dim=dim, deg=deg, skipna=skipna)
    fit = xr.polyval(da[dim], p.polyfit_coefficients).astype(da.dtype)
    detr = (da - fit).assign_attrs(da.attrs)
    detr.name = (da.name or "var") + "_detrended"
    if return_trend:
        fit.name = (da.name or "var") + "_trend"
        return detr, fit
    return detr

def anom(xarr, baseline=('2010-01-01','2021-12-31')):
    base = xarr.sel(time=slice(*baseline)) if baseline else xarr
    clim = base.groupby('time.month').mean('time')
    ano  = xarr.groupby('time.month') - clim
    return ano, clim

def anomd(xarr, baseline=('2010-01-01','2021-12-31'), deg=1):
    x_det, trend = detrend_dim(xarr, dim='time', deg=deg, baseline=baseline, return_trend=True)
    base_det = x_det.sel(time=slice(*baseline)) if baseline else x_det
    clim_d = base_det.groupby('time.month').mean('time')
    ano_d  = x_det.groupby('time.month') - clim_d
    return ano_d, clim_d, trend

  
##### Study Area #####
# Define bounds for the Volta River Estuary Area
lat_min, lat_max = 5.73, 5.83
lon_min, lon_max = 0.64, 0.75

# Full map bounds
full_lat_min, full_lat_max = 3, 9
full_lon_min, full_lon_max = -3, 3

# Specific points
lon_estuary, lat_estuary = 0.667, 5.77 # these coordinates are chosen at the estuary, near Ada Foah
lon_lake, lat_lake = 0.087, 6.267 # these are the coordinates of the Volta River just downstream of Volta Lake, close to Akosombo.

  # Create figure and axis with PlateCarree projection
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 12), subplot_kw={'projection': ccrs.PlateCarree()})
# First panel: Broad focus Area
ax[0].set_extent([full_lon_min, full_lon_max, full_lat_min, full_lat_max])
ax[0].coastlines(resolution='10m')  # Dettagli costieri
ax[0].add_feature(cfeature.BORDERS, linestyle='-', linewidth=1.5)
ax[0].add_feature(cfeature.LAND, edgecolor='black')
ax[0].add_feature(cfeature.RIVERS)
ax[0].add_feature(cfeature.LAKES, alpha=0.5)
ax[0].add_feature(cfeature.OCEAN)
gl0 = ax[0].gridlines(draw_labels=True)
gl0.top_labels = False
gl0.right_labels = False
gl0.xlabel_style = {'fontsize': 18}
gl0.ylabel_style = {'fontsize': 18}
gl0.xformatter = LONGITUDE_FORMATTER
gl0.yformatter = LATITUDE_FORMATTER
ax[0].set_title('Study area - the Keta Basin', fontsize=30)
  # Add rectangle for Keta Estuary subset
  # Add patch (box)
rect = Rectangle((lon_min, lat_min), lon_max - lon_min, lat_max - lat_min,
                 linewidth=2, edgecolor='red', facecolor='none', transform=ccrs.PlateCarree())
ax[0].add_patch(rect)
ax[0].text(lon_min, lat_max - 0.3, 'Volta Estuary', color='red', fontsize=20, transform=ccrs.PlateCarree())
  # Second panel: detail over the Volta River Estuary 
ax[1].set_extent([0, 1.5, 5, 6.5])
ax[1].coastlines(resolution='10m')  # Dettagli costieri
ax[1].add_feature(cfeature.BORDERS, linestyle='-', linewidth=1.5)
ax[1].add_feature(cfeature.LAND, edgecolor='black')
ax[1].add_feature(cfeature.RIVERS)
ax[1].add_feature(cfeature.LAKES, alpha=0.5)
ax[1].add_feature(cfeature.OCEAN)
gl1 = ax[1].gridlines(draw_labels=True)
gl1.top_labels = False
gl1.right_labels = False
gl1.xlabel_style = {'fontsize': 18}
gl1.ylabel_style = {'fontsize': 18}
gl1.xformatter = LONGITUDE_FORMATTER
gl1.yformatter = LATITUDE_FORMATTER
ax[1].set_title('Study area - Volta River Estuary Area', fontsize=30)
  # Add patch (box)
rect2 = Rectangle((lon_min, lat_min), lon_max - lon_min, lat_max - lat_min,
                  linewidth=2, edgecolor='red', facecolor='none', transform=ccrs.PlateCarree())
ax[1].add_patch(rect2)
ax[1].text(lon_min, lat_max + 0.05, 'Volta Estuary', color='red',fontsize=20, transform=ccrs.PlateCarree())
plt.tight_layout()
plt.show()

## For further analysis, it will be take into account a single point, located at the Volta River Mouth (5.77°N e 0.667°E), 
## and an aditional point further upstream, at Volta Lake (6.50°N, 0.117°E).

  # Base map
plt.figure(figsize=(6,5))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([0, 1.5, 5, 6.7])
ax.coastlines(resolution='10m')
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=0.5)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.OCEAN)
gl = ax.gridlines(draw_labels=True)
gl.right_labels = False
gl.top_labels = False
  # Add red points 
plt.plot(lon_estuary, lat_estuary, marker='o', color='red', markersize=5)
ax.text(lon_estuary -0.15, lat_estuary - 0.1, 'Volta Estuary reference point', color='red',
        fontsize=10, transform=ccrs.PlateCarree())
plt.plot(lon_lake, lat_lake, marker='o', color='red', markersize=5)
ax.text(lon_lake + 0.03, lat_lake - 0.1, 'Volta Lake reference point', color='red',
        fontsize=10, transform=ccrs.PlateCarree())
plt.title('Volta River Estuary')
plt.show()


##### Load and preprocess data #####
### GloFAS data ###
# note: this dataset was downloaded from the CEMS Early Warning Data store 
# (https://ewds.climate.copernicus.eu/datasets/cems-glofas-historical?tab=overview), 
# selecting the years between 2010-2021 singularly.
# in the following these separated files are concatenated and sorted.
##
# ----------------------------------------
# Message from Thomas: 
#  Alessandra, the script needs to be reproducible e.g. someone without knowledge needs to be able to 
#  get all the data without leaving the script here. 
#  It can be a notebook or a python script, this is not important, but everything has to be 
#  consistently reachable and reproducible at the same spot. 
#  https://confluence.ecmwf.int/pages/viewpage.action?pageId=428248687
 
os.makedirs("keta_data",exist_ok=True)
for year in [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]:
  cds_request_keta(year)
files_glofas = sorted(glob.glob("*.nc"))
  # Open and concatenate
glofas_ds = [xr.open_dataset(f) for f in files_glofas]
glofas_keta = xr.concat(glofas_ds, dim="time")
glofas_keta

# Checking on and sorting the 'time' variable
  # Get a DatetimeIndex for convenience
t = getattr(glofas_keta.indexes, 'time', pd.DatetimeIndex(glofas_keta['time'].values))
print("Count:", t.size)
print("First :", t[0])
print("Last  :", t[-1])
  # Sortedness / monotonicity
print("Monotonic increasing:", t.is_monotonic_increasing)
print("Has duplicates      :", t.has_duplicates)
  # Peek at the edges
print("Head:", t[:5].tolist())
print("Tail:", t[-5:].tolist())
  # Frequency / regularity
print("Inferred frequency  :", t.inferred_freq)  # None => irregular
  # Show where ordering is broken (if any)
bad_order_idx = np.where(t[1:] < t[:-1])[0]
print("Out-of-order indices:", bad_order_idx[:10], "(showing up to 10)")
  # Gap summary (how many times each delta occurs)
diffs = pd.Series(t[1:] - t[:-1])
print("Most common gaps:\n", diffs.value_counts().head(5))
print("Unique gaps:", pd.unique(diffs))

  # Show the exact out-of-order transitions (with context)
t = glofas_keta.get_index('time')
bad_idx = np.where(t[1:] < t[:-1])[0]  # indices where next < prev
print("Out-of-order count:", bad_idx.size)
  # Show a little neighborhood around each break
for i in bad_idx:
    lo = max(0, i-2)
    hi = min(len(t), i+3)
    print(f"\nBreak at i={i} (t[i] -> t[i+1]):")
    print(pd.Series(t[lo:hi]).to_string())

  # Sort by time and verify
glofas_sorted = glofas_keta.sortby('time')
ti = glofas_sorted.get_index('time')
print("Monotonic after sort:", ti.is_monotonic_increasing)
print("Start/End after sort:", ti[0], ti[-1])
print("Inferred freq after sort:", ti.inferred_freq)  # still None if gaps remain

  # Identify and list missing dates (daily grid)
full = pd.date_range(t.min(), t.max(), freq='D')
have = glofas_sorted.time.to_index()
missing = full.difference(have)
print("Missing days:", len(missing))
print("First 20 missing:\n", pd.Series(missing[:20]))
  # Summarize missing by year
miss_df = pd.DataFrame({"date": missing})
miss_df["year"] = miss_df["date"].dt.year
print(miss_df["year"].value_counts().sort_index())

  # Extract raw (daily) values to the point closest to the two points
rd_estuary = glofas_sorted['dis24'].sel(latitude = lat_estuary, longitude = lon_estuary, method='nearest')
rd_lake = glofas_sorted['dis24'].sel(latitude = lat_lake, longitude = lon_lake, method='nearest')
  # confirm where we actually landed
sel_estuary_lat = float(rd_estuary.latitude.values)
sel_estuary_lon = float(rd_estuary.longitude.values)
sel_lake_lat  = float(rd_lake.latitude.values)
sel_lake_lon  = float(rd_lake.longitude.values)
print("Estuary grid cell:",  sel_estuary_lat, sel_estuary_lon)
print("Lake grid cell:",   sel_lake_lat,  sel_lake_lon)


### Water level data ###
# 

  # Import data from working directory
data_dir = r"C:/Users/aless/Desktop/dati_tesi/globalDailyMaxWaterLevel/VER2024-05-03"
file_jrc = sorted(glob.glob(os.path.join(data_dir, "*.nc")))
  # Checking for the presence and validity of files in the working directory
valid_files = []
invalid_files = []
for filepath in file_jrc:
    if os.path.isfile(filepath) and filepath.endswith(".nc"):
        try:
            ds = Dataset(filepath)
            ds.close()
            valid_files.append(filepath)
        except:
            invalid_files.append(filepath)
    else:
        invalid_files.append(filepath)
print(f"Valid NetCDF files: {len(valid_files)}")
print(f"Unreadable NetCDF files: {len(invalid_files)}")
if invalid_files:
    print("Examples of invalid files:")
    for f in invalid_files[:5]:
        print(" -", f)

# Explore data structure
sample_ds = Dataset(valid_files[0])
print("DATASET INFO:")
print(sample_ds)
print("VARIABLES:")
print(sample_ds.variables.keys())
water_var = sample_ds.variables['waterLevelreanalysis'][:]  
print(f"WATER LEVEL shape: {water_var.shape}")
print(f"TIME VARIABLE:", sample_ds['time_1959_2021'])
sample_ds.close()
sample_xr = xr.open_dataset(valid_files[0])
print(sample_xr)
print(sample_xr.coords)
print(sample_xr.dims)
print(sample_xr['waterLevelreanalysis'].attrs)

# Open and concatenate datasets
filtered = []
for f in file_jrc:
    ds = xr.open_dataset(f)
    mask = ((ds.longitudeSAT >= full_lon_min) & (ds.longitudeSAT <= full_lon_max) &
            (ds.latitudeSAT  >= full_lat_min) & (ds.latitudeSAT  <= full_lat_max))
    ds = ds.sel(pointsSAT=mask)
    if ds.sizes.get("pointsSAT", 0) > 0:
        filtered.append(ds)
if not filtered:
    raise ValueError("No datasets found within the target region. Check coordinate ranges.")

keta_wl = xr.concat(filtered, dim="pointsSAT", combine_attrs="override")
print("Longitude range:", float(keta_wl.longitudeSAT.min()), "to", float(keta_wl.longitudeSAT.max()))
print("Latitude range:",  float(keta_wl.latitudeSAT.min()),  "to", float(keta_wl.latitudeSAT.max()))
keta_wl

# Convert to meters (x 1e-4)
  # 1) convert to meters in place (respect fill if present)
v = keta_wl["waterLevelreanalysis"]
fill = v.encoding.get("_FillValue", v.attrs.get("_FillValue"))
keta_wl["waterLevelreanalysis"] = (v.where(v != fill) if fill is not None else v) * 1e-4
keta_wl["waterLevelreanalysis"].attrs.update({
    **{k: v.attrs.get(k) for k in v.attrs if k != "units"},
    "units": "m",
    "long_name": "daily maximum offshore water level (meters)",
    "note": "converted from 1e-4 m by multiplying by 1e-4"})

  # 2) standardize time coord only if needed
time_name = next((c for c in ["time", "time_1959_2021", "valid_time"] if c in keta_wl.coords), None)
if time_name and time_name != "time":
    keta_wl = keta_wl.rename({time_name: "time"})

# Selection of the ofshore point nearest to the estuary
dist2 = (keta_wl.latitudeSAT - lat_estuary)**2 + (keta_wl.longitudeSAT - lon_estuary)**2
ip = int(dist2.argmin(dim="pointsSAT").values)
  # Filter the period 2010-2021
sel_keta_wl = keta_wl.sel(time=slice("2010-01-01", "2021-12-31"))
  # Nearest open-ocean point to the river mouth
wl_estuary = sel_keta_wl['waterLevelreanalysis'].isel(pointsSAT=ip)
wl_estuary = wl_estuary.sortby("time")
