import json
import logging
import re

# Setup logging to output to a file
logging.basicConfig(level=logging.INFO,
                    filename='cleanup_log.txt',
                    filemode='w',  # 'w' to overwrite existing log file, 'a' to append
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load the dataset from a JSON file
def load_dataset(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

# Function to update descriptions and remove duplicates
def refine_dataset(data):
    seen_names = set()
    for category, resources in data.items():
        new_resources = []
        for resource in resources:
            # Update description if needed
            if resource["description"].strip() == "More Info":
                resource["description"] = "No description available. Visit homepage for more info."
                logging.info(f'Updated description for "{resource["name"]}" in "{category}".')

            # Remove duplicates
            if resource["name"] not in seen_names:
                seen_names.add(resource["name"])
                new_resources.append(resource)
            else:
                logging.info(f'Removed duplicate "{resource["name"]}" in "{category}".')

            # Standardize phone number format
            if "phone" in resource:
                formatted_phone = standardize_phone_number(resource["phone"])
                resource["phone"] = formatted_phone

        data[category] = new_resources
    return data

# Function to standardize phone number formats
def standardize_phone_number(phone_number):
    digits = re.sub(r'\D', '', phone_number)  # Remove non-digit characters
    
    # Check if it starts with '1' and has 11 digits, format with +1 prefix
    if digits.startswith('1') and len(digits) == 11:
        formatted_number = f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        return formatted_number
    
    # Standard format for 10 digit numbers
    elif len(digits) == 10:
        formatted_number = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        return formatted_number
    
    else:
        logging.warning(f'Phone number "{phone_number}" could not be standardized.')
        return phone_number  # Return original if not 10 or 11 digits starting with 1

# Load your dataset
file_name = 'dataset.json'  # Replace 'your_dataset.json' with your actual file name
data = load_dataset(file_name)

# Refine the dataset: update descriptions, remove duplicates, and standardize phone numbers
refined_data = refine_dataset(data)

# Save the refined dataset to a new JSON file
with open("dataset.json", "w") as file:
    json.dump(refined_data, file, indent=4)

logging.info("The dataset has been refined and saved to 'dataset.json'")
