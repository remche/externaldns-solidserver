import requests
import json
from base64 import b64encode
# from neutron_lib import constants
# from neutron_lib.exceptions import dns as dns_exc
# from oslo_config import cfg
import cfg as CONF

# from neutron.services.externaldns import driver


# class Designate(driver.ExternalDNSService):
class Designate():
    """Driver for Designate."""

    def __init__(self):
        """Initialize external dns service driver."""
        self.headers = {'X-IPM-Username': b64encode(CONF.SOLIDSERVER_user),
                        'X-IPM-Password': b64encode(CONF.SOLIDSERVER_password)}

    def create_record_set(self, context, dns_domain, dns_name, records):
        """Create a record set in the specified zone.
        :param context: neutron api request context
        :type context: neutron_lib.context.Context
        :param dns_domain: the dns_domain where the record set will be created
        :type dns_domain: String
        :param dns_name: the name associated with the record set
        :type dns_name: String
        :param records: the records in the set
        :type records: List of Strings
        :raises: neutron.extensions.dns.DNSDomainNotFound
                 neutron.extensions.dns.DuplicateRecordSet
        """
        payload = {'site_name': CONF.SOLIDSERVER_site,
                   'ip_name': '{}.{}'.format(dns_name, dns_domain),
                   'hostaddr': records[0],
                   'add_flag': 'new_only'}
        r = requests.post(CONF.SOLIDSERVER_url+'ip_add', headers=self.headers,
                          data=json.dumps(payload))
        print(r)

    def delete_record_set(self, context, dns_domain, dns_name, records):
        """Delete a record set in the specified zone.
        :param context: neutron api request context
        :type context: neutron.context.Context
        :param dns_domain: the dns_domain from which the record set will be
         deleted
        :type dns_domain: String
        :param dns_name: the dns_name associated with the record set to be
         deleted
        :type dns_name: String
        :param records: the records in the set to be deleted
        :type records: List of Strings
        """
        payload = {'site_name': CONF.SOLIDSERVER_site,
                   'ip_name': '{}.{}'.format(dns_name, dns_domain),
                   'hostaddr': records[0]}
        r = requests.delete(CONF.SOLIDSERVER_url+'ip_delete',
                            headers=self.headers,
                            params=payload)
        print(r)
