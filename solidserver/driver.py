# -*- coding: utf-8 -*-
import requests
import json
from base64 import b64encode

from neutron_lib.exceptions import dns as dns_exc
from oslo_config import cfg
from oslo_log import log
from neutron._i18n import _
from neutron.services.externaldns import driver


LOG = log.getLogger(__name__)

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
        LOG.debug('Init SolidServer external DNS to work with ' +
                  CONF.solidserver.url)
        self.headers = {'X-IPM-Username':
                        b64encode(CONF.solidserver.user.encode("utf-8")),
                        'X-IPM-Password':
                        b64encode(CONF.solidserver.password.encode("utf-8"))}

    def check_domain(self, dns_domain):
        LOG.debug('Checking {} zone'.format(dns_domain))
        url = '{}dns_zone_list/WHERE/dnszone_name=\'{}\''.format(
            CONF.solidserver.url, dns_domain.rstrip('.'))
        try:
            r = requests.get(url, headers=self.headers)
        except:
            LOG.error('Something was terribly wrong')
        if r.status_code != 200:
            raise dns_exc.DNSDomainNotFound(dns_domain=dns_domain)

    def check_name(self, ip_name):
        LOG.debug('Checking {} name'.format(ip_name))
        url = '{}ip_address_list/WHERE/name=\'{}\''.format(
            CONF.solidserver.url, ip_name)
        try:
            r = requests.get(url, headers=self.headers)
        except:
            LOG.error('Something was terribly wrong')
        if r.status_code != 204:
            raise dns_exc.DuplicateRecordSet(dns_name=ip_name)

    def create_record_set(self, context, dns_domain, dns_name, records):
        ip_name = '{}.{}'.format(dns_name, dns_domain.rstrip('.'))
        LOG.debug('Adding record {} to {}'.format(ip_name, records[0]))
        self.check_domain(dns_domain)
        self.check_name(ip_name)
        payload = {'site_name': CONF.solidserver.space,
                   'ip_name': ip_name,
                   'hostaddr': records[0],
                   'add_flag': 'new_only'}
        r = requests.post(CONF.solidserver.url+'ip_add', headers=self.headers,
                          data=json.dumps(payload))
        if r.status_code != 201:
            raise dns_exc.BadRequest(resource='SolidServer', msg=r.reason)
        LOG.debug('Solidserver response :' + r.content)

    def delete_record_set(self, context, dns_domain, dns_name, records):
        LOG.debug('Removing record {} to SolidServer'.format(records[0]))
        payload = {'site_name': CONF.solidserver.space,
                   'ip_name': '{}.{}'.format(dns_name, dns_domain.rstrip('.')),
                   'hostaddr': records[0]}
        try:
            r = requests.delete(CONF.solidserver.url+'ip_delete',
                                headers=self.headers,
                                params=payload)
        except:
            LOG.error('Something was terribly wrong')
        LOG.debug('Solidserver response :' + r.content)
