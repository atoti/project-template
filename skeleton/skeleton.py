from .typing import Skeleton

# Rerun `uv run python -m skeleton` after changing this.
SKELETON: Skeleton = {
    "tables": {
        "Station information": {
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
                "Station information": {
                    "Location": {
                        "Department",
                        "City",
                        "Postcode",
                        "Street",
                        "House number",
                    },
                    "Station": {"Name", "ID"},
                },
                "Station status": {"Bike type": {"Bike type"}},
            },
            "measures": {"Bikes", "Capacity", "contributors.COUNT"},
        }
    },
}
