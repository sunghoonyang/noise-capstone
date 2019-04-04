"""
Written By: Duke shy256@nyu.edu
2018-03-27
Pipeline from socrata to cusp pg

Table DDL:
drop table if exists dep_complaints;
create table dep_complaints (
	 unique_key                      bigint      primary key                                               ,
	 agency                          character varying(255)                                     ,
	 agency_name                     character varying(255)                                     ,
	 complaint_type                  character varying(255)                                     ,
	 facility_type                   character varying(255)                                     ,
	address_type                    character varying(255)                                     ,
	 borough                         character varying(255)                                     ,
	 city                            character varying(255)                                     ,
	 community_board                 character varying(255)                                     ,
	 park_borough                    character varying(255)                                     ,
	 park_facility_name              character varying(255)                                     ,
	 cross_street_1                  character varying(255)                                     ,
	 cross_street_2                  character varying(255)                                     ,
	 street_name                     character varying(255)                                     ,
	 incident_address                character varying(255)                                     ,
	 incident_zip                    bigint                                                     ,
	 intersection_street_1           character varying(255)                                     ,
	 intersection_street_2           character varying(255)                                     ,
	 latitude                        numeric(20,18)                                             ,
	 longitude                       numeric(20,18)                                             ,
	 x_coordinate_state_plane        bigint                                                     ,
	 y_coordinate_state_plane        bigint                                                     ,
	 status                          character varying(255)                                     ,
	 resolution_description          text                                                       ,
	 resolution_action_updated_date  timestamp without time zone                                ,
	 created_date                    timestamp without time zone                                ,
	 due_date                        timestamp without time zone                                ,
	 closed_date                     timestamp without time zone                                ,
	 descriptor                      text                                                       ,
	 location                        text
);
"""
__PROJ_DIR__ = '/nfshome/shy256/projects/cs19_urban_noise/shared'
import os
import pandas as pd
pd.set_option("display.max_columns", 101)
import numpy as np
import datetime
import urllib
import requests
from requests.exceptions import ReadTimeout
from sodapy import Socrata
import geopandas as gp
import sqlalchemy
import sys
sys.path.insert(0, __PROJ_DIR__) # include root for access to modules
from time import sleep
from pprint import pprint
from util.postgres_api import PostgresAPI as pg_api
import logging
from APPTOKEN import myToken
# set up logging to file
logging.basicConfig(
     filename=os.path.join(__PROJ_DIR__, 'logs', '311_data_pg_setup.log'),
     filemode='w',
     level=logging.INFO, 
     format= '[%(asctime)s] %(message)s',
     datefmt='%H:%M:%S'
 )

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

_convert_map_np = {
	# 'address_type': 'string_'
	# , 'agency': 'string_'
	# , 'agency_name': 'string_'
	# , 'borough': 'string_'
	# , 'city': 'string_'
	'closed_date': 'datetime64'
	, 'due_date': 'datetime64'    
	# , 'community_board': 'string_'
	# , 'complaint_type': 'string_'
	, 'created_date': 'datetime64'
	# , 'cross_street_1': 'string_'
	# , 'cross_street_2': 'string_'
	# , 'descriptor': 'string_'
	# , 'facility_type': 'string_'
	# , 'incident_address': 'string_'
	, 'incident_zip': 'float64'
	# , 'intersection_street_1': 'string_'
	# , 'intersection_street_2': 'string_'
	, 'latitude': 'float64'
	# , 'location': 'string_'    
	, 'longitude': 'float64'
	# , 'park_borough': 'string_'
	# , 'park_facility_name': 'string_'
	, 'resolution_action_updated_date': 'datetime64'
	# , 'resolution_description': 'string_'
	# , 'status': 'string_'
	# , 'street_name': 'string_'
	, 'unique_key': 'float64'
	, 'x_coordinate_state_plane': 'float64'
	, 'y_coordinate_state_plane': 'float64'
}

