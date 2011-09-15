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

class GeoExifCollector():
	def __init__(self,dirpath):
		#if not os.path.exists("gps_file"):
		#	os.mkdir("gps_file")
		self.points={}
		#os.listdir(os.curdir)
		isJPG = lambda x: re.search(".*\.(JPG|jpg|jpeg|JPEG)",str(x)) != None
		images = filter(isJPG,  os.listdir(dirpath))

		for f in images:
			
			exif_data = self._get_exif_data(Image.open(dirpath + "/" + f))
		
			point =  self._get_lat_lon(exif_data)
			if not None in point:
				self.points[dirpath + "/" + f]=point
			
				
	def _get_exif_data(self,image):
		"""Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
		exif_data = {}
		if image.format !="JPEG":
			return exif_data
		info = image._getexif()
		if info:
			for tag, value in info.items():
				decoded = TAGS.get(tag, tag)
				
				if decoded == "GPSInfo":
					gps_data = {}					
					for t in value:
						sub_decoded = GPSTAGS.get(t, t)
						gps_data[sub_decoded] = value[t]
					#print dir(gps_data.)
					#if gps_data.has_key(None) == False:
					exif_data[decoded] = gps_data
			else:
				exif_data[decoded] = value

		return exif_data

	def _get_if_exist(self,data, key):
		if key in data:
			return data[key]

		return None

	def _convert_to_degress(self,value):
		"""Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
		#print value
		d0 = value[0][0]
		d1 = value[0][1]
		d = float(d0) / float(d1)

		m0 = value[1][0]
		m1 = value[1][1]
		m = float(m0) / float(m1)

		s0 = value[2][0]
		s1 = value[2][1]
		s = float(s0) / float(s1)

		return d + (m / 60.0) + (s / 3600.0)

	def _get_lat_lon(self,exif_data):
		"""Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
		lat = None
		lon = None

		if "GPSInfo" in exif_data:		
			gps_info = exif_data["GPSInfo"]

			gps_latitude = self._get_if_exist(gps_info, "GPSLatitude")
			gps_latitude_ref = self._get_if_exist(gps_info, 'GPSLatitudeRef')
			gps_longitude = self._get_if_exist(gps_info, 'GPSLongitude')
			gps_longitude_ref = self._get_if_exist(gps_info, 'GPSLongitudeRef')

			if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
				lat = self._convert_to_degress(gps_latitude)
				if gps_latitude_ref != "N":					 
					lat = 0 - lat

				lon = self._convert_to_degress(gps_longitude)
				if gps_longitude_ref != "E":
					lon = 0 - lon

		return (lon,lat)


	def getImagesFiles(self):

		return self.points.keys()
	
	def getWGS84Coord(self,f):
		if (self.points[f] != None):
			return self.points[f]
		else:
			return ()

def _uint(i):
  i = int(i)
  if i > sys.maxint and i <= 2 * sys.maxint + 1:
    return int((i & sys.maxint) - sys.maxint - 1)
  else:
    return i
def minimap(raw,map_img,coord):
	
	# crop_name="crop.gif"
	# rect_name="rect.png"
	# minimap_name="mini_map.jpg"
	im_raw = Image.open(raw)
	
	im_map = Image.open(map_img)

	box = (int(coord[0]-100),int(coord[1]-100),int(coord[0]+100),int(coord[1]+100))	
	im_crop = im_map.crop(box)
	draw = ImageDraw.Draw(im_crop)
	
	draw.rectangle([(90,90),(110,110)],fill=_uint(0xff0000ff))
	del draw
	
	im_raw.paste(im_crop,(im_raw.size[0]-200,im_raw.size[1]-200))


	return_name=str(raw).split("/")[-1]+"-mod" + ".jpg" 
	print return_name
	im_raw.save(return_name,quality=90)


	return return_name

def crop_path(image,coordlist,save_path):


	im = Image.open(image)
	draw = ImageDraw.Draw(im)
	draw.line(coordlist, fill=128,width=6)
	xmin = int(min(coordlist,key=lambda k:k[0])[0])-50
	ymin = int(min(coordlist,key=lambda k:k[1])[1])-50
	xmax = int(max(coordlist,key=lambda k:k[0])[0])+50
	ymax = int(max(coordlist,key=lambda k:k[1])[1])+50
	print xmin,ymin,xmax,ymax,save_path
	im.crop((xmin,ymin,xmax,ymax)).save(save_path)


	

def _crop(image, coord, save_path):
	im_raw = Image.open(image)
	box = (coord[0],coord[1],coord[2],coord[3])
	im_crop = im_raw.crop(box)
	im_crop.save(save_path)