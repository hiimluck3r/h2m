#!/bin/bash

options=()
services=()

WIDTH=10

# Extract and clear information from "config/services.yaml"
extract_info() {
    line="$1"
    servicename=$(echo "$line" | cut -d ':' -f 1)
    status=$(echo "$line" | cut -d ':' -f 2 | cut -d '|' -f 1 | tr -d ' ')
    description=$(echo "$line" | cut -d '|' -f 2 | tr -d ' ')
    
    options+=($servicename)
    options+=($description)
    options+=($status)
    services+=($servicename)
    concatenated_string="${servicename}${description}"
    length=$((${#concatenated_string}+20))
    if (( $length > $WIDTH ));
    then
      WIDTH=$length
    fi
    
}

# Read information from "config/services.yaml"
read_services() {
    # Read the file line by line
    options=()
    services=()
    while IFS= read -r line; do
        extract_info "$line"
    done < config/services.yaml
}

# Display menu
display_checklist() {
    # Create the checklist menu using whiptail
    read_services
    local choices=$(whiptail --title "Available services" \
        --ok-button "OK" --nocancel \
        --checklist "Select the services you want to install:" \
        20 "$WIDTH" 8 "${options[@]}" 3>&1 1>&2 2>&3)

    for each in "${services[@]}"; do
        if [[ ${choices[@]} =~ $each ]]; then
            sed -i "s/$each: [^ ]*/$each: ON/" config/services.yaml
        else
            sed -i "s/$each: [^ ]*/$each: OFF/" config/services.yaml
        fi
    done
    
    sed 's/ON.*/ON/' config/services.yaml > group_vars/all/all_services.yml
    sed -i 's/OFF.*/OFF/' group_vars/all/all_services.yml
}

display_checklist