from simple_salesforce import Salesforce
import datetime
from copy import deepcopy

class SalesforceSession:
    """
    Wrapper around simple_salesforce with better session handling.
    """

    def __init__(self, username, consumer_key=None, privatekey=None, password=None, token=None, domain=None):
        self.username = username
        self.consumer_key = consumer_key
        self.privatekey = privatekey
        self.password = password
        self.token = token
        self.domain = domain
        self.session = None
        self.db_conn = None
        self.last_active = None
        self.login()

    def login(self):
        if self.token is None:
            self.session = Salesforce(
                username=self.username, consumer_key=self.consumer_key, privatekey=self.privatekey, domain=self.domain
            )
        else:
            self.session = Salesforce(
                username=self.username, password=self.password, security_token=self.token, domain=self.domain
            )
        self.last_active = datetime.datetime.now(datetime.timezone.utc)

    def get_session(self):
        # First check if there is a valid session, if not, create a new one
        # Return a copy of the session so we can use it in multiple threads
        if self.last_active is None or self.last_active < datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2):
            self.login()
        self.last_active = datetime.datetime.now(datetime.timezone.utc)
        return deepcopy(self.session)

def check_logins_last_hour(sf, user_id):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = datetime.timedelta(hours=1)
    prev_hour = now - diff
    prev_hour = prev_hour.isoformat()
    return f"[{now}] Logins since {prev_hour}: " + str(sf.query(f"SELECT COUNT() from LoginHistory WHERE UserId = '{user_id}' AND LoginTime > {prev_hour}")['totalSize'])