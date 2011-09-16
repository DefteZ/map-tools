#!/usr/bin/python

import os
import shutil
import gdal
import osr
import re
import sys
import Image, ImageDraw, ImageFont
from   PIL.ExifTags import TAGS, GPSTAGS
import pygpx as GPX
import datetime
import image_operator
import map_operator

import math

def split_by_gpx(map_img,gpx_file,utc_zone):
	"""Create crop map by day"""
	split_dir = "split"
	gpx = GPX.GPX(open(gpx_file))
	map_info = map_operator.Map(map_img)
	if not os.path.exists(split_dir):
		os.mkdir(split_dir)
	for track in gpx.tracks:
		for trkseg in track.trksegs:
		
			cur_day=''
			ptcoord_list = []
			if len(trkseg.trkpts)>0:
				cur_day = trkseg.trkpts[0]
				ptcoord_list.append(map_info.getPixelCoord(cur_day.lon,cur_day.lat))
				cur_day.time = cur_day.time + datetime.timedelta(hours=int(utc_zone))
			for pt in trkseg.trkpts:
				pt.time = pt.time + datetime.timedelta(hours=int(utc_zone))

				if (pt.time.day - cur_day.time.day) != 0:
					image_operator.crop_path(map_img, \
											 ptcoord_list,
								             os.path.join(os.curdir, split_dir, \
														  track.name + "_" + str(cur_day.time.month) + "_" + str(cur_day.time.day) + ".jpg"))
					cur_day = pt
					ptcoord_list = []
					ptcoord_list.append(map_info.getPixelCoord(pt.lon,pt.lat))
				else:
					ptcoord_list.append(map_info.getPixelCoord(pt.lon,pt.lat))

def minimap_create(map_img,dir_path):
	"""Create minimap on the corner of photo"""
	mod = "mod"
	tiff = map_operator.Map(map_img)
	
	geo = image_operator.GeoExifCollector(dir_path)
	if not os.path.exists(os.path.join(dir_path, mod)):
		os.mkdir(os.path.join(dir_path, mod))
	for f in geo.getImagesFiles():
		
		wgsc = geo.getWGS84Coord(f)
		
		minimap_path = image_operator.minimap(f, tiff.getPath(), tiff.getPixelCoord(wgsc[0],wgsc[1]))
		target_path = os.path.join(dir_path, mod, os.path.basename(minimap_path))
		


		if os.path.exists(target_path):
			os.remove(target_path)
		shutil.move(minimap_path, os.path.join(dir_path,mod))




def splitA4All(map_image):
	print map_image
	m = map_operator.Map(map_image)
	box = m.getCoordinateBox()
	
	pixkil = m.getPixelForKilometer()
	
	a4width = pixkil*20
	a4height = pixkil*28

	by_width = int(m.width/a4width)+1
	by_height = int(m.height/a4height)+1

	#vBinit_coord = m.getPixelCoord(int(box[0][0]),int(box[1][1]))
	offset = 26
	#print init_coord

	#by_width=1
	#by_height=1
	for i in range(by_width):
		xcoord = i*a4width #+ init_coord[1]
		for j in range(by_height):
			ycoord = j*a4height #+ init_coord[0]	
			
			wgsLeft = m.getWGS84Coord(xcoord,ycoord)
			wgsRight = m.getWGS84Coord(xcoord+a4width,ycoord)
			print wgsLeft,wgsRight
			wgsDeltaX = wgsLeft[1]*60-int(wgsLeft[1]*60)
			wgsDeltaY = wgsLeft[0]*60-int(wgsLeft[0]*60)
			print wgsDeltaX*m.getPixelForMinuteLat()
			whKoef = m.getPixelForMinuteLat()/m.getPixelForMinuteLon()
		
			rotateAngle = math.atan((-wgsLeft[1]+wgsRight[1])/((-wgsLeft[0]+wgsRight[0])*whKoef))
			#print rotateAngle
			
			savepath = os.path.join(os.path.dirname(map_image),str(j) + "_" +str(i) + ".jpg")
			

			newIm = Image.new('RGBA',(int(a4width+52),int(a4height+52)))
			image_operator._crop(map_image, (int(xcoord),int(ycoord),int(xcoord + a4width),int(ycoord+ a4height)),savepath)
			im=Image.open(savepath)
			im=im.rotate((180/math.pi)*rotateAngle,expand=True)
			newIm.paste(im,(offset,offset))
			newIm.save(savepath)
			print a4width/2 - math.cos(rotateAngle)*a4width/2

			image_operator.drawXCoordinatePlank(savepath,m.getPixelForMinuteLat(),\
				init_coord=offset+wgsDeltaX*m.getPixelForMinuteLat()+ (a4width/2 - math.cos(rotateAngle)*math.sqrt((a4width**2)/4+(a4height**2)/4)))
			
			image_operator.drawYCoordinatePlank(savepath, int(m.getPixelForKilometer()*1.8520),\
				init_coord=offset+wgsDeltaY*m.getPixelForMinuteLon()-math.tan(rotateAngle)*a4width/2)
			

		
def splitA4One(map_image, coord):

	pass
print "dsadsa"
splitA4All("/home/q/kodar-1km.tif")