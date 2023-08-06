import unittest
from eurodem2km.api import DemAPI

class Test_DemAPI(unittest.TestCase):
    
    def test_getAltitude(self):
        altitude = DemAPI.getAltitude(44.159,10.386)
        print(f'{altitude:.2f}')
        assert altitude == 597.00
    
    def test_getAltitudeOutOfBounds(self):        
        self.assertRaises(ValueError, DemAPI.getAltitude, 4.159, 0.386)
    