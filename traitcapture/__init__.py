from sqlalchemy import Column, String, ForeignKey, Float, DateTime, Text
from sqlalchemy import Integer, Date, LargeBinary, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Create Session class
ENGINE = "sqlite:///traitcapture.db"
engine = create_engine(ENGINE)
Session = sessionmaker(bind=engine)


# Setup base
TableBase = declarative_base()
# give all tables a primary key
TableBase.id = Column(Integer, primary_key=True)


def _validate_kwargs(kwargs, validation):
    for key, value in kwargs.iteritems():
        if not validation[key](value):
            raise ValueError("Bad value for %s: %r." % (key, value))


class MissingValueError(ValueError):
    
    def __init__(self, field, table):
        message = "A value is required for field '%s' in table '%s'" % \
                (field, table)
        super(MissingValueError, self).__init__(message)


class BadValueError(ValueError):
    
    def __init__(self, given_value, field, table):
        message = "'%r' is an invalid value for '%s' in table '%s'" % \
                (given_value, field, table)
        super(BadValueError, self).__init__(message)


class Accession(TableBase):
    __tablename__ = "accessions"
    accession_name = Column(String(255), nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    anuid = Column(String(45), nullable=False, index=True, unique=True)
    population = Column(String(255))
    collector_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date_collected = Column(DateTime, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    alitude = Column(Float)
    datum = Column(String(10))
    collection_trip_id = Column(Integer, ForeignKey('collection_trips.id'))
    maternal_lines = Column(Integer(2))
    box_name = Column(String(255))
    source = Column(Text)
    external_id = Column(String(45))
    background = Column(String(45))
    generation = Column(String(4))
    country_origin = Column(String(45))
    habitat = Column(Text)
    notes = Column(Text)
    
    validation = {
            "accession_name": lambda v: v is not None and isinstance(v, str),
            "species_id": lambda v: isinstance(v, int),
            "anuid": lambda v: v is None,
            }

    def __init__(self, **kwargs):
        
        for key, value in kwargs.iteritems():
            self.__setattr__(key, value)
        self.session = Session()
        self._make_anuid()

    def _make_anuid(self):
        todays_accessions = self.session.query(Accession.id).\
                filter(Accession.collector_id == self.collector_id,
                Accession.date_collected == self.date_collected,
                Accession.species_id == self.species_id).all()
        accession_counter = len(todays_accessions) + 1

        species_abbrev = self.session.query(Species.abbreviation).\
                filter(Species.id == self.species_id).scalar()

        anuid = ""
        anuid += species_abbrev
        anuid += "_" 
        anuid += str(self.date_collected.year)[:2]
        anuid += str(self.date_collected.month)[:2]
        anuid += str(self.date_collected.day)[:2]
        anuid += "_"
        anuid += str(accession_counter)
        self.anuid = anuid


class CollectionTrip(TableBase):
    __tablename__ = "collection_trips"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(Text)
    notes = Column(Text)
    kml = Column(LargeBinary)


class Experiment(TableBase):
    __tablename__ = "experiments"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    notes = Column(Text)


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

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.__setattr__(key, value)


class Species(TableBase):
    __tablename__ = "species"
    genus = Column(String(255), nullable=False)
    species = Column(String(511), nullable=False)
    family = Column(String(255), nullable=False)
    abbreviation = Column(String(5), nullable=False)
    __table_args__ = (
            UniqueConstraint("genus", "species"),
            )

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.__setattr__(key, value)


class Protocol(TableBase):
    __tablename__ = "protocols"
    name = Column(String(45), unique=True, nullable=False)
    protocol = Column(Text, nullable=False)
    machine_instructions = Column(LargeBinary)


class ExperimentCondition(TableBase):
    __tablename__ = "experiment_conditions"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'),
            nullable=False)
    notes = Column(Text)


class ExperimentConditionProtcol(TableBase):
    __tablename__ = "experiment_condition_protocols"
    experiment_condition_id = Column(Integer,
            ForeignKey('experiment_conditions.id'), nullable=False)
    ordinal = Column(Integer(3), nullable=False)
    protcol_id = Column(Integer, ForeignKey('protocols.id'), nullable=False)
    protcol_notes = Column(Text)


class ExperimentConditionPreset(TableBase):
    __tablename__ = "experiment_condition_presets"
    name = Column(String(45), index=True, nullable=False)
    description = Column(String(255), index=True)
    notes = Column(Text)

class ExperimentConditionPresetProtcol(TableBase):
    __tablename__ = "experiment_condition_preset_protocols"
    experiment_condition_preset_id = Column(Integer,
            ForeignKey('experiment_condition_presets.id'), nullable=False)
    ordinal = Column(Integer(3), nullable=False)
    protcol_id = Column(Integer, ForeignKey('protocols.id'), nullable=False)

# samples table

#file structure classes go here once we've decided
# raw_data_items


### RELATIONSHIPS

#ExperimentCondition.protocolis = relationship(
#        "ExperimentConditionProtocol",
#        order_by="asc(ExperimentConditionProtocol.ordinal)",
#        primaryjoin="ExperimentConditionProtocol.experiment_condition_id \
#        == ExperimentCondition.id"
#        )

#ExperimentConditionPreset.protocols = relationship(
#    "Protocol",
#    order_by="asc(ExperimentConditionPresetProtocol.order)",
#    primaryjoin="ExperimentConditionPresetProtocol.\
#        experiment_condition _preset_id == ExperimentConditionPreset.id"
#    )




def main():
    # create tables in sqlite
    engine = create_engine(ENGINE, echo=False)
    TableBase.metadata.create_all(engine)
    return True

if __name__ == "__main__":
    main()
