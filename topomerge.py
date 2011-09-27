#!/bin/python
import gdal
import subprocess
import argparse
import maptools
import os
import glob
import sys
import re
def isdir(string):
	if not os.path.isdir(os.path.dirname(string)):
                
		msg = "%r is not direcotory" % string
		raise argparse.ArgumentTypeError(msg)
	else:
		return string
                

if __name__=="__main__":
        argv=sys.argv
        parser=argparse.ArgumentParser(description="Merge some Soviet topographic map")

        parser.add_argument("MAP_DIR",type=isdir, nargs='*', help="Path to maps")
        
        parser.add_argument("TOPO_SHP",  type=argparse.FileType("r"), nargs=1,help="Path to shape file")


        args = parser.parse_args()

        dirPath = os.path.dirname(args.MAP_DIR[0])
        print dirPath
        for f in args.MAP_DIR:
                

        
        
#        maptools.map_operator.Map()
    
