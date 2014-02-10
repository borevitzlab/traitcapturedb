import unittest
import traitcapture
from traitcapture import TableBase, Accession, Species, User
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from datetime import datetime
from tempfile import mkstemp
import os

TEMPLATE_DB = "./Tests/test.db"


class TestORM(unittest.TestCase):
    
    def test_ormsetup(self):
        engine = create_engine("sqlite://")
        session = sessionmaker(bind=engine)()
        TableBase.metadata.create_all(engine)
        self.assertTrue(traitcapture.main())

    def setUp(self):
        db_fh, self.db_fn = mkstemp()
        db_fh = os.fdopen(db_fh, "wb")
        template_fh = open(TEMPLATE_DB, "rb")
        db_fh.write(template_fh.read())
        template_fh.close()
        db_fh.close()
        self.engine = create_engine("sqlite:///%s" % self.db_fn)
        traitcapture.Session = sessionmaker(bind=self.engine)
        self.session = traitcapture.Session()

    def tearDown(self):
        self.session.close()
        os.remove(self.db_fn)

    def test_species(self):
        record = {
                "genus": "Eucalyptus",
                "species": "scoparia",
                "family": "Myrtaceae",
                "abbreviation": "Eusco"
                }
        # Create
        record_instance = Species(**record)
        self.assertTrue(isinstance(record_instance, Species))
        # Consistency
        for key, value in record.iteritems():
            self.assertEqual(getattr(record_instance, key), value)
        # Insert
        self.session.add(record_instance)
        self.session.commit()
        self.assertEqual(record_instance.id, 2)
        
    def test_user(self):
        record = {
                "user_name": "testuser1",
                "given_name": "test1",
                "family_name": "user",
                "email": "testuser1@example.com",
                "phone_number": "+6123456789",
                "organisation": "test_organisation"
                }
        # Create
        record_instance = User(**record)
        self.assertTrue(isinstance(record_instance, User))
        # Consistency
        for key, value in record.iteritems():
            self.assertEqual(getattr(record_instance, key), value)
        # Insert
        self.session.add(record_instance)
        self.session.commit()
        self.assertEqual(record_instance.id, 2)

    def test_accession(self):
        record = {
                "accession_name": "test_accession",
                "species_id": 1,
                "collector_id": 1,
                "date_collected": datetime(2012, 12, 12, 12, 12, 12,0)
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
    runner = unittest.TextTestRunner(verbosity=5)
    unittest.main(testRunner=runner)
