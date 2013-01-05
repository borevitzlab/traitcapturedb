from traitcapture import Accession, User, Species, ENGINE
import csv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine(ENGINE)
session = scoped_session(sessionmaker(bind=engine))

collector = User(
    **{
     "user_name": "kmurray",
     "given_name": "Kevin",
     "family_name": "murray",
     "email": "k.d.murray.91@gmail.com"
     }
    )

session.add(collector)
session.flush()
session.commit()

species = Species(
    **{
     "genus": "Euc",
     "species": "maculata",
     "family": "Myrt",
     "abbreviation": "Eumac"
     }
    )

session.add(species)
session.flush()
session.commit()

acc_d = {
    "accession_name": "test_sp",
    "species_id": 1,
    "collector_id": 1, 
    "date_collected": datetime.now()
    }
acc = Accession(**acc_d)

session.add(acc)
session.flush()
session.commit()


