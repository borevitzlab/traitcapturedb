from __future__ import print_function
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

if bytes == str:
    # py2
    PACK = json.dumps
    UNPACK = json.loads
else:
    #python3
    PACK = lambda x: bytes(json.dumps(x), encoding="utf8")
    UNPACK = lambda x: json.loads(x.decode("utf8"))


ENGINE = "sqlite:///{uri:s}"
DB_FN = "traitcapture.db"
DATE_STR_FORMAT = "%Y-%m-%d"
# Create Session class
engine = create_engine(ENGINE.format(uri=DB_FN))
Session = sessionmaker(bind=engine)

# Setup base
TableBase = declarative_base()
    # give all tables a primary key
TableBase.id = Column(Integer, primary_key=True)
TableBase.data = Column(LargeBinary)


def pack_extras(self, kwargs):
    """Packs extra keys into a k:v store to be put in a LargeBinary column."""
    extras = {}
    for key, value in kwargs.items():
        if hasattr(self, key):
            self.__setattr__(key, value)
        else:
            extras[key] = value
    if extras:
        self.data = PACK(extras)


def _validate_kwargs(kwargs, validation):
    """Performs validation on kwargs to a table class"""
    for key, value in kwargs.items():
        if not validation[key](value):
            raise ValueError("Bad value for %s: %r." % (key, value))


class Accession(TableBase):
    __tablename__ = "accessions"
    accession_name = Column(String(255), nullable=False)
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    has_seed = Column(Boolean, default=True)
    date_collected = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    locality_name = Column(String(255))
    population = Column(String(255))
    country = Column(String(45))
    maternal_lines = Column(Integer)
    storage_location = Column(Text)
    source = Column(Text)
    external_id = Column(String(45))
    notes = Column(Text)
    ala_id = Column(String(63))
    first_parent_id = Column(Integer, ForeignKey('accessions.id'))
    first_parent_gender = Column(Integer)
    second_parent_id = Column(Integer, ForeignKey('accessions.id'))
    second_parent_gender = Column(Integer)
    data = Column(LargeBinary)

    def __init__(self, **kwargs):
        super(Accession, self).__init__()
        pack_extras(self, kwargs)


class Experiment(TableBase):
    __tablename__ = "experiments"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    notes = Column(Text)

    def __init__(self, **kwargs):
        super(Experiment, self).__init__(**kwargs)
        try:
            if isinstance(kwargs["start_date"], str):
                self.start_date = datetime.strptime(kwargs["start_date"],
                        DATE_STR_FORMAT)
            else:
                self.start_date = kwargs["start_date"]
        except KeyError:
            pass
        try:
            if isinstance(kwargs["end_date"], str):
                self.end_date = datetime.strptime(kwargs["end_date"],
                        DATE_STR_FORMAT)
            else:
                self.end_date = kwargs["end_date"]
        except KeyError:
            pass



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
    data = Column(LargeBinary)
    def __init__(self, **kwargs):
        super(Plant, self).__init__()
        pack_extras(self, kwargs)

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
        print("Warning: couldn't create db at {}".format(out_path))
        print("Using ./traitcapture.db as db path")
        main()
