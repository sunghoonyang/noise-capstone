"""
Written By: Duke shy256@nyu.edu
2018-03-27
Create or Add a column to Spatial Reference Table

stats from raw data:

cusp=> select count(*) from dep_complaints where latitude is not null and longitude is not null;
 count
--------
 431089
(1 row)

cusp=> select count(*) from dep_complaints;
 count
--------
 438181
(1 row)

cusp=> select 431089 * 1.0 / 438181;
        ?column?
------------------------
 0.98381490753820909624
(1 row)

~98% of data has lat lon data. The data without latlon has relevant information in the column resolution_description for the reason for nullity.

Process:
0. instantiate geopandas object shapefile whose path is provided with input param with the crs
1. Query entire data from dim_spatial
Table DDL:
drop table if exists dim_spatial;
create table dim_spatial (
	 location_id                     bigint      primary key                                    ,
	 latitude                        numeric(20,18)                                             ,
	 longitude                       numeric(20,18)
);
"""
import sys
import geopandas as gpd
import matplotlib


# 0. instantiate geopandas object shapefile whose path is provided with input param with the crs
fp, crs = sys.argv[1], sys.argv[2]
shp = gpd.read_file(fp)
print(shp.columns)
print(shp.head())
shp.plot()


