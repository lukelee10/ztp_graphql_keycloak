import logging
import os
from opa_client.opa import OpaClient
from dotenv import load_dotenv
from pathlib import Path
from typing import List
from django.db.models.query import QuerySet
from apps.data_tables.models import AccessAttribute, Classification
from apps.users.models import User
from opa_client.opa import OpaClient
from apps.data_tables.models import AccessAttribute
from apps.users.models import User

log = logging.getLogger("main")


dot_path = Path(".env")
load_dotenv(dotenv_path=dot_path)


class OPA(object):
    """OPA class to query OPA"""

    def __init__(self):
        self.addr = os.environ.get("OPA_ADDR")
        self.port = int(os.environ.get("OPA_PORT"))
        self.version = os.environ.get("VERSION")
        self.ssl = os.environ.get("SSL")
        self.certs = os.environ.get("CERTS")
        self.headers = os.environ.get("HEADERS")
        self.client = OpaClient(self.addr, self.port, self.version)

    def checkin(self):
        """OPA health check returns boolean"""
        val = False
        try:
            val = self.client.check_health()
        except Exception as e:
            log.critical("Failed to connect to OPA: {}".format(e))
        return val

    def check_policy_rule(self, data, path="policy", rule="allow_login"):
        """OPA policy rule check returns boolean no need for input in data"""
        val = False
        try:
            val = self.client.check_policy_rule(data, package_path=path, rule_name=rule)
        except Exception as e:
            log.critical("Failed to connect to OPA: {}".format(e))

        return val

    def verify_user_clearance(self, clearance: Classification):
        """verify user has valid clearance
        returns boolean"""
        try:
            data = {"user": {"clearance": clearance.name}}
            log.info("Validating user clearance {}".format(data))
            if not self.check_policy_rule(data=data):
                log.critical("Failed to verify user clearance: {}".format(data))
                return False
        except Exception as e:
            log.error("Unable to verify user clearance: {}".format(e.with_traceback))
            return False
        log.info("Clearance validated")
        return True

    def user_doc_auth(self, clearance: Classification, doc_class_list: QuerySet[int]):
        """verify user is auth to see doc
        returns boolean"""
        try:
            log.debug("Doc classification list: {}".format(doc_class_list))
            for doc_class in doc_class_list.distinct():  # doing per doc class to handle individual rec
                if doc_class is not None:
                    data = {"user": {"clearance_level": clearance.level}, "doc": {"classification": doc_class}}
                    log.info("Validating user clearance authorization to view doc. Data: {}".format(data))
                    if not self.check_policy_rule(data=data, rule="clearance_auth"):
                        log.critical("Failed to verify user doc authorization: {}".format(data))
                        return False
                    else:
                        log.info("Access authorized: {}".format(data))
        except Exception as e:
            log.error(
                "Unable to verify user clearance level auth to view doc with classification: {}".format(
                    e.with_traceback
                )
            )
            return False
        # log.info("Clearance level valid and authorized")
        return True

    def verify_attribute_access(self, user: User, doc_attr: QuerySet[int]):
        """verify users attributes with doc attributes
        returns boolean"""
        try:
            # iterate through each doc attr
            log.debug("in verify_attribute_access")
            for attribute in doc_attr.distinct():
                if attribute is not None:
                    data = {
                        "doc": {"access_attributes": attribute},
                        "user": {"access_attributes": list(user.access_attributes.all().values_list("id", flat=True))},
                    }
                    log.info("Validating user attributes against doc attributes {}".format(data))
                    if not self.check_policy_rule(data=data, rule="attribute_auth"):
                        log.critical("Attribute(s) verification failed. Data: {}".format(data))
                        return False
                    else:
                        log.info("Access authorized: {}".format(data))
        except Exception as e:
            log.critical("Failed to validate attributes with OPA: {}".format(e))
            return False
        # log.info("User attributes valid and authorized. ")
        return True
