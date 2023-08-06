import os
import numpy as np
import s3fs
import wis_s3api as main
import xarray as xr

endpoint_url = main.endpoint_url
access_key = main.access_key
secret_key = main.secret_key
bucket_path = main.bucket_path

fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": endpoint_url}, 
    key=access_key, 
    secret=secret_key
)

start = np.datetime64("2015-01-01T00:00:00.000000000")
end = np.datetime64("2021-12-31T23:00:00.000000000")
box = (115, 38, 136, 54)
variables=[
    'HQobservationTime',
    'HQprecipSource',
    'HQprecipitation',
    'IRkalmanFilterWeight',
    'IRprecipitation',
    'precipitationCal',
    'precipitationUncal',
    'probabilityLiquidPrecipitation',
    'randomError'
]


def open(start_time=start, end_time=end, bbox=box, time_chunks=24):

    chunks = {"time": time_chunks}
    ds = xr.open_dataset(
        "reference://", 
        engine="zarr", 
        chunks=chunks,
        backend_kwargs={
            "consolidated": False,
            "storage_options": {
                "fo": fs.open('s3://' + bucket_path + 'gpm/gpm2022_inc.json'), 
                "remote_protocol": "s3",
                "remote_options": {
                    'client_kwargs': {'endpoint_url': endpoint_url}, 
                    'key': access_key, 
                    'secret': secret_key}
            }
        }      
    )
    
    ds = ds['precipitationCal']
    # ds.to_dataframe().filter(['precipitationCal','precipitationUncal']).to_xarray()
    
    # ds = ds.rename({"longitude": "lon", "latitude": "lat"})
    ds = ds.transpose('time','lon','lat')
    
    if start_time < start:
        start_time = start
    
    if end_time > end:
        end_time = end
    
    times = slice(start_time, end_time)
    ds = ds.sel(time=times)
    
    if bbox[0] < box[0]:
        left = box[0]
    else:
        left = bbox[0]
        
    if bbox[1] < box[1]:
        bottom = box[1]
    else:
        bottom = bbox[1]
    
    if bbox[2] > box[2]:
        right = box[2]
    else:
        right = bbox[2]
    
    if bbox[3] > box[3]:
        top = box[3]
    else:
        top = bbox[3]
    
    longitudes = slice(left - 0.00001, right + 0.00001)
    latitudes = slice(bottom - 0.00001, top + 0.00001)
    
    ds = ds.sortby('lat', ascending=True)
    ds = ds.sel(lon=longitudes, lat=latitudes)
    
    return ds