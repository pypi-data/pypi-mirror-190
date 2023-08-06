import datetime

from .get_master_data import *


timezone_hanoi = datetime.timezone(datetime.timedelta(hours=7))

dict_for_fucking_name = {
    "vehicleType": {
        "name": "typeOfVehicle",
        "value_set": vehicle_type,
    },
    "customerType": {
        "name": "typeOfCustomer",
        "value_set": customer_type,
    },
    "depotType": {
        "name": "typeOfDepot",
        "value_set": depot_type,
    },
    "itemType": {
        "name": "typeOfItem",
        "value_set": item_type
    }
}