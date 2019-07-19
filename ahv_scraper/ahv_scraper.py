
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime
import pandas as pd
import json


# In[17]:


def main(start_ahv_id='00896479', 
         not_found_retries=5, 
         max_times_blocked=0,
         max_times_hard_blocked=5,
         sleep_seconds=0.1,
         spoof_chrome=True,
         show_print_log=True,
         csv_filename='ahv_data.csv',
         csv_write_mode='append',
         delete_terminal_not_found_rows_and_infer_start=True):
    """
    Scrape the DOB's website for the latest AHVs and write selected attributes to CSV.
    
    Arguments:
        start_ahv_id: The AHV ID from which to begin scraping (with or without two leading zeros)
        not_found_retries: Threshold for when to stop the scraping based on consecutive not found results
        max_times_blocked: Threshold for when to stop the scraping based on blocks (0=no limit)
        max_times_hard_blocked: Threshold for when to stop the scraping based on hard blocks (0=no limit)
        sleep_seconds: Seconds to sleep between requests
        spoof_chrome: Use a user agent and request headers from Google Chrome (may reduce blocks?)
        show_print_log: Print each AHV and its status during run
        csv_filename: CSV file to read and write to
        csv_write_mode: 'overwrite' to recreate the file; append to add the latest AHV rows
        delete_terminal_not_found_rows_and_infer_start: If true, the function will delete the last rows
            with a not found status and resume scraping from the latest valid AHV found
        
    Returns:
        A CSV file (based on csv_filename argument) with the AHV attributes
    """

    if csv_write_mode == 'append' and delete_terminal_not_found_rows_and_infer_start:
        df = pd.read_csv(csv_filename, index_col=0)
        highest_ahv_id = df[df['status']!='AHV does not exist'].index.max()
        df[df.index<=highest_ahv_id].to_csv(csv_filename)  
        start_ahv_id = int(highest_ahv_id) + 1

    current_ahv_id = int(start_ahv_id)
    url = 'http://a810-bisweb.nyc.gov/bisweb/AHVPermitDetailsServlet'
    blocked_counter = 0
    not_found_counter = 0
    hard_blocked_counter = 0

    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        }
    if spoof_chrome:
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }

    blocked_counter_limit = 999999 if max_times_blocked == 0 else max_times_blocked
    
    hard_blocked_counter_limit = 999999 if max_times_hard_blocked == 0 else max_times_hard_blocked

    file_mode = 'w' if csv_write_mode == 'overwrite' else 'a'

    with open(csv_filename, file_mode) as csvfile:

        writer = csv.writer(csvfile)

        if file_mode == 'w':
            writer.writerow(['ahv_id', 
                            'timestamp_utc', 
                            'building_identification_number', 
                            'status',
                            'residence_within_200_feet',
                            'enclosed_building_work',
                            'full_or_partial_demolition',
                            'crane_use',
                            'requested_for_date_ranges',
                            'apply_reason',
                            'work_description'
                            ])

        while not_found_counter < not_found_retries             and blocked_counter < blocked_counter_limit             and hard_blocked_counter < hard_blocked_counter_limit:

            # Set up call and parse HTML
            current_ahv_str = '00' + str(current_ahv_id)
            
            if show_print_log:
                print("AHV ID:", current_ahv_str)

            response = requests.request("GET", url, headers=headers, params={"allkey":current_ahv_str})
            soup = BeautifulSoup(response.text, 'html.parser')

            # Server/client error
            if response.status_code >= 400:
                hard_blocked_counter += 1
                if show_print_log:
                    print("Error status code:", response.status_code)
                    
            # Request blocked due to high demand
            if soup.title.string == 'Visitor Prioritization - NYC Department of Buildings':
                blocked_counter += 1
                
                if show_print_log:
                    print("Blocked")

            # ID does not have an AHV
            elif soup.find('td', {'class':'errormsg'}):
                writer.writerow(
                    [current_ahv_str,
                     datetime.datetime.utcnow().isoformat(),
                     '',
                     'AHV does not exist',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     ''
                    ])

                if show_print_log:
                    print("Not found")
                not_found_counter += 1
                current_ahv_id += 1

            # AHV found
            elif soup.findAll('td', {"class": "maininfo"}):

                ahv_id = current_ahv_str
                timestamp_utc = datetime.datetime.utcnow().isoformat()
                building_identification_number = soup.findAll('td', {"class": "maininfo", "colspan": "3"})[-1].a.string
                status = soup.findAll('td', {"class": "content", "colspan":"4"})[0].string

                bools = ['_check' in str(i) for i in soup.findAll('img',{'height':10})[::2]]
                residence_within_200_feet, enclosed_building_work, full_or_partial_demolition, crane_use = bools

                start_days = [i.string for i in soup.findAll('td', {"class": "centercontent"})[5:][::4]]
                start_times = [i.string for i in soup.findAll('td', {"class": "centercontent"})[7:][::4]]
                end_times = [i.string for i in soup.findAll('td', {"class": "centercontent"})[8:][::4]]
                requested_for_date_ranges = json.dumps(dict(zip(start_days,(zip(start_times, end_times)))))
                apply_reason = soup.findAll('td', {'class':'content', 'colspan':7})[-2].text.split('\xa0')[2]
                work_description = soup.find('td', {'class':'content','colspan':6,'valign':'top'}).string

                writer.writerow(
                    [ahv_id,
                     timestamp_utc,
                     building_identification_number,
                     status,
                     residence_within_200_feet,
                     enclosed_building_work,
                     full_or_partial_demolition,
                     crane_use,
                     requested_for_date_ranges,
                     apply_reason,
                     work_description,
                    ])

                if show_print_log:
                    print("Scraped")
                current_ahv_id += 1
                not_found_counter = 0
                
            time.sleep(sleep_seconds)


# In[18]:


if __name__ == '__main__':
   main(start_ahv_id='00896479',
        not_found_retries=5, 
        max_times_blocked=0, 
        max_times_hard_blocked=5,
        sleep_seconds=0.1,
        spoof_chrome=True,
        show_print_log=True,
        csv_filename='ahv_data.csv',
        csv_write_mode='append',
        delete_terminal_not_found_rows_and_infer_start=True
       )


# In[10]:


# For convenience, add address and latitude/longitude for each AHV based on BIN
df_address = pd.read_csv('Address_Point.csv')
df_ahv = pd.read_csv('ahv_data.csv')
df = df_ahv.merge(df_address[['the_geom','BIN','H_NO','FULL_STREE','ZIPCODE']], how='left', left_on = 'building_identification_number', right_on='BIN')
df.drop(['BIN'], axis=1, inplace=True)
df.rename(columns={"H_NO": "house_number", "FULL_STREE": "street_name", "ZIPCODE":"zip_code"}, inplace=True)
df.to_csv('ahv_data.csv', index=False)

