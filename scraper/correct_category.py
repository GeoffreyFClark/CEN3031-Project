import json
import logging

logging.basicConfig(level=logging.INFO, 
                    filename='correct_category_log.txt', 
                    filemode='w',  # 'w' to overwrite existing log file, 'a' to append
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_dataset(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)
    
def recategorize_resources(data):
    categories = list(data.keys())
    logging.info(f"Recognized categories: {categories}")  # Log the recognized categories

    # Keywords associated with the "Animal" category
    animal_keywords = ['cats', 'dog']
    description_keywords = ['pet', 'animal']

    new_data = {category: [] for category in categories}
    all_resources = [(resource, original_category) for original_category in categories for resource in data[original_category]]

    # Assign each resource to the correct category based on its name, keywords, and description
    for resource, original_category in all_resources:
        # Check for specific keywords in name or description to move to "Animal"
        if any(keyword in resource["name"].lower() for keyword in animal_keywords) or \
           any(keyword in resource["description"].lower() for keyword in description_keywords):
            new_data["Animal"].append(resource)
            if original_category != "Animal":
                logging.info(f'Moving "{resource["name"]}" to "Animal" based on keywords in its name or description.')
            continue

        # Check for category match in resource name
        found_category = False
        for target_category in categories:
            if target_category.lower() in resource["name"].lower():
                if original_category != target_category:
                    new_data[target_category].append(resource)
                    logging.info(f'Moving "{resource["name"]}" from "{original_category}" to "{target_category}" based on its name.')
                else:
                    logging.info(f'"{resource["name"]}" is already in the correct category "{original_category}". No move needed.')
                found_category = True
                break
        if not found_category:
            new_data[original_category].append(resource)  # Keep in its original category if no match is found

    return new_data


def save_corrected_dataset(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    raw_data = 'raw.json'
    data = load_dataset(raw_data)
    

    corrected_data = recategorize_resources(data)
    
    # Save the corrected dataset
    corrected_file_name = 'dataset.json'
    save_corrected_dataset(corrected_data, corrected_file_name)
    
    print("The resources have been re-categorized and saved to '{}'".format(corrected_file_name))
