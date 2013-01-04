from traitcapture-cli import Accession, get_engine_str
import csv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

engine = create_engine(get_engine_str())
Session = scoped_session(sessionmaker(bind=engine))

