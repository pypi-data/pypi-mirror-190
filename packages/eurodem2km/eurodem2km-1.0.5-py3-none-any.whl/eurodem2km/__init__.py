# __init__.py

from importlib import resources
from pathlib import Path
import tempfile
from zipfile import ZipFile
try:
    import rasterio
except ModuleNotFoundError:
    import rasterio as rasterio

# Version of the realpython-reader package
__version__ = "1.0.5"

__dem_name__ = "DEM_Europe_2km"

# Read DEM
DEM = None
_dem = resources.path('eurodem2km.dems','dem.grd')
_demZip = resources.path('eurodem2km.dems',__dem_name__+'.zip')
#fp = r"/mnt/d/Code/data-monitor-dem-api/src/dem/dem.grd"
#DEM = rasterio.open(_dem)
#print(f'Using DEM with following "profile":\n{DEM.profile}')

tmpFolder = tempfile.gettempdir()

with ZipFile(_demZip, 'r') as zObject:
    zObject.extract(__dem_name__+'.grd', path=tmpFolder)
    tmpDem = Path(tmpFolder,__dem_name__+'.grd')
    DEM = rasterio.open(tmpDem)