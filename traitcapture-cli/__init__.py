from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

TableBase = declarative_base()

# give all tables a primary key
TableBase.id = Column(Integer, primary_key=True)

class Accession(TableBase):
    __tablename__ = "accessions"
    accession_name = Column(String(255), nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'))
    anuid = Column(String(45), nullable=False, index=True, unique=True)
    population = Column(String(255))
    collector_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_collected = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    alitude = Column(Float)
    datum = Column(String(10), nullable=False)
    collection_trip_id = Column(Integer, ForeignKey('collection_trips.id'))
    maternal_lines = Column(Integer(2), nullable=False)
    box_name = Column(String(255))
    source = Column(Text)
    external_id = Column(String(45))
    background = Column(String(45))
    generation = Column(String(4))
    country_origin = Column(String(45))
    habitat = Column(Text)
    notes = Column(Text, index=True)


class CollectionTrip(TableBase):
    __tablename__ = "collection_trips"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = False)
    location = Column(Text)
    notes = Column(Text, index=True)
    kml = Column(LargeBinary)


class Experiment(TableBase):
    __tablename__ = "experiments"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable = False)
    end_date = Column(Date, nullable = False)
    notes = Column(Text, index=True)

class Pedigree(TableBase):
    __tablename__ = "pedigrees"
    experiment_id = Column(Integer, ForeignKey('experiments.id'),
            nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    first_parent_plant_id = Column(Integer, ForeignKey('plants.id'))
    first_parent_gender = Column(Integer(1))
    second_parent_plant_id = Column(Integer, ForeignKey('plants.id'))
    second_parent_gender = Column(Integer(1))


class Plant(TableBase):
    __tablename__ = "plants"
    accession_id = Column(Integer, ForeignKey('accessions.id'), nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'),
            nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tray_number = Column(Integer(3))
    tray_position = Column(String(3))
    chamber_position = Column(String(3))
    anuid = Column(String(45))
    experiment_condition_id = Column(Integer,
            ForeignKey('experiment_conditions.id'), nullable=False)


class User(TableBase):
    __tablename__ = "users"
    user_name = Column(String(45), index=True, unique=True)
    given_name = Column(String(511), index=True)
    family_name = Column(String(511), index=True)
    email = Column(String(45), index=True, unique=True)
    phone = Column(String(45))
    organisation = Column(String(45))

class Species(TableBase):
    __tablename__ = "species"
    genus = Column(String(255))
    species = Column(String(511))
    family = Column(String(255))
    abbreviation = Column(String(5))
    __table_args__ = (
            UniqueConstraint("genus", "species"),
            )

class Protocol(TableBase):
    __tablename__ = "protocols"
    protocol_name = Column(String(45))
    protocol = Column(Text, index=True, unique=True)
    machine_instructions = Column(LargeBinary)


class ExperimentCondition(TableBase):  # NOT FINISHED
    __tablename__ = "experiment_conditions"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'),
            nullable=False)
    notes = Column(Text, index=True)


class ExperimentConditionPreset(TableBase):  # NOT FINISHED
    __tablename__ = "experiment_condition_presets"
    experiment_id = Column(Integer, ForeignKey('experiments.id'),
            nullable=False)
    notes = Column(Text, index=True)


#file structure classes go here once we've decided
# raw_data_items


# create it
engine = create_engine("sqlite:///traitcapturedev.db")
TableBase.metadata.create_all(engine)

