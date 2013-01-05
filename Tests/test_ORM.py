import unittest
import traitcapture
from traitcapture import TableBase, Accession, Species, User, ENGINE, Session
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from datetime import datetime


class ORM(unittest.TestCase):
    
#    def test_ormsetup(self):
#        engine = create_engine(ENGINE)
#        session = sessionmaker(bind=engine)()
#        TableBase.metadata.create_all(engine)
#        self.assertTrue(traitcapture.main())

    def setUp(self):
        self.engine = create_engine(ENGINE)
        self.session = Session()
        TableBase.metadata.create_all(self.engine)
        self.session.commit()

        species = Species(**{
                "genus": "Eucalyptus",
                "species": "delagatensis",
                "family": "Myrtaceae",
                "abbreviation": "Eudel"
                })
        self.session.add(species)
        self.session.commit()
        self.species_id = species.id
        
        user = User(**{
                "user_name": "testuser",
                "given_name": "test",
                "family_name": "user",
                "email": "test@example.com",
                "phone_number": "+6123456789",
                "organisation": "test_organisation"
                })
        self.session.add(user)
        self.session.commit()
        self.user_id = user.id

    def test_accession(self):
        record = {
                "accession_name": "test_sp",
                "species_id": 1,
                "collector_id": 1,
                "date_collected": datetime(2012, 12, 12, 12, 12, 12,0),
                }
        
        # Create
        record_instance = Accession(**record)
        self.assertTrue(isinstance(record_instance, Accession))
        
        # Consistency
        for key, value in record.iteritems():
            self.assertEqual(getattr(record_instance, key), value)

        # Insert
        self.session.add(record_instance)
        self.session.commit()
        self.assertEqual(record_instance.id, 1)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
