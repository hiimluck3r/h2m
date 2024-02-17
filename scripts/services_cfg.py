import time
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
from rich.console import Console

console = Console()

services = []

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

spinner = Spinner(DOTS, "Changing configuration...")
spinner.start()

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

time.sleep(0.5)
print('Done!')
spinner.stop()