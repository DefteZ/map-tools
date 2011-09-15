from distutils.core import setup

setup(
<<<<<<< HEAD
	name="maptools",
	version ="0.0.1",
	author_email = "privezentsev@gmail.com",
	packages = ["maptools"],
	scripts = ["addminimap","splitmap"]    	
    
)
=======
    name="maptools",
    version ="0.0.1",
    console=[{"script":"addminimap"}],
       
    author_email="privezentsev@gmail.com",
    packages=["maptools"],
    scripts=["addminimap","splitmap"]    
)
>>>>>>> ba4f0125dfc23f352354de80e84506072e2d007d
