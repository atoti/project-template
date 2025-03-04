from .util.skeleton import (
    Column,
    Columns,
    Cube,
    Cubes,
    Dimension,
    Dimensions,
    Hierarchies,
    Hierarchy,
    Level,
    Levels,
    Measure,
    Measures,
    Skeleton,
    Table,
    Tables,
)


class _StationDetailsTableColumns(Columns):
    ID = Column("ID")
    NAME = Column("Name")
    DEPARTMENT = Column("Department")
    CITY = Column("City")
    POSTCODE = Column("Postcode")
    STREET = Column("Street")
    HOUSE_NUMBER = Column("House number")
    CAPACITY = Column("Capacity")


class _StationDetailsTable(Table):
    name = "Station details"
    columns = _StationDetailsTableColumns()


class _StationStatusTableColumns(Columns):
    STATION_ID = Column("Station ID")
    BIKE_TYPE = Column("Bike type")
    BIKES = Column("Bikes")


class _StationStatusTable(Table):
    name = "Station status"
    columns = _StationStatusTableColumns()


class _Tables(Tables):
    STATION_DETAILS = _StationDetailsTable()
    STATION_STATUS = _StationStatusTable()


class _StationCubeStationDetailsDimensionLocationHierarchyLevels(Levels):
    DEPARTMENT = Level(_StationDetailsTableColumns.DEPARTMENT)
    CITY = Level(_StationDetailsTableColumns.CITY)
    POSTCODE = Level(_StationDetailsTableColumns.POSTCODE)
    STREET = Level(_StationDetailsTableColumns.STREET)
    HOUSE_NUMBER = Level(_StationDetailsTableColumns.HOUSE_NUMBER)


class _StationCubeStationDetailsDimensionLocationHierarchy(Hierarchy):
    name = "Location"
    levels = _StationCubeStationDetailsDimensionLocationHierarchyLevels()


class _StationCubeStationDetailsDimensionStationHierarchyLevels(Levels):
    NAME = Level(_StationDetailsTableColumns.NAME)
    ID = Level(_StationDetailsTableColumns.ID)


class _StationCubeStationDetailsDimensionStationHierarchy(Hierarchy):
    name = "Station"
    levels = _StationCubeStationDetailsDimensionStationHierarchyLevels()


class _StationCubeStationDetailsDimensionHierarchies(Hierarchies):
    LOCATION = _StationCubeStationDetailsDimensionLocationHierarchy()
    STATION = _StationCubeStationDetailsDimensionStationHierarchy()


class _StationCubeStationDetailsDimension(Dimension):
    name = _StationDetailsTable.name
    hierarchies = _StationCubeStationDetailsDimensionHierarchies()


class _StationCubeStationStatusDimensionBikeTypeHierarchyLevels(Levels):
    BIKE_TYPE = Level(_StationStatusTableColumns.BIKE_TYPE)


class _StationCubeStationStatusDimensionBikeTypeHierarchy(Hierarchy):
    name = _StationStatusTableColumns.BIKE_TYPE.name
    levels = _StationCubeStationStatusDimensionBikeTypeHierarchyLevels()


class _StationCubeStationStatusDimensionHierarchies(Hierarchies):
    BIKE_TYPE = _StationCubeStationStatusDimensionBikeTypeHierarchy()


class _StationCubeStationStatusDimension(Dimension):
    name = _StationStatusTable.name
    hierarchies = _StationCubeStationStatusDimensionHierarchies()


class _StationCubeDimensions(Dimensions):
    STATION_DETAILS = _StationCubeStationDetailsDimension()
    STATION_STATUS = _StationCubeStationStatusDimension()


class _StationCubeMeasures(Measures):
    CAPACITY = Measure(_StationDetailsTableColumns.CAPACITY.name)
    BIKES = Measure(_StationStatusTableColumns.BIKES.name)


class _StationCube(Cube):
    name = "Station"
    dimensions = _StationCubeDimensions()
    measures = _StationCubeMeasures()


class _Cubes(Cubes):
    STATION = _StationCube()


class _Skeleton(Skeleton):
    cubes = _Cubes()
    tables = _Tables()


SKELETON = _Skeleton()
