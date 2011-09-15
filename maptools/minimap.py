#!/usr/bin/python

import os
import shutil
import gdal
import osr
import re
import sys
import Image, ImageDraw
from PIL.ExifTags import TAGS, GPSTAGS
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
	m = map_operator.Map(map_image)
	box = m.getCoordinateBox()
	
	pixkil = m.getPixelForKilometer()
	
	a4width = pixkil*21
	a4height = pixkil*29

	by_width = int(m.width/a4width)+1
	by_height = int(m.height/a4height)+1
	print box
	init_coord = m.getPixelCoord(int(box[0][0]),int(box[1][1]))

	print init_coord


	for i in range(by_width):
		xcoord = i*a4width #+ init_coord[1]
		for j in range(by_height):
			ycoord = j*a4height #+ init_coord[0]	
			#print (xcoord,ycoord,a4width,a4height)
			m.getWGS84()
			savepath = os.path.join(os.path.dirname(map_image),str(j) + "_" +str(i) + ".jpg")
			image_operator._crop(map_image, (xcoord,ycoord,xcoord + a4width,ycoord+ a4height),savepath)
			image_operator.drawXCoordinatePlank(savepath,m.getPixelForMinuteLat())
			image_operator.drawYCoordinatePlank(savepath, int(m.getPixelForKilometer()*1.8520))
		
def splitA4One(map_image, coord):
	pass	
 	
