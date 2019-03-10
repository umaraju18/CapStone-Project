# -*- coding: utf-8 -*-
'''
WARNING: Use this code at your own risk, scraping is against Zillow's TOC.

Zillow home listings scraper, using Selenium.  The code takes as input search 
terms that would normally be entered on the Zillow home page.  It creates 11 
variables on each home listing from the data, saves them to a data frame, 
and then writes the df to a CSV file that gets saved to your working directory.

Software requirements/info:
- This code was written using Python 3.5.
- Scraping is done with Selenium v3.0.2, which can pip installed, or downloaded
  here: http://www.seleniumhq.org/download/
- The selenium package requires a webdriver program. This code was written 
  using Chromedriver v2.25, which can be downloaded here: 
  https://sites.google.com/a/chromium.org/chromedriver/downloads
  
'''

import time
import pandas as pd
import zillow_functions as zl

# Create list of search terms.
# Function zipcodes_list() creates a list of US zip codes that will be 
# passed to the scraper. For example, st = zipcodes_list(["10", "11", "606"])  
# will yield every US zip code that begins with "10", begins with "11", or 
# begins with "606", as a list object.
# I recommend using zip codes, as they seem to be the best option for catching
# as many house listings as possible. If you want to use search terms other 
# than zip codes, simply skip running zipcodes_list() function below, and add 
# a line of code to manually assign values to object st, for example:
# st = ["Chicago", "New Haven, CT", "77005", "Jacksonville, FL"]
# Keep in mind that, for each search term, the number of listings scraped is 
# capped at 520, so in using a search term like "Chicago" the scraper would 
# end up missing most of the results.
# Param st_items can be either a list of zipcode strings, or a single zipcode 
# string.
#st = zl.zipcodes_list(st_items = ["94536"])
#st = ['95117']
#st = ['94538']
#st = ['38045 Blacow Rd Fremont CA 94536']

def invoke_zillow_sale_townhouse(zipcode):    
    st = []
    st.append(zipcode)

    # Initialize the webdriver.
    driver = zl.init_driver("/Users/hp/Projects/zillow/Zillow/chromedriver")

    # Go to www.zillow.com/homes
    zl.navigate_to_website(driver, "https://www.zillow.com/homes/for_sale/townhouse_type")

    # Click the "buy" button.
    #zl.click_buy_button(driver)

    # Get total number of search terms.
    num_search_terms = len(st)

    # Initialize list obj that will house all scraped data.
    output_data = []

    number = 1

    # Start the scraping.
    for idx, term in enumerate(st):
        # Enter search term and execute search.
        if zl.enter_search_term(driver, term):
            print("Entering search term %s of %s" % 
                (str(idx + 1), str(num_search_terms)))
        else:
            print("Search term %s failed, moving on to next search term\n***" % 
                str(idx + 1))
            continue

        # Check to see if any results were returned from the search.
        # If there were none, move onto the next search.
        if zl.test_for_no_results(driver):
            print("Search %s returned zero results. Moving on to next search\n***" %
                str(term))
            continue

        # Pull the html for each page of search results. Zillow caps results at 
        # 20 pages, each page can contain 26 home listings, thus the cap on home 
        # listings per search is 520.
        raw_data = zl.get_html(driver)
        print("%s pages of listings found" % str(len(raw_data)))

        # Take the extracted HTML and split it up by individual home listings.
        listings = zl.get_listings(raw_data)
        print("%s home listings scraped\n***" % str(len(listings)))

        # For each home listing, extract the 11 variables that will populate that 
        # specific observation within the output dataframe.
        for home in listings:
            new_obs = []
            parser = zl.html_parser(home)

            print("checking home ", number)
            number += 1
            
            # Latitude
            new_obs.append(parser.get_latitude())

            # Longitude
            new_obs.append(parser.get_longitude())

            # Street Address
            new_obs.append(parser.get_street_address())
            
            # City
            new_obs.append(parser.get_city())
            
            # State
            new_obs.append(parser.get_state())
            
            # Zipcode
            new_obs.append(parser.get_zipcode())
            
            # Bedrooms
            new_obs.append(parser.get_bedrooms())
            
            # Bathrooms
            new_obs.append(parser.get_bathrooms())

            # Sqft
            new_obs.append(parser.get_sqft())

            # Lot Size
            new_obs.append(parser.get_lot_size())

            # Year built
            new_obs.append(parser.get_year_built())

            # Sale Price 
            new_obs.append(parser.get_price())
            
            # Zestimate
            new_obs.append(parser.get_zestimate())

            # Sale Type (House for Sale, New Construction, Foreclosure, etc.)
            new_obs.append(parser.get_sale_type())
            
            # Date Sold
            new_obs.append(parser.get_sold_date())
            
            # Days on the Market/Zillow
            # new_obs.append(parser.get_days_on_market())
            new_obs.append(parser.get_days_on_zillow_sold())
            
            # URL for each house listing
            new_obs.append(parser.get_url())
            
            # Append new_obs to list output_data.
            output_data.append(new_obs)

    # Close the webdriver connection.
    zl.close_connection(driver)

    # Write data to data frame, then to CSV file.
    file_name = "sale_townhouse_%s_%s_%s.csv" % (zipcode, str(time.strftime("%Y-%m-%d")), 
                            str(time.strftime("%H%M%S")))
    columns = ["latitude", "longitude", "address", "city", "state", "zip", "bedrooms", 
            "bathrooms", "sqft", "lot_size", "year_built", "sale_price", "zestimate",
            "sale_type", "date_sold", "days_on_zillow",  "url"]
    pd.DataFrame(output_data, columns = columns).drop_duplicates().to_csv(
        file_name, index = False, encoding = "UTF-8"
    )

invoke_zillow_sale_townhouse("95002")
invoke_zillow_sale_townhouse("95101")
invoke_zillow_sale_townhouse("95103")
invoke_zillow_sale_townhouse("95106")
invoke_zillow_sale_townhouse("95108")
invoke_zillow_sale_townhouse("95109")
invoke_zillow_sale_townhouse("95110")
invoke_zillow_sale_townhouse("95111")
invoke_zillow_sale_townhouse("95112")
invoke_zillow_sale_townhouse("95113")
# zip from 15 to 36
for x in range(15,37):
    tail = str(x)
    fullzip = "951" + tail
    invoke_zillow_sale_townhouse(fullzip)

invoke_zillow_sale_townhouse("95138")
invoke_zillow_sale_townhouse("95139")
invoke_zillow_sale_townhouse("95140")
invoke_zillow_sale_townhouse("95141")
invoke_zillow_sale_townhouse("95148")
# for 50 to 61
for x in range(50,62):
    tail = str(x)
    fullzip = "951" + tail
    invoke_zillow_sale_townhouse(fullzip)

invoke_zillow_sale_townhouse("95164")
invoke_zillow_sale_townhouse("95170")
invoke_zillow_sale_townhouse("95172")
invoke_zillow_sale_townhouse("95173")

#for 90 to 94
for x in range(90,95):
    tail = str(x)
    fullzip = "951" + tail
    invoke_zillow_sale_townhouse(fullzip)

invoke_zillow_sale_townhouse("95196")