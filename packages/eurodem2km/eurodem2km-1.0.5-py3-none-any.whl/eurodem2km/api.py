import rasterio
from eurodem2km import DEM

class DemAPI():
    
    def getAltitude(lat: float, lon: float) -> float:
        '''Returns the float64 valeue of th altitude in DEM or raises ValueError on error/missing data'''
        band = 1
        bbox = DEM.bounds
        if (lat <= bbox.top and lat >= bbox.bottom and lon >= bbox.left and lon <= bbox.right):
            samples = rasterio.sample.sample_gen(DEM, [[lon, lat]], band, False)
            try:
                for altitude in samples:
                    return altitude[0]
            except:
                err = 'Impossibile determinare l\'altitudine alla coordinata richiesta.'
                print(err)
                raise ValueError(f)
        else:
            err = f'Coordinata fuori dai limitidel DEM:\n{DEM.bounds}'
            print(err)
            raise ValueError(err)