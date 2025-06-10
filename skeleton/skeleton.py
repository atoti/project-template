from .typing import SessionSkeleton

SKELETON: SessionSkeleton = {
    "tables": {
        "Station details": {
            "ID",
            "Name",
            "Department",
            "City",
            "Postcode",
            "Street",
            "House number",
            "Capacity",
        },
        "Station status": {"Station ID", "Bike type", "Bikes"},
    },
    "cubes": {
        "Station": {
            "dimensions": {
                "Station details": {
                    "Location": [
                        "Department",
                        "City",
                        "Postcode",
                        "Street",
                        "House number",
                    ],
                    "Station": ["Name", "ID"],
                },
                "Station status": {"Bike type": ["Bike type"]},
            },
            "measures": {"CAPACITY", "BIKES"},
        }
    },
}
