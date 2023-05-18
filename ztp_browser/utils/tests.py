from django.test import TestCase
from ztp_browser.utils.ztp_opa_client import OPA
import logging
from collections import OrderedDict

logging.basicConfig(level=logging.INFO)


# Create your tests here.
class OPATestCase(TestCase):
    """to test the opa class"""

    def test_opa_con(self):
        logging.debug("Testing OPA Connection")
        client = OPA()
        val = client.checkin
        self.assertTrue(val)

    def test_login_policy(self):
        logging.debug("Testing OPA Login Rule for TS, S, U roles")
        logging.debug("Testing OPA Login Rule for TS role")
        client = OPA()
        data = {"user": {"clearance": "TOPSECRET"}}
        self.assertTrue(client.check_policy_rule(data, "policy", "allow_login"))

        logging.debug("Testing OPA Login Rule for S role")
        data = {"user": {"clearance": "SECRET"}}
        self.assertTrue(client.check_policy_rule(data, "policy", "allow_login"))

        logging.debug("Testing OPA Login Rule for U role")
        data = {"user": {"clearance": "CONFIDENTIAL"}}
        self.assertTrue(client.check_policy_rule(data, "policy", "allow_login"))

        logging.debug("Testing OPA Login Rule for U role")
        data = {"user": {"clearance": "UNCLASSIFIED"}}
        self.assertTrue(client.check_policy_rule(data, "policy", "allow_login"))

    # doc auth test
    def test_doc_clearance_auth(self):
        logging.debug("Testing OPA doc clearance authorization")
        client = OPA()
        logging.debug("TS User")
        data = {"user": {"clearance_level": 3}, "doc": {"classification": 3}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        data = {"user": {"clearance_level": 3}, "doc": {"classification": 2}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        data = {"user": {"clearance_level": 3}, "doc": {"classification": 1}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        data = {"user": {"clearance_level": 3}, "doc": {"classification": 0}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        logging.debug("S User")
        data = {"user": {"clearance_level": 2}, "doc": {"classification": 3}}
        self.assertEquals(client.check_policy_rule(data, "policy", "clearance_auth"), {})
        data = {"user": {"clearance_level": 2}, "doc": {"classification": 2}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        data = {"user": {"clearance_level": 2}, "doc": {"classification": 1}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        data = {"user": {"clearance_level": 2}, "doc": {"classification": 0}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        logging.debug("C User")
        data = {"user": {"clearance_level": 1}, "doc": {"classification": 3}}
        self.assertEquals(client.check_policy_rule(data, "policy", "clearance_auth"), {})
        data = {"user": {"clearance_level": 1}, "doc": {"classification": 2}}
        self.assertEquals(client.check_policy_rule(data, "policy", "clearance_auth"), {})
        data = {"user": {"clearance_level": 1}, "doc": {"classification": 1}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        data = {"user": {"clearance_level": 1}, "doc": {"classification": 0}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))
        logging.debug("U User")
        data = {"user": {"clearance_level": 0}, "doc": {"classification": 3}}
        self.assertEquals(client.check_policy_rule(data, "policy", "clearance_auth"), {})
        data = {"user": {"clearance_level": 0}, "doc": {"classification": 2}}
        self.assertEquals(client.check_policy_rule(data, "policy", "clearance_auth"), {})
        data = {"user": {"clearance_level": 0}, "doc": {"classification": 1}}
        self.assertEquals(client.check_policy_rule(data, "policy", "clearance_auth"), {})
        data = {"user": {"clearance_level": 0}, "doc": {"classification": 0}}
        self.assertTrue(client.check_policy_rule(data, "policy", "clearance_auth"))

    def test_attr_auth(self):
        """test depends on current data structure i.e. sci1 id=1 ntk1 id=4 etc."""
        logging.debug("Testing OPA doc attr user authorization")
        client = OPA()
        logging.debug("TS User with sci1, ntk1")
        user_attributes = [1, 2, 4]
        doc_attr = [4, 1]
        for i in list(OrderedDict.fromkeys(doc_attr)):
            data = {"doc": {"access_attributes": i}, "user": {"access_attributes": user_attributes}}
            self.assertTrue(client.check_policy_rule(data=data, rule="attribute_auth"))
        doc_attr = [2, 1, 4]
        for i in list(OrderedDict.fromkeys(doc_attr)):
            data = {"doc": {"access_attributes": i}, "user": {"access_attributes": user_attributes}}
            self.assertTrue(client.check_policy_rule(data=data, rule="attribute_auth"))
        doc_attr = [2, 3, 4, 5]  # negative test
        for i in list(OrderedDict.fromkeys(doc_attr)):
            data = {"doc": {"access_attributes": i}, "user": {"access_attributes": user_attributes}}
            if i != 5 and i != 3:
                self.assertTrue(client.check_policy_rule(data=data, rule="attribute_auth"))
            else:
                self.assertEquals(client.check_policy_rule(data=data, rule="attribute_auth"), {})
        doc_attr = [6, 7]  # negative test
        for i in list(OrderedDict.fromkeys(doc_attr)):
            data = {"doc": {"access_attributes": i}, "user": {"access_attributes": user_attributes}}
            self.assertEquals(client.check_policy_rule(data=data, rule="attribute_auth"), {})
        doc_attr = [4, 1, 2, 3]  # negative test
        for i in list(OrderedDict.fromkeys(doc_attr)):
            data = {"doc": {"access_attributes": i}, "user": {"access_attributes": user_attributes}}
            if i != 3:
                self.assertTrue(client.check_policy_rule(data=data, rule="attribute_auth"))
            else:
                self.assertEquals(client.check_policy_rule(data=data, rule="attribute_auth"), {})
