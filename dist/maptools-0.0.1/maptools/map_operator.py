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
"""
Module for operation with GeoTiff map
"""
class Map():

	def __init__(self, path):
		self.path = path
		ds = gdal.Open(path)

		new_cs=osr.SpatialReference()
		new_cs.ImportFromWkt(ds.GetProjectionRef())
		
		# create the new coordinate system
		wgs84_wkt = """
		GEOGCS["WGS 84",
		DATUM["WGS_1984",
			SPHEROID["WGS 84",6378137,298.257223563,
				AUTHORITY["EPSG","7030"]],
			AUTHORITY["EPSG","6326"]],
		PRIMEM["Greenwich",0,
			AUTHORITY["EPSG","8901"]],
		UNIT["degree",0.01745329251994328,
			AUTHORITY["EPSG","9122"]],
		AUTHORITY["EPSG","4326"]]"""

		old_cs = osr.SpatialReference()
		old_cs.ImportFromWkt(wgs84_wkt)

		# create a transform object to convert between coordinate systems
		self.transform = osr.CoordinateTransformation(old_cs,new_cs) 
		self.width = ds.RasterXSize
		self.height = ds.RasterYSize
		
		
		gt = ds.GetGeoTransform()
		
		self.minx = gt[0]
		self.miny = gt[3] + self.width*gt[4] + self.height*gt[5] 
		self.maxx = gt[0] + self.width*gt[1] + self.height*gt[2]
		self.maxy = gt[3] 

	def getPath(self):
		return self.path
	def getPixelCoord(self, lan, lat):
		#print self.transform
		
		
		tr_coord  = self.transform.TransformPoint(lan , lat)
		# self.minx,self.miny, self.maxx, self.maxy
		return  ((float)(tr_coord[0]-self.minx)/(self.maxx-self.minx)*self.width,\
		 (float)(-tr_coord[1]+self.maxy)/(self.maxy-self.miny)*self.height)