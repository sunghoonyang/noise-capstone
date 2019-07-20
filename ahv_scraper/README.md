# Overview
The New York City Department of Buildings (DOB) issues after-hours variances to construction sites performing activity outside the permitted time bounds of the New York City Noise Code.

This data is accessible through the DOB Building Information website (http://a810-bisweb.nyc.gov/bisweb/bispi00.jsp) but only at the building level and only by navigating through a series of search forms and links. There is no public access to aggregate reporting about AHVs.

Sample online AHV form: http://a810-bisweb.nyc.gov/bisweb/AHVPermitDetailsServlet?requestid=2&allkey=00839419

This tool scrapes the DOB website to return a CSV file with one record per AHV.

Information available: 
* ahv_id (DOB unique identifier for the AHV)
* timestamp_utc (UTC timestamp of script run time)
* building_identification_number (DOB BIN)
* status (AHV status)
* residence_within_200_feet (boolean)
* enclosed_building_work (boolean)
* full_or_partial_demolition (boolean)
* crane_use (boolean)
* requested_for_date_ranges (JSON object with dates and times for the AHV)
* apply_reason
* work_description

With optional join based on BIN:
* the_geom (latitude and longitude ready for Python parsing)
* house_number
* street_name
* zip_code

# Requirements
The scraper has been tested in Python 3.7. Package requirements:
* requests
* bs4
* pandas

# How to Use
The script is called by the main() function.

Scraping is done in the aggregate based on a range of AHV IDs. It cannot be performed for a filtered geography or specific BIN. AHV IDs are sequential. The file can start from a user-inputted AHV ID or from the latest AHV ID already available in the CSV file. By default, new AHV IDs are appended to the CSV file.

The use case for the tool is to run it every few hours or days to capture the latest new AHVs.

The performance of the script is hampered by the DOB's blocking on frequent web requests. Very rough performance expectations are 80 AHVs per minute or 4,000 AHVS per hour.

The script runs on the main() function, which takes in the following arguments:
* start_ahv_id: The AHV ID from which to begin scraping (with or without two leading zeros) (default: 00895134)
* not_found_retries: Threshold for when to stop the scraping based on total AHV ID not found results (default: 5)
* max_times_blocked: Threshold for then to stop the scraping based on blocks (0=no limit) (default: 0)
* sleep_seconds: Seconds to sleep between requests
* spoof_chrome: Use a user agent and request headers from Google Chrome (may reduce blocks?)
* csv_file_name: CSV file to read and write to
* csv_write_mode: 'overwrite' to recreate the file; append to add the latest AHV rows
* delete_terminal_not_found_rows_and_infer_start: If true, the function will delete the last rows
    with a not found status and resume scraping from the latest valid AHV found
    
There is additional code at the end of the file (for convenience/reference) for getting the geographical attributes of the AHV based on the BIN. Geographical attributes by BIN are sourced from the following (documentation, NYC Open Data portal, download link):
* https://github.com/CityOfNewYork/nyc-geo-metadata/blob/master/Metadata/Metadata_AddressPoint.md
* https://data.cityofnewyork.us/City-Government/NYC-Address-Points/g6pj-hd8k
* https://data.cityofnewyork.us/api/views/cpcq-gbvg/rows.csv?accessType=DOWNLOAD

Due to file size, this must be downloaded and placed in the script directory. File name should be Address_Point.csv.

The default file for reading and writing is attached here (ahv_data.csv), along with a sample of some output data.

# Productionizing
Steps needed:
* A server/service to run the script at a specific time interval (recommendation: hourly)
* Likely process to write entries to a database instead of CSV
