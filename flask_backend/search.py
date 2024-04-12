from pyzipcode import ZipCodeDatabase

def search_resources(resources, criteria):
    matching_resources = []
    zip_query = criteria.get('zip', 'none')
    category_query = criteria.get('category', 'none')
    radius = criteria.get('radius', 0)  # Default radius is 0 if not provided
    print(category_query, zip_query, radius)

    zcdb = ZipCodeDatabase()

    if zip_query and radius > 0:
        # Perform ZIP code radius search
        in_radius = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_query, radius)]
        zip_codes = [x.encode('UTF-8').decode('UTF-8') for x in in_radius]  # Convert to string list
        print(f"Found the following ZIP codes within {radius} miles of {zip_query}:")
        print(", ".join(zip_codes))
    else:
        zip_code_info = zcdb.get(zip_query)
        zip_codes = [zip_query] if zip_code_info else []
        print(f"Searching for resources with ZIP code: {zip_query}")

    for resource_type, resource_list in resources.items():
        if category_query != 'none' and resource_type != category_query:
            continue

        for resource in resource_list:
            if zip_query and resource["address"]["postalCode"] in zip_codes:
                matching_resources.append(resource)
            elif not zip_query:
                matching_resources.append(resource)

    return matching_resources

def search_by_id(resources, ids):
    found_resources = []
    
    for category in resources.values():
        for resource in category:
            if resource['id'] in ids:
                found_resources.append(resource)
    
    return found_resources

