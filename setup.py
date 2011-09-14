from distutils.core import setup
import py2exe

setup(
    name="maptools",
    version ="0.0.1",
    console=[{"script":"addminimap"}],
       
    author_email="privezentsev@gmail.com",
    packages=["maptools"],
    scripts=["addminimap","splitmap"]    
)