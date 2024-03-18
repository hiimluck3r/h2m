import time
import yaml
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
import re
from rich.console import Console

console = Console()

services = []

with open('../group_vars/all/h2mcfg.yml', 'r') as cfg_file:
    config_info = yaml.safe_load(cfg_file)

with open('../config/services.yml', 'r') as services_file:
    lines = services_file.readlines()
    for each in lines:
        service, latter = each.split(': ')
        status, description = latter.split(' | ')
        services.append({
            'name': service,
            'status': status,
            'description': description})

item_options = []
ticked = []
for each in services:
    item_options.append(f"{each['name']} - {each['description']}")
    if each['status'] == 'ON':
        ticked.append(services.index(each))

console.print("Select the applications you want to run:")
# Choose multiple options from a list
items = select_multiple(item_options, tick_character='x', ticked_indices=ticked, return_indices=True)
items = sorted(items)

#Change files
with open('../config/services.yml', 'w') as services_file:
    for each in services:
        if services.index(each) in items:
            services_file.writelines(f"{each['name']}: ON | {each['description']}")
        else:
            services_file.writelines(f"{each['name']}: OFF | {each['description']}")

with open('../group_vars/all/services.yml', 'w') as services_file:
    services_file.writelines('---\n')
    for each in services:
        if services.index(each) in items:
            services_file.writelines(f"{each['name']}: ON\n")
        else:
            services_file.writelines(f"{each['name']}: OFF\n")

for each in services:
    if services.index(each) in items:
        with open(f"../roles/apps/tasks/{each['name']}.yml", 'r') as task_file:
            task_data = task_file.read()
        
        current_domain = re.findall(r'domain: .*', task_data)[0]
        print(f'Current domain for {each["name"]} service: {current_domain}')
        print(f'Configure domain for {each["name"]} service: ')
        domain = select_multiple(config_info['domains'], tick_character='x', maximal_count=1, ticked_indices=[0])
        domain = domain[0]
        task_data = task_data.replace(current_domain, f'domain: {domain}')
        
        with open(f"../roles/apps/tasks/{each['name']}.yml", 'w') as task_file:
            task_file.write(task_data)

spinner = Spinner(DOTS, "Changing configuration...")
spinner.start()

time.sleep(0.5)
print('Done!')
spinner.stop()