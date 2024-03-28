from datetime import datetime
import logging
import os
import asyncio
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from selenium_driverless.types.webelement import WebElement
import json
import re


logs_folder = (os.getcwd() + '\\logs')

options = webdriver.ChromeOptions()

def setup_logging(logs_folder):
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    currentDate = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    logFilePath = os.path.join(logs_folder, f"Scraper-{currentDate}.log")

    logging.basicConfig(
        filename=logFilePath,
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%I:%M:%S %p'
    )


def log(message):
    print(message)
    logging.info(message)

resource_links = {
    "Food bank": "https://greatnonprofits.org/organizations/browse/search:Food%20bank/sort:review_count/direction:desc/page:1",
    "Animals": "https://greatnonprofits.org/organizations/browse/search:animals/sort:review_count/direction:desc/page:1",
    "Veteran": "https://greatnonprofits.org/organizations/browse/search:Veteran%20Support/sort:review_count/direction:desc/page:1",
    "Substance abuse": "https://greatnonprofits.org/organizations/browse/search:Substance%20drugs%20abuse/sort:review_count/direction:desc/page:1"
}


#######################################################################################


async def main():
    setup_logging(logs_folder)
    
    with open('organizations.json', 'w') as file:
        json.dump({}, file)

    async with webdriver.Chrome(options=options) as driver:
        await driver.get('https://www.example.com')
        for resource_type, link in resource_links.items():
            
            initial = await driver.new_window('tab')
            await driver.switch_to.window(initial)
            await driver.get(link)

            log(f"Opened {resource_type} link")


            while True:
                #Check if there are less than 5 reviews on the current page
                reviews = await driver.find_element(By.CSS_SELECTOR, 'span[itemprop="reviewCount"]')
                reviews_text = await reviews.get_property("innerText")
                if int(reviews_text) < 6:
                    log("No more orgs to scrape for this resource type")
                    await driver.close()
                    break

                #Get all organization sections
                li_elements = await driver.find_elements(By.CSS_SELECTOR, 'li[typeof="Organization"]')

                for li_element in li_elements[:9]:

                    #Open organization page
                    anchor_element = await li_element.find_element(By.TAG_NAME, 'a')
                    anchor_link = await anchor_element.get_attribute('href')
                    new_target = await driver.new_window('tab')
                    await driver.switch_to.window(new_target)
                    await driver.get(anchor_link)

                    await asyncio.sleep(1)
                    link_data = {}
                    orgname = await driver.find_element(By.CSS_SELECTOR, 'h1[itemprop="name"]')
                    orgname = await orgname.get_property("textContent")
                    orgname = orgname.capitalize()
                    link_data['name'] = orgname
                    log(f"Got name: {orgname}")

                    description = await driver.find_element(By.CSS_SELECTOR, 'div[itemprop="description"]')
                    ptags = await description.find_elements(By.TAG_NAME, 'p')
                    descriptionTag = ptags[1]
                    description = await descriptionTag.get_property("textContent")
                    description = description.replace('Mission:', '')
                    description = description.strip()

                    link_data['description'] = description
                    log(f"Got description: {description}")


                    imagediv = await driver.find_element(By.ID, 'np-logo')
                    image = await imagediv.find_element(By.CSS_SELECTOR, 'img[itemprop="image"]')
                    image = await image.get_attribute('src')

                    link_data['image'] = image
                    log(f"Got image: {image}")

                    ul_element = await driver.find_element(By.ID, "np-info-details")
                
                    for li in await ul_element.find_elements(By.TAG_NAME, 'li'):
                        email_element = await li.find_elements(By.CSS_SELECTOR, 'a[itemprop="email"]')
                        if email_element:
                            link_data['email'] = await email_element[0].get_property("textContent")
                            log(f"Got email: {link_data['email']}")

                        telephone_element = await li.find_elements(By.CSS_SELECTOR, 'span[itemprop="telephone"]')
                        if telephone_element:
                            link_data['phone'] = await telephone_element[0].get_property("textContent")
                            log(f"Got phone: {link_data['phone']}")

                        url_element = await li.find_elements(By.CSS_SELECTOR, 'a[itemprop="url"]')
                        if url_element:
                            link_data['url'] = await url_element[0].get_attribute('href')
                            log(f"Got URL: {link_data['url']}")
                            break

                    address_li = await ul_element.find_element(By.CSS_SELECTOR, 'li[itemprop="address"]')
                    if address_li:
                        address_data = {}
                        spans = await address_li.find_elements(By.TAG_NAME, 'span')
                        address = spans[1]
                        
                        streetAddress = await address.find_element(By.CSS_SELECTOR, 'span[itemprop="streetAddress"]')
                        streetAddressText = await streetAddress.get_property("innerText")
                        address_data['streetAddress'] = streetAddressText.strip()
                        
                        addressLocality = await address.find_element(By.CSS_SELECTOR, 'span[itemprop="addressLocality"]')
                        addressLocalityText = await addressLocality.get_property("innerText")
                        address_data['addressLocality'] = addressLocalityText.strip()
                        
                        addressRegion = await address.find_element(By.CSS_SELECTOR, 'span[itemprop="addressRegion"]')
                        addressRegionText = await addressRegion.get_property("innerText")
                        address_data['addressRegion'] = addressRegionText.strip()
                        
                        postalCode = await address.find_element(By.CSS_SELECTOR, 'span[itemprop="postalCode"]')
                        postalCodeText = await postalCode.get_property("innerText")
                        address_data['postalCode'] = postalCodeText.strip()
                        
                        addressCountry = await address.find_element(By.CSS_SELECTOR, 'span[itemprop="addressCountry"]')
                        addressCountryText = await addressCountry.get_property("innerText")
                        address_data['addressCountry'] = addressCountryText.strip()
                        
                        link_data['address'] = address_data
                        log(f"Got address: {address_data}")
                            
                    # Load the existing data from the JSON file
                    with open('raw.json', 'r') as file:
                        data = json.load(file)
                    
                    # Add the organization data to the loaded data
                    if resource_type not in data:
                        data[resource_type] = []
                    data[resource_type].append(link_data)
                    
                    # Write the updated data back to the JSON file
                    with open('raw.json', 'w') as file:
                        json.dump(data, file, indent=4)


                    await driver.close()

                #Increment the page number and navigate to the next page
                await driver.switch_to.window(initial)
                url = await driver.current_url
                match = re.search(r"/page:(\d+)", url)
                if match:
                    current_page = int(match.group(1))
                    incremented_page = current_page + 1
                    new_url = re.sub(r"/page:\d+", f"/page:{incremented_page}", url)
                    log(f"Next Page... ({incremented_page})")
                    log(f"New URL: {new_url}")
                    await driver.get(new_url)
                else:
                    log("No page number found in the URL.")
                    break

asyncio.run(main())
