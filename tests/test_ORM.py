import unittest
import traitcapture
from traitcapture import orm
from traitcapture.orm import TableBase, Accession, Species, User, Experiment
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from tempfile import mkstemp
from shutil import copy2, rmtree, copytree
import os
from os import path, makedirs


TEST_DIR = path.dirname(__file__)
DATA_DIR = path.join(TEST_DIR, "data")
OUT_DIR = path.join(TEST_DIR, "out")
TEMPLATE_DB = path.join(DATA_DIR, "test.db")


class BaseTest(unittest.TestCase):
    """Base of all tests, includes tmp dir creation/deletion"""
    def setUp(self):
        makedirs(OUT_DIR)

    def tearDown(self):
        rmtree(OUT_DIR)


class BaseORMTest(BaseTest):
    """Base of all ORM-testing cases, creates a db engine"""
    def setUp(self):
        super(BaseTest, self).setUp()
        db_fh, self.db_fn = mkstemp()
        self.engine = create_engine("sqlite://")
        orm.Session = sessionmaker(bind=self.engine)
        orm.TableBase.metadata.create_all(self.engine)
        self.session = orm.Session()
        # add some existing data
        usr = User(
                user_name="test",
                given_name="test",
                family_name="user",
                email="test@example.com",
                phone="+6123456789",
                organisation="test organisation"
                )
        spe = Species(
                genus="Test",
                species="testii",
                family="testaceae",
                abbreviation="Tte",
                )
        self.session.add(usr)
        self.session.add(spe)
        self.session.commit()

    def tearDown(self):
        super(BaseTest, self).tearDown()
        self.session.close()
        os.remove(self.db_fn)

    def _test_add(self, record, expt_id=1, consistency=True):
        # Create
        record_instance = self.model(**record)
        self.assertTrue(isinstance(record_instance, self.model))
        if consistency:
            if isinstance(consistency, dict):
                # Consistency dict from user
                for key, value in consistency.items():
                    self.assertEqual(getattr(record_instance, key), value)
            else:
                # Check consistency with supplied record dict
                for key, value in record.items():
                    self.assertEqual(getattr(record_instance, key), value)
        # Insert
        self.session.add(record_instance)
        self.session.commit()
        self.assertEqual(record_instance.id, expt_id)
        return record_instance

class TestORMSetup(BaseTest):
    # don't explicity use unittests here, we just want errors to be raised
    def test_ormsetup_inmemory(self):
        engine = create_engine("sqlite://")
        session = sessionmaker(bind=engine)()
        TableBase.metadata.create_all(engine)

    def test_orm_generation_function(self):
        db_fn = path.join(OUT_DIR, "test.db")
        orm.main(db_fn)
        self.assertTrue(path.exists(db_fn))


class TestSpecies(BaseORMTest):
    model = Species
    def test_add_species(self):
        """Test adding a species"""
        record = {
                "genus": "Eucalyptus",
                "species": "scoparia",
                "family": "Myrtaceae",
                "abbreviation": "Eusco"
                }
        self._test_add(record, expt_id=2)

    def test_add_species_noabbrev(self):
        """Test adding species without giving an abbreviation"""
        record = {
                "genus": "Eucalyptus",
                "species": "scoparia",
                "family": "Myrtaceae",
                "abbreviation": ""
                }
        # Create
        record_instance = self._test_add(record, expt_id=2,
                consistency=False)
        # manually check abbreviation
        self.assertEqual(record_instance.abbreviation, "Es")

        # add again and check that the abbreviation changes
        record["species"] = "strezleckii"
        record_instance = self._test_add(record, expt_id=3,
                consistency=False)
        # manually check abbreviation
        self.assertEqual(record_instance.abbreviation, "Est")


class TestUser(BaseORMTest):
    model = User
    def test_add_user(self):
        """Test adding a user"""
        record = {
                "user_name": "testuser1",
                "given_name": "test1",
                "family_name": "user",
                "email": "testuser1@example.com",
                "phone_number": "+6123456789",
                "organisation": "test_organisation"
                }
        self._test_add(record, expt_id=2)

class TestExperiment(BaseORMTest):
    model = Experiment
    def test_add_experiment(self):
        """Test adding a expt"""
        record = {
                "user_id": 1,
                "start_date": "2014-02-21",
                "end_date": "2014-02-24",
                "notes": "WVDSFSDFSDFSDFSDFKjsaf;lsdkfjaslkdfjasd"
                }
        expect = {
                "user_id": 1,
                "start_date": datetime(2014, 2, 21, 0, 0),
                "end_date": datetime(2014, 2, 24, 0, 0),
                "notes": "WVDSFSDFSDFSDFSDFKjsaf;lsdkfjaslkdfjasd"
                }
        self._test_add(record, consistency=expect)


class TestAccession(BaseORMTest):
    model = Accession
    def test_add_accession(self):
        """Test adding an accession (required fields only)"""
        record = {
                "accession_name": "test_accession",
                "species_id": 1,
                "user_id": 1,
                "latitude": 145.0,
                "longitude": 45.0,
                "altitude": 45.0,
                "locality_name": "Nowhere",
                "date_collected": datetime(2012, 12, 12, 12, 12, 12,0)
                }
        self._test_add(record)

    def test_add_accession_full(self):
        """Test adding an accession (all fields)"""
        record = {
                "accession_name": "test_accession2",
                "species_id": 1,
                "user_id": 1,
                "latitude": 145.0,
                "longitude": 45.0,
                "altitude": 45.0,
                "locality_name": "Nowhere",
                "date_collected": datetime(2012, 12, 12, 12, 12, 12,0),
                "population": "Test Populations",
                "country": "straya",
                "maternal_lines": -1,
                "storage_location": "In the box that noone knows of.",
                "source": "ABRC",
                "external_id": "abc12345",
                "notes": "Lots of notes here!!!",
                "ala_id": "ala:dccacddacdafcad8d998cad89cd89a8c8dcd4cda",
                }
        self._test_add(record)

    def test_add_accession_extra(self):
        """Test adding an accession (all fields, plus some extra columns)"""
        record = {
                "accession_name": "test_accession2",
                "species_id": 1,
                "user_id": 1,
                "latitude": 145.0,
                "longitude": 45.0,
                "altitude": 45.0,
                "locality_name": "Nowhere",
                "date_collected": datetime(2012, 12, 12, 12, 12, 12,0),
                "population": "Test Populations",
                "country": "straya",
                "maternal_lines": -1,
                "source": "ABRC",
                "external_id": "abc12345",
                "notes": "Lots of notes here!!!",
                "ala_id": "ala:dccacddacdafcad8d998cad89cd89a8c8dcd4cda",
                }
        extras = {
                "habitat": "Barren Concrete",
                "plant_height": 23423,
                "box_name": "In the box in the freezer that noone knows of",
                "some_weird_shit_noone_cares_for": "asdfjsadlfksfsadfsdafd234",
                }
        record.update(extras)
        record_instance = self._test_add(record,
                consistency=False)

        # UNPACK converts str to unicode, so we have to
        expect_extras = {}
        for k, v in extras.items():
            if isinstance(v, str):
                expect_extras[unicode(k)] = unicode(v)
            else:
                expect_extras[unicode(k)] = v
        self.assertDictEqual(orm.UNPACK(record_instance.data), expect_extras)
