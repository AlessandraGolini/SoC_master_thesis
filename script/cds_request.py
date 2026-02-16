import cdsapi

def cds_request_keta(year):
    dataset = "cems-glofas-historical"
    request = {
        "system_version": "version_4_0",
        "hydrological_model": "lisflood",
        "product_type": "consolidated",
        "variable": "river_discharge_in_the_last_24_hours",
        "hyear": f"{year}",
        "hmonth": [f"{m:02d}" for m in range(1, 13)],
        "hday": [f"{d:02d}" for d in range(1, 32)],
        "data_format": "netcdf",
        "area": [6.75, 0, 5, 1.5],
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download()
