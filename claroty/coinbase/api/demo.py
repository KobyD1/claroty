import json
developer = {
    "name": "Dev1",
    "grade": 77,
    "city": "TLV"

}

# with open("Data/developer_file.json","w") as file:  # another option to open file
file = open("./data/json/price_vs_time.json", "w")

json.dump(developer, file)
file.close()
