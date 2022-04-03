import requests
import json
from urllib.request import urlopen, Request


style_list = []


user = "Udealio"
password = "gXKuZg3at4EZkQDY"
obj = {"username":"Udealio",
"password":"gXKuZg3at4EZkQDY"}
token = requests.post('https://www.udealio.com/token/obtain/', data = obj)
token_json = token.json()
token_json_access = token_json['access']
token_header = "JWT " + token_json_access
header = {'Content-Type': 'application/json',
            'authorization': token_header}

resp_style = requests.get('https://www.udealio.com/apiStyle/', headers=header)
resp_clothing = requests.get('https://www.udealio.com/apiClothing/', headers=header)
resp_clothing_type = requests.get('https://www.udealio.com/apiClothingStyle/', headers=header)



count=0
for resp_style_data in resp_style.json():
    style_clothing_list = []
    style_clothing_type_list = []
    style_exclude_list =[]
    
    style_clothing_list.append(resp_style_data['clothing'])
    style_clothing_type_list.append(resp_style_data['clothing_type'])
    style_exclude_list.append(resp_style_data['exclude'])

    temp_clothing_list = []
    for clothing_link_list in style_clothing_list:
        for clothing_link in clothing_link_list:
            split_link_clothing = clothing_link.split('/')
            clothing_id = split_link_clothing[-2]
    
            for resp_clothing_data in resp_clothing.json():
                if str(resp_clothing_data['id']) == str(clothing_id):
                    temp_clothing_list.append(resp_clothing_data['name'])

    temp_clothing_type_list = []
    for clothing_type_link_list in style_clothing_type_list:
        for clothing_type_link in clothing_type_link_list:
            split_link_clothing_type = clothing_type_link.split('/')
            clothing_type_id = split_link_clothing_type[-2]
    
            for resp_clothing_type_data in resp_clothing_type.json():
                if str(resp_clothing_type_data['id']) == str(clothing_type_id):
                    temp_clothing_type_list.append(resp_clothing_type_data['name'])


    temp_exclude_list = []
    for exclude_link_list in style_exclude_list:
        for exclude_link in exclude_link_list:
            split_link_exclude = exclude_link.split('/')
            exclude_type_id = split_link_exclude[-2]
            
            for resp_exclude_data in resp_clothing_type.json():
                if str(resp_exclude_data['id']) == str(exclude_type_id):
                   temp_exclude_list.append(resp_exclude_data['name'])

        temp = {'style': resp_style_data['name'], 'clothing': temp_clothing_list, 'clothing_type': temp_clothing_type_list, 'exclude': temp_exclude_list}
        style_list.append(temp)

#print(style_list)
title = 'spaghetti straps'
for style in style_list:
    exclude = False
    for exclusion in style['exclude']:
        exclusion = exclusion.lower()
        if exclusion in title.lower():
            print(style['exclude'],title+'exclude')
            exclude = True
    if exclude == False:
        for clothing in style['clothing']:
            clothing = clothing.lower()
            if clothing in title.lower():
                print(style['style'],title)
                
                
        for clothing_type in style['clothing_type']:
            clothing_type = clothing_type.lower()
            if clothing_type in title.lower():
                print(style['clothing_style'],title)
            

