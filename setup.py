from distutils.core import setup
import py2exe

setup(
    console = ["addminimap"],
    options = {"py2exe" : {
        
        'includes': 'gdal'
    }}
)