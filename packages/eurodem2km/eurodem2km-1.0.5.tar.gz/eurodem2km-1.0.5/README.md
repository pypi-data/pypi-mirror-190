## eurodem2km

Import the DemAPI class as follows:

`from eurodem2km.api import DemAPI`

and use its method "getAltitude(lat: float, lon: float)" to get the location altitude'  

`altitude = DemAPI.getAltitude(44.159,10.386)`

<br/>

### DEVELOPMENT

Clone the code and install as an editable install using:  
`python -m pip install -e .`

<br/>

### PACKAGING
Follow this fine tutorial:
https://realpython.com/pypi-publish-python-package/

Install in virtual environment the build and twine tools:  
``python -m pip install build twine keyrings.alt``

Build:  
``python -m build``

Check output:  
``twine check dist/*``

Upload to PyPI:  
``twine upload dist/*``