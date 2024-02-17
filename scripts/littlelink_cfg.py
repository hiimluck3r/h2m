import time
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
from rich.console import Console

console = Console()

socials = []

with open('../config/social.yml', 'r') as social_file:
    lines = social_file.readlines()
    for each in lines:
        social, latter = each.split(': ')
        status, description = latter.split(' | ')
        socials.append({
            'name': social,
            'status': status,
            'description': description})

item_options = []
ticked = []
for each in socials:
    item_options.append(f"{each['name']} - {each['description']}")
    if each['status'] == 'ON':
        ticked.append(socials.index(each))

console.print("Select the socials you want to show:")
# Choose multiple options from a list
items = select_multiple(item_options, tick_character='x', ticked_indices=ticked, return_indices=True)
items = sorted(items)

spinner = Spinner(DOTS, "Changing configuration...")
spinner.start()

#Change files
with open('../config/social.yml', 'w') as social_file:
    for each in socials:
        if socials.index(each) in items:
            social_file.writelines(f"{each['name']}: ON | {each['description']}")
        else:
            social_file.writelines(f"{each['name']}: OFF | {each['description']}")

with open('../roles/apps/manifests/littlelink/deployment.yaml', 'w') as deployment:
    deployment.writelines('''---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: littlelink
spec:
  selector:
    matchLabels:
      app: littlelink
  replicas: 1
  template:
    metadata:
      labels:
        app: littlelink
    spec:
      containers:
      - name: littlelink
        image: ghcr.io/techno-tim/littlelink-server:latest
        ports:
        - containerPort: 80
        env:
        - name: TZ
          value: "{{ TZ }}"
        - name: LANG
          value: "{{ LANG }}"
        - name: META_INDEX_STATUS
          value: "{{ META_INDEX_STATUS }}"
        - name: META_KEYWORDS
          value: "{{ META_KEYWORDS }}"
        - name: OG_SITE_NAME
          value: "{{ OG_SITE_NAME }}"
        - name: OG_TITLE
          value: "{{ OG_TITLE }}"
        - name: OG_DESCRIPTION
          value: "{{ OG_DESCRIPTION }}"
        - name: OG_URL
          value: "{{ OG_URL }}"
        - name: OG_IMAGE
          value: "{{ OG_IMAGE }}"
        - name: OG_IMAGE_WIDTH
          value: "{{ OG_IMAGE_WIDTH }}"
        - name: OG_IMAGE_HEIGHT
          value: "{{ OG_IMAGE_HEIGHT }}"
        - name: GA_TRACKING_ID
          value: GXXXXXXXXXX
        - name: META_TITLE
          value: "{{ META_TITLE }}"
        - name: META_DESCRIPTION
          value: "{{ META_DESCRIPTION }}"
        - name: META_AUTHOR
          value: "{{ META_AUTHOR }}"
        - name: THEME
          value: "{{ THEME }}"
        - name: FAVICON_URL
          value: "{{ FAVICON_URL }}"
        - name: AVATAR_URL
          value: "{{ AVATAR_URL }}"
        - name: AVATAR_2X_URL
          value: "{{ AVATAR_2X_URL }}"
        - name: AVATAR_ALT
          value: "{{ AVATAR_ALT }}"
        - name: NAME
          value: "{{ NAME }}"
        - name: BIO
          value: "{{ BIO }}"
        - name: FOOTER
          value: "{{ FOOTER }}"
        - name: BUTTON_ORDER
          value: "{{ BUTTON_ORDER }}"
''')
    for each in items:
        if socials[each]["name"] == 'CUSTOM':
            
            custom_env = ['CUSTOM_BUTTON_TEXT',
            'CUSTOM_BUTTON_URL',
            'CUSTOM_BUTTON_COLOR',
            'CUSTOM_BUTTON_TEXT_COLOR',
            'CUSTOM_BUTTON_ALT_TEXT',
            'CUSTOM_BUTTON_NAME',
            'CUSTOM_BUTTON_ICON'
            ]
            
            for item in custom_env:
              if 'COLOR' in item:
                deployment.writelines(f'''        - name: {item}
          value: "#{{{{ { item } }}}}" #please be aware of NOT using "#" at the start of the definition\n''')
              else:  
                deployment.writelines(f'''        - name: {item}
          value: "{{{{ { item } }}}}"\n''')
        
        else:
            
            if 'EMAIL' in socials[each]["name"]: #what a mess
              custom_env = ["EMAIL", "EMAIL_ALT"]
              
              for item in custom_env:
                deployment.writelines(f'''        - name: {item}
            value: "{{{{ { item } }}}}"\n''')
            
            else:
              deployment.writelines(f'''        - name: {socials[each]["name"]}
            value: "{{{{ { socials[each]["name"] } }}}}"\n''')

time.sleep(0.5)
print('Done!')
spinner.stop()