_convert_map_sql = {
	'unique_key': sqlalchemy.types.BigInteger()    
	, 'agency': sqlalchemy.types.VARCHAR(length=255)
	, 'agency_name': sqlalchemy.types.VARCHAR(length=255)    
	, 'complaint_type': sqlalchemy.types.VARCHAR(length=255)
	, 'facility_type': sqlalchemy.types.VARCHAR(length=255)    
	, 'address_type': sqlalchemy.types.VARCHAR(length=255)
	, 'borough': sqlalchemy.types.VARCHAR(length=255)
	, 'city': sqlalchemy.types.VARCHAR(length=255)
    , 'community_board': sqlalchemy.types.VARCHAR(length=255)
	, 'park_borough': sqlalchemy.types.VARCHAR(length=255)
	, 'park_facility_name': sqlalchemy.types.VARCHAR(length=255)    
	, 'cross_street_1': sqlalchemy.types.VARCHAR(length=255)
	, 'cross_street_2': sqlalchemy.types.VARCHAR(length=255)
	, 'street_name': sqlalchemy.types.VARCHAR(length=255)    
	, 'incident_address': sqlalchemy.types.VARCHAR(length=255)
	, 'incident_zip': sqlalchemy.types.BigInteger()
	, 'intersection_street_1': sqlalchemy.types.VARCHAR(length=255)
	, 'intersection_street_2': sqlalchemy.types.VARCHAR(length=255)
	, 'latitude': sqlalchemy.types.Numeric(precision=20, scale=18, asdecimal=True)
	, 'longitude': sqlalchemy.types.Numeric(precision=20, scale=18, asdecimal=True)    
	, 'x_coordinate_state_plane': sqlalchemy.types.BigInteger()
	, 'y_coordinate_state_plane': sqlalchemy.types.BigInteger()    
	, 'status': sqlalchemy.types.VARCHAR(length=255)
	, 'resolution_description': sqlalchemy.types.Text()    
	, 'resolution_action_updated_date': sqlalchemy.DateTime()    
	, 'created_date': sqlalchemy.DateTime()
	, 'due_date': sqlalchemy.DateTime()        
    , 'closed_date': sqlalchemy.DateTime()    
	, 'descriptor': sqlalchemy.types.Text()
	, 'location': sqlalchemy.types.Text()    
}

#### connect w/ Socrata 
endpoint = 'https://data.cityofnewyork.us/resource/p5f6-bkga.json'
domain = 'data.cityofnewyork.us'
data_id = 'p5f6-bkga'
token = myToken
client = Socrata(domain, token)
metadata = client.get_metadata(data_id)
columns = [x['name'] for x in metadata['columns']]
meta_amount = [x for x in metadata['columns'] if x['name'] == 'Agency'][0]
retries = 3

#### Start Operation
# 3006411 as of 2019-03-31
batches = int(3006411 // 50000) + 1
i=0
dropped_cols = []
while i < batches:
    fail_cnt = 0
    query ="""
    select
        *
    where
        agency = 'DEP'
--        and created_date >= '2018-01-01'
--        and created_date <= '2018-12-31'
    limit
        50000
    offset
        {}
    """.format(i*50000)
    try:
        results = client.get(data_id, query=query)
    except ReadTimeout:
        fail_cnt += 1
        if retries == fail_cnt:
            logging.warning("batch %d failed" % i)
            continue
        sleep(3)
        continue
    res = pd.DataFrame(results)
    if 'location' in res.columns:
        res.location = res.location.astype(str)
    if len(set(res.columns) - set(_convert_map_sql)): # current batch has an unknown column: dropped
        _drop_cols = [c for c in res.columns if c not in _convert_map_sql.keys()]
        res.drop(labels=_drop_cols, axis=1, inplace=True)
        logging.warning("columns dropped: %s" % str(_drop_cols))
    if len(res.columns) < len(_convert_map_sql): # current batch does not have an expected column: filled with NaN's
        new_c = [c for c in _convert_map_sql.keys() if c not in res.columns]
        for _c in new_c:
            res[_c] = np.nan

    res = res.astype(_convert_map_np, errors='ignore')
    res.to_sql('dep_complaints', pg_api.get_engine(), schema='cs19_urban_noise', if_exists='append', dtype=_convert_map_sql, index=False)
    logging.info("Total number of non-null results: {}".format(meta_amount['cachedContents']['non_null']))
    logging.info("Number of results downloaded: {}".format(len(results)))
    # break
    i += 1

logging.info('The following columns are dropped from ingestion into PG: %s' % str(dropped_cols))