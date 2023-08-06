import json

# check data with file master_data.json
with open("./components/master_data.json") as f:
    data = json.load(f)
    vehicle_categories = data["vehicle_categories"]
    vehicle_type = data["vehicle_type"]
    depot_type = data["depot_type"]
    customer_type = data["customer_type"]
    matrix_outline = data["matrix_outline"]
    item_type = data["item_type"]