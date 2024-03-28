import json
import logging
import re

logging.basicConfig(level=logging.INFO,
                    filename='cleanup_log.txt',
                    filemode='w',  
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_dataset(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

def refine_dataset(data):
    seen_names = set()
    for category, resources in data.items():
        new_resources = []
        for resource in resources:

            if resource["description"].strip() == "More Info":
                resource["description"] = "No description available. Visit homepage for more info."
                logging.info(f'Updated description for "{resource["name"]}" in "{category}".')

            if resource["name"] not in seen_names:
                seen_names.add(resource["name"])
                new_resources.append(resource)
            else:
                logging.info(f'Removed duplicate "{resource["name"]}" in "{category}".')

            if "phone" in resource:
                formatted_phone = standardize_phone_number(resource["phone"])
                resource["phone"] = formatted_phone

        data[category] = new_resources
    return data

def standardize_phone_number(phone_number):
    digits = re.sub(r'\D', '', phone_number)  

    if digits.startswith('1') and len(digits) == 11:
        formatted_number = f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return formatted_number

    elif len(digits) == 10:
        formatted_number = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return formatted_number

    else:
        logging.warning(f'Phone number "{phone_number}" could not be standardized.')
        return phone_number  

file_name = 'dataset.json'  
data = load_dataset(file_name)

refined_data = refine_dataset(data)

with open("dataset.json", "w") as file:
    json.dump(refined_data, file, indent=4)

logging.info("The dataset has been refined and saved to 'dataset.json'")
