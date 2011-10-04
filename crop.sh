#!/bin/bash
src=$1
topo1km=$2



cd $1
echo "translate"
#echo `ls | grep \\.$1`
for i in `ls *gif`
do
    echo $i
    dst=`expr "$i" : '\([a-zA-Z0-9\-]*\)'`-crop.tif
    savei=$i
    i=${i##*/}
   
    i=${i#100k--} 
   
    i=${i%%\.gif}
   
    zone=`expr "$i" : '\([a-z]*\)'`
    i=${i#[a-z]*}
   
    km10=`expr "$i" : '\([0-9]*\)'`
    km1=${i:3:3}
    
 
    echo "translate" 
    gdal_translate -of GTiff -a_srs EPSG:4284 -expand rgba -a_nodata "0 0 0 0"  $savei translate.tif
    echo "warp"

    
    gdalwarp -r near -overwrite -cutline $topo1km -cwhere "zone='$zone' and i10km=$km10 and i1km=$km1" -crop_to_cutline translate.tif $1/$dst
    rm translate.tif
    echo "Complete"  $dst
    echo 
    echo 
done

gdalbuildvrt -srcnodata "0 0 0 0" o.vrt *-crop.tif 
gdal_translate -co COMPRESS=LZW  o.vrt o.tif
echo "Map is create - o.tif"
rm o.vrt

#gdal_translate -of GTiff -expand rgba -a_nodata "0 0 0 0"  $1 translate.tif
#echo "warp"
#gdalwarp -overwrite -cutline topo1km_rus.shp -cwhere "zone='$zone' and i10km=$km10 and i1km=$km1" -crop_to_cutline translate.tif $dst




