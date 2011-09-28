#!/bin/python
import gdal
import subprocess
import argparse
import maptools
import os
import glob
import sys
import re
import maptools.map_operator
import math
import glob
def isdir(string):
	if not os.path.isdir(os.path.dirname(string)):
                
		msg = "%r is not direcotory" % string
		raise argparse.ArgumentTypeError(msg)
	else:
		return string
                

if __name__=="__main__":
        argv=sys.argv
        parser=argparse.ArgumentParser(description="Merge some Soviet topographic map")
        parser.add_argument("TOPO_SHP",  type=argparse.FileType("r"), nargs=1,help="Path to shape file")
        parser.add_argument("MAP_DIR",type=isdir, nargs='*', help="Path to maps")
        
        args = parser.parse_args()

        dirPath = os.path.dirname(args.MAP_DIR[0])
        os.chdir(dirPath)
        translatePath=os.path.join(dirPath,"translate.tif")
        translateModPath=os.path.join(dirPath,"translate-mod.tif")
        vrtPath = os.path.join(dirPath,"o.vrt")
        resultPath=os.path.join(dirPath,"o.tif")

        
        print "Translate and warp map:"
        for f in args.MAP_DIR:
                
#                             
                subprocess.call(["gdal_translate","-of","GTiff","-a_srs","EPSG:4284","-expand","rgba","-a_nodata","\"0 0 0 0\"",f,translatePath],stdout=open("/dev/null", "w"))
                
                subprocess.call(["gdalwarp","-r","near","-overwrite",translatePath, translateModPath],stdout=open("/dev/null", "w"))


                m = maptools.map_operator.Map(translateModPath)
                box = m.getCoordinateBox()

                avlat = abs(box[0][0]+box[1][0])/2
                avlon = abs(box[0][1]+box[1][1])/2
                                
                zone = chr(97+int(math.floor(float(avlon)/4)))
                zoneNum = ord(zone)-97
                km10 = int((180+avlat)/6+1 )
                km1 = int(12*((avlat+180)-km10*6)/6)+12*int(12-12*(avlon-zoneNum*4)/4+1)
                print f,"Nomenclature:",zone+str(km10)+"-"+str(km1)
                select = "zone='%s' and i10km=%s and i1km=%s" % (str(zone),str(km10),str(km1))

                subprocess.call(["gdalwarp","-overwrite","-cutline",str(args.TOPO_SHP[0].name),"-cwhere",select,"-crop_to_cutline",translateModPath, os.path.join(dirPath,os.path.splitext(os.path.basename(f))[0]+"-crop.tif")],stdout=open("/dev/null","w"))
                
        print "Merge map..."
        subprocess.call(["gdalbuildvrt","-srcnodata","\"0 0 0 0\"", vrtPath]+glob.glob('*-crop.tif'),stdout=open("/dev/null","w"))
        
        subprocess.call(["gdal_translate","-co", "COMPRESS=LZW",vrtPath,resultPath],stdout=open("/dev/null","w"))
        print "Write merged map to",resultPath


#        maptools.map_operator.Map()
    
