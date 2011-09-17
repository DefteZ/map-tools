from distutils.core import setup

setup(

	name="maptools",
	version ="0.0.2",
	author_email = "privezentsev@gmail.com",
	packages = ["maptools"],
	
	data_files=[('ttf', ['maptools/data/arial.ttf'])],
	scripts = ["addminimap","splitmap","crop4paper.py"]    	
    
)

