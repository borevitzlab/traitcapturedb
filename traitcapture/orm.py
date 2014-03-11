from sqlalchemy import (
        String,
        ForeignKey,
        Float,
        DateTime,
        Text,
        Date,
        LargeBinary,
        Boolean,
        )
from sqlalchemy import Column, Integer, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import (
        MultipleResultsFound,
        NoResultFound,
        )
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import msgpack
import json
PACK = json.dumps
UNPACK = json.loads


# Create Session class
ENGINE = "sqlite:///{uri:s}"
DB_FN = "traitcapture.db"
engine = create_engine(ENGINE.format(uri=DB_FN))
Session = sessionmaker(bind=engine)

# Setup base
TableBase = declarative_base()
    # give all tables a primary key
TableBase.id = Column(Integer, primary_key=True)
TableBase.data = Column(LargeBinary)

def pack_extras(self, kwargs):
    extras = {}
    for key, value in kwargs.items():
        if hasattr(self, key):
            self.__setattr__(key, value)
        else:
            extras[key] = value
    if extras:
        self.data = PACK(extras)


def _validate_kwargs(kwargs, validation):
    for key, value in kwargs.items():
        if not validation[key](value):
            raise ValueError("Bad value for %s: %r." % (key, value))


class Accession(TableBase):
    __tablename__ = "accessions"
    accession_name = Column(String(255), nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    has_seed = Column(Boolean, nullable=False, default=True)
    date_collected = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)
    locality_name = Column(String(255))
    population = Column(String(255))
    country = Column(String(45))
    collection_trip_id = Column(Integer, ForeignKey('collection_trips.id'))
    maternal_lines = Column(Integer)
    storage_location = Column(Text)
    source = Column(Text)
    external_id = Column(String(45))
    notes = Column(Text)
    ala_id = Column(String(63))
    first_parent_id = Column(Integer,
            ForeignKey('accessions.id', post_update=True),
            nullable=False)
    first_parent_gender = Column(Integer)
    second_parent_id = Column(Integer,
            ForeignKey('accessions.id', post_update=True)
            )
    second_parent_gender = Column(Integer)

#    validation = {
#            "accession_name": lambda v: v is not None and isinstance(v, str),
#            "species_id": lambda v: isinstance(v, int),
#            "anuid": lambda v: v is None,
#            }
    def __init__(self, **kwargs):
        super(Accession, self).__init__()
        pack_extras(self, kwargs)


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


class Plant(TableBase):
    __tablename__ = "plants"
    plant_name = Column(String(127), nullable=False, unique=True)
    accession_id = Column(Integer, ForeignKey('accessions.id'), nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'),
            nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    location = Column(String(127))
    layout = Column(Integer)
    layout_type = Column(String(63))
    experiment_condition = Column(Text)
#    experiment_condition_id = Column(Integer,
#            ForeignKey('experiment_conditions.id'), nullable=False)


class User(TableBase):
    __tablename__ = "users"
    user_name = Column(String(45), index=True, unique=True)
    given_name = Column(String(511), index=True)
    family_name = Column(String(511), index=True)
    email = Column(String(45), index=True, unique=True)
    phone = Column(String(45))
    organisation = Column(String(45))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class Species(TableBase):
    __tablename__ = "species"
    genus = Column(String(255), nullable=False, index=True)
    species = Column(String(511), nullable=False, index=True)
    family = Column(String(255), nullable=False, index=True)
    abbreviation = Column(String(63), nullable=False, unique=True, index=True)
    common_name = Column(String(255), index=True)
    __table_args__ = (
            UniqueConstraint("genus", "species"),
            )

    def __init__(self, **kwargs):
        self.session = Session()
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        if "abbreviation" not in kwargs or not kwargs["abbreviation"]:
            abbr_len = 2
            while abbr_len < 64:
                g = max(int(abbr_len * 0.4), 1)
                s = abbr_len - g
                species_abbrev = self.genus[:g] + self.species[:s]
                try:
                    self.session.query(Species).filter(
                            Species.abbreviation == species_abbrev).one()
                    abbr_len += 1
                except NoResultFound:
                    self.abbreviation = species_abbrev
                    break
        self.session.close()

#class Protocol(TableBase):
#    __tablename__ = "protocols"
#    name = Column(String(45), unique=True, nullable=False)
#    protocol = Column(Text, nullable=False)
#    machine_instructions = Column(LargeBinary)
#
#
#class ExperimentCondition(TableBase):
#    __tablename__ = "experiment_conditions"
#    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#    experiment_id = Column(Integer, ForeignKey('experiments.id'),
#            nullable=False)
#    notes = Column(Text)
#
#
#class ExperimentConditionProtcol(TableBase):
#    __tablename__ = "experiment_condition_protocols"
#    experiment_condition_id = Column(Integer,
#            ForeignKey('experiment_conditions.id'), nullable=False)
#    ordinal = Column(Integer, nullable=False)
#    protcol_id = Column(Integer, ForeignKey('protocols.id'), nullable=False)
#    protcol_notes = Column(Text)
#
#
#class ExperimentConditionPreset(TableBase):
#    __tablename__ = "experiment_condition_presets"
#    name = Column(String(45), index=True, nullable=False)
#    description = Column(String(255), index=True)
#    notes = Column(Text)
#
#class ExperimentConditionPresetProtcol(TableBase):
#    __tablename__ = "experiment_condition_preset_protocols"
#    experiment_condition_preset_id = Column(Integer,
#            ForeignKey('experiment_condition_presets.id'), nullable=False)
#    ordinal = Column(Integer, nullable=False)
#    protcol_id = Column(Integer, ForeignKey('protocols.id'), nullable=False)


def main(filename="traitcapture.db"):
    # create tables in sqlite
    engine = create_engine(ENGINE.format(uri=filename), echo=False)
    TableBase.metadata.create_all(engine)

if __name__ == "__main__":
    from sys import argv
    from os import path
    try:
        out_path = argv[1]
    except IndexError:
        out_path = ""
    if path.exists(path.dirname(out_path)):
        main(out_path)
    else:
        print "Warning: couldn't create db at {}".format(out_path)
        print "Using ./traitcapture.db as db path"
        main()
