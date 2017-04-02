import logging
import os
import xmlrpc.client

logger = logging.getLogger('webfaction.api')


class WebFactionAPI:
    def __init__(self,
                 machine_name=None,  # not required if you have only one machine
                 username=None, password=None,
                 ):
        super().__init__()

        if username is None:
            username = os.environ.get("WEBFACTION_USER")
        if password is None:
            password = os.environ.get("WEBFACTION_PASS")
        if machine_name is None:
            # for the API, when we have more machines, we have to select the machine name
            machine_name = os.environ.get("WEBFACTION_MACHINE_NAME", "")  # empty string as default

        if not username or not password:
            logger.error("Please set the webfaction username and password to connect")
            logger.error("They can be set WEBFACTION_USER and WEBFACTION_PASS variables")
            exit(1)

        self.username = username
        self.password = password
        self.machine_name = machine_name
        self.server = xmlrpc.client.ServerProxy('https://api.webfaction.com/')
        self.session_id = self.account = None

    def connect(self):
        if not self.session_id:
            logger.debug("Connecting to API server")
            api_version = 2
            self.session_id, self.account = self.server.login(self.username, self.password,
                                                              self.machine_name,
                                                              api_version)

    def list_apps(self):
        self.connect()
        results = self.server.list_apps(self.session_id)
        return {a['name']: a for a in results}  # return apps keyed by id

    def create_app(self, app_name, app_type, autostart=False,
                   extra_info="", open_port=False):
        self.connect()
        app = self.server.create_app(self.session_id,
                                     app_name, app_type,
                                     autostart, extra_info, open_port
                                     )
        return app

    def create_domain(self, domain, subdomains=None):
        self.connect()
        if subdomains is None:
            subdomains = []

        domain = self.server.create_domain(self.session_id,
                                           domain,
                                           *subdomains
                                           )
        return domain

    def list_domains(self):
        """ Return all domains. Domain is a key, so group by them """
        self.connect()
        results = self.server.list_domains(self.session_id)
        return {i['domain']: i['subdomains'] for i in results}

    def list_websites(self):
        """ Return all websites, name is not a key """
        self.connect()
        results = self.server.list_websites(self.session_id)

        return results

    def list_certificates(self):
        self.connect()
        results = self.server.list_certificates(self.session_id)

        return {i['name']: i for i in results}

    def create_certificate(self, certificate):
        self.connect()
        certificate = self.server.create_certificate(
            self.session_id,
            certificate['name'],
            certificate['certificate'],
            certificate['private_key'],
            certificate['intermediates'],
        )
        return certificate

    def update_certificate(self, certificate):
        self.connect()
        certificate = self.server.update_certificate(
            self.session_id,
            certificate['name'],
            certificate['certificate'],
            certificate['private_key'],
            certificate['intermediates'],
        )
        return certificate

    def list_ips(self):
        self.connect()
        return self.server.list_ips(self.session_id)

    def main_ip(self):
        ips = self.list_ips()
        return list(filter(lambda x: x['is_main'], ips))[0]['ip']  # one should be main

    def create_website(self, website_name, ip, enable_https, subdomains, certificate="", apps=()):
        self.connect()
        self.server.create_website(self.session_id,
                                   website_name, ip, enable_https, subdomains,
                                   certificate,
                                   *apps)

    def update_website(self, website):
        self.connect()
        website = self.server.update_website(
            self.session_id,
            website['name'],
            website['ip'],
            website['https'],
            website['subdomains'],
            website['certificate'],
            *website['website_apps']
        )
        return website

    def website_exists(self, website, websites=None):
        """ Look for websites matching the one passed """
        if websites is None:
            websites = self.list_websites()
        if isinstance(website, str):
            website = {"name": website}
        ignored_fields = ('id',)  # changes in these fields are ignored

        results = []
        for other in websites:
            different = False
            for key in website:
                if key in ignored_fields:
                    continue
                if other.get(key) != website.get(key):
                    different = True
                    break
            if different is False:
                results.append(other)
        return results
