import requests
import json
from base64 import b64encode
# from neutron_lib.exceptions import dns as dns_exc
from oslo_config import cfg

from neutron._i18n import _

from neutron.services.externaldns import driver

CONF = cfg.CONF

solidserver_opts = [
    cfg.StrOpt('url',
               help=_('SOLIDServer REST API endpoint')),
    cfg.StrOpt('space',
               help=_('The name of the space into \
                      which creating the IP addresses')),
    cfg.StrOpt('user',
               help=_('Username used to establish the connection.')),
    cfg.StrOpt('password',
               help=_('Password associated with the username.')),

]

solidserver_group = cfg.OptGroup(name='solidserver',
                                 title='EfficientIP SolidServer options')
CONF.register_group(solidserver_group)
CONF.register_opts(solidserver_opts, group='solidserver')


class SolidServer(driver.ExternalDNSService):
    """Driver for SolidServer."""

    def __init__(self):
        """Initialize external dns service driver."""
        print('External DNS Efficient IP init')
        print(CONF.solidserver.url)
        self.headers = {'X-IPM-Username': b64encode(CONF.solidserver.user),
                        'X-IPM-Password': b64encode(CONF.solidserver.password)}

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
        print('External DNS EfficientIP')
        print(records)
        payload = {'site_name': CONF.solidserver.space,
                   'ip_name': '{}.{}'.format(dns_name, dns_domain),
                   'hostaddr': records[0],
                   'add_flag': 'new_only'}
        r = requests.post(CONF.solidserver.url+'ip_add', headers=self.headers,
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
        print('External DNS EfficientIP')
        print(records)
        payload = {'site_name': CONF.solidserver.space,
                   'ip_name': '{}.{}'.format(dns_name, dns_domain),
                   'hostaddr': records[0]}
        r = requests.delete(CONF.solidserver.url+'ip_delete',
                            headers=self.headers,
                            params=payload)
        print(r)
