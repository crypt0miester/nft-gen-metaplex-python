from PIL import Image 
import random
import json
from multiprocessing.pool import Pool
from functools import partial
import time

start = time.time()

CONFIGURATION_NAME = 'traits-configuration.json'; 

EXTERNAL_LINK = ""
TOTAL_IMAGES = 10 # Number of random unique images we want to generate
pool_size = 5  # your "parallelness"

all_images = [] 

f = open(CONFIGURATION_NAME,) 
data = json.load(f)
traits = data['breakdown']

# A recursive function to generate unique image combinations
def create_new_image():
    
    new_image = {} #

    trait_list = [trait for trait in traits]
    # print(trait_list)
    # For each trait category, select a random trait based on the weightings 
    for trait in trait_list:
        # print(trait, traits[trait].items())
        trait_type = [k for k,v in traits[trait].items()]
        trait_value = [v * 100 for k,v in traits[trait].items()]

        new_image[trait] = random.choices(trait_type, trait_value)[0]
    
    # print(new_image)
    if new_image in all_images:
        return create_new_image()
    else:
        return new_image
    
    

# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 
    
    new_trait_image = create_new_image()
    
    all_images.append(new_trait_image)

def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))

# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1

METADATA_FILE_NAME = 'metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value.split(".")[0]
    }

f = open('traits-default.json',) 
metadata = json.load(f)

pool = Pool(pool_size)

im = {}
com = {}
com_of_previous = {}


def generate_images_and_metadata(all_images, n):    
    items = all_images[n]
    token_id = items['tokenId']
    token = {
        "image": str(token_id) + '.png',
        "name": metadata['name'] + str(token_id),
        "properties": {
            "files": [{
                "uri": str(token_id) + '.png',
                "type": "image/png"
                }]},
        "attributes": []
    }
    # token['description'] = f"A member of the Blueblood family with a body of {items['Body'].split('.')[0]}, sitting on a {items['Throne'].split('.')[0]}, wearing a {items['Headpiece'].split('.')[0]}.",
    token['external_link'] = EXTERNAL_LINK
    for item, index in zip(items, range(len(items))):
        if 'tokenId' not in item:
            im[index] = Image.open(f'assets/{item}/{items[item]}').convert('RGBA')
            token["attributes"].append(getAttribute(item, items[item]))
        if index in [1,2]:
            com[index] = Image.alpha_composite(im[index-1], im[index])
        
        if index >= 2 and index != len(items)-1:
            com[index] = Image.alpha_composite(com[index-1], im[index])
        
    all_images_in_one = com[len(items)-2]
    file_name = str(items["tokenId"]) + ".png"
    all_images_in_one.save("out/" + file_name)

    metadata_final = {**metadata, **token}
    with open('out/' + str(token_id) + '.json', 'w') as outfile:
        json.dump(metadata_final, outfile, indent=4)


print(f"done collecting data, it took: {time.time() - start}, now we create the images, sit tightly.")

list_of_index = [index for index in range(len(all_images))]
interval = 0
data_length = len(all_images)
# print(all_images[0])
for data in range(int(data_length/pool_size)):
    list_in_pool = list_of_index[interval:interval+pool_size]
    print(f"working on: {data=}, {list_in_pool}")
    p = Pool(pool_size)
    func= partial(generate_images_and_metadata, all_images)
    p.map(func, list_in_pool)
    interval += pool_size
    p.close()
    p.join()
    time.sleep(0.3)

print(f"done collecting creating images, it took: {time.time() - start}")