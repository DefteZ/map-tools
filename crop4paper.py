
#!/usr/bin/python
#import maptools.minimap
import sys
import os
import argparse

import maptools.minimap

def paperCoord(string):
	coord = string.split("x")
        
        
	if  coord[0].isdigit() and coord[1].isdigit():
		return [int(coord[0]),int(coord[1])]
	else:
		msg = "%r is not a perfect coordinate. Use like this 1000x1000" % string
		raise argparse.ArgumentTypeError(msg)



if __name__ == "__main__":
	argv = sys.argv

	
	parser = argparse.ArgumentParser(description='Create some map for print on standart paper format (a4,a3) and add coordinate plank for it')
	#parser.add_argument('MAP_PATH', required=True)
	parser.add_argument("MAP_PATH", nargs=1, type=argparse.FileType('r'), help="path to map")
	parser.add_argument('--format', choices=["a3","a4","No"], nargs=1,default="No",
							help='paper format')
	parser.add_argument('--coord', type=paperCoord,
                   help='coordinate of left top corner of paper on map. If is not set, map all cropping.')

	args = parser.parse_args()
        format = maptools.minimap.PaperFormat.NO
        #print args.format
        if  "a3" in args.format:
                format =  maptools.minimap.PaperFormat.A3
        if  "a4" in args.format:
                format  = maptools.minimap.PaperFormat.A4
                
	#print args.coord
        if not args.coord is None and format != maptools.minimap.PaperFormat.NO:
        
                maptools.minimap.splitOne(maptools.map_operator.Map((os.path.abspath(args.MAP_PATH[0].name))),args.coord,format=format)
        if format == maptools.minimap.PaperFormat.NO:
                maptools.minimap.splitOne(maptools.map_operator.Map((os.path.abspath(args.MAP_PATH[0].name))),(0,0),format=format)
        if args.coord is None and format != maptools.minimap.PaperFormat.NO:
                maptools.minimap.splitA4All(os.path.abspath(args.MAP_PATH[0].name),format=format)
	
