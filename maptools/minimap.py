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
					image_operator.crop_path(map_img, ptcoord_list, os.curdir + "/" + split_dir + "/" + \
					track.name + "_" + str(cur_day.time.month) + "_" + str(cur_day.time.day) + ".jpg")
					cur_day = pt
					ptcoord_list = []
					ptcoord_list.append(map_info.getPixelCoord(pt.lon,pt.lat))
				else:
					ptcoord_list.append(map_info.getPixelCoord(pt.lon,pt.lat))

def minimap_create(map_img,dir_path):
	"""Create minimap on the corner of photo"""
	mod = "mod/"
	tiff = map_operator.Map(map_img)
	
	geo = image_operator.GeoExifCollector(dir_path)
	if not os.path.exists(mod):
		os.mkdir(mod)
	for f in geo.getImagesFiles():
		
		wgsc = geo.getWGS84Coord(f)
		
		path = image_operator.minimap(f, tiff.getPath(), tiff.getPixelCoord(wgsc[0],wgsc[1]))
		full_path = dir_path + mod + path
		


		if os.path.exists(full_path):
			os.remove(full_path)
		shutil.move(path, dir_path + mod)

			
	

 	