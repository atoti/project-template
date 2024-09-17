from enum import Enum


class Table(Enum):
    STATION_DETAILS = "Station details"
    STATION_STATUS = "Station status"


class StationDetailsTableColumn(Enum):
    ID = "ID"
    NAME = "Name"
    DEPARTMENT = "Department"
    CITY = "City"
    POSTCODE = "Postcode"
    STREET = "Street"
    HOUSE_NUMBER = "House number"
    CAPACITY = "Capacity"


class StationStatusTableColumn(Enum):
    STATION_ID = "Station ID"
    BIKE_TYPE = "Bike type"
    BIKES = "Bikes"


class Cube(Enum):
    STATION = "Station"


class StationCubeHierarchy(Enum):
    BIKE_TYPE = StationStatusTableColumn.BIKE_TYPE.value
    LOCATION = "Location"
    STATION = "Station"


class StationCubeBikeTypeLevel(Enum):
    BIKE_TYPE = StationCubeHierarchy.BIKE_TYPE.value


class StationCubeLocationLevel(Enum):
    DEPARTMENT = StationDetailsTableColumn.DEPARTMENT.value
    CITY = StationDetailsTableColumn.CITY.value
    POSTCODE = StationDetailsTableColumn.POSTCODE.value
    STREET = StationDetailsTableColumn.STREET.value
    HOUSE_NUMBER = StationDetailsTableColumn.HOUSE_NUMBER.value


class StationCubeStationLevel(Enum):
    NAME = StationDetailsTableColumn.NAME.value
    ID = StationDetailsTableColumn.ID.value


class StationCubeMeasure(Enum):
    CAPACITY = StationDetailsTableColumn.CAPACITY.value
    BIKES = StationStatusTableColumn.BIKES.value
