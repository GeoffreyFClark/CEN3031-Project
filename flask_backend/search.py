def search_resources(resources, criteria):
    matching_resources = []

    if 'zip' in criteria:
        zip_query = criteria['zip']
        print("Search | searching for zip:", zip_query)
        
        for resource_type in resources:
            for resource in resources[resource_type]:
                if resource["address"]["postalCode"] == zip_query:
                    matching_resources.append(resource)

    return matching_resources