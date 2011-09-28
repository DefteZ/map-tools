from distutils.core import setup

setup(

	name="maptools",
	version ="0.0.3",
        author="Privezentsev Konstantin",
	author_email = "privezentsev@gmail.com",
        
	packages = ["maptools"],
	
	data_files=[('ttf', ['maptools/data/arial.ttf'])],
	scripts = ["addminimap","splitmap","crop4paper.py","topomerge.py","topomerge-win.py"]    	
    
)

