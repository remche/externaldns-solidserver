# External DNS driver for EfficientIP SolidServer

This project allow you to register VM port or floating IP in an EfficientIP SolidServer IPAM using [Neutron DNS integration with an external service](https://docs.openstack.org/neutron/rocky/admin/config-dns-int-ext-serv.html)

## Installation

Via pip :

```bash
pip install externaldns-solidserver
```

## Configuration

Add following lines to neutron.conf :

```ini
[solidserver]
url = http://solidserver_url/rest/
space = solidserver_space
user = solidserver_user
password = soliserver_password

[default]
external_dns_driver = solidserver
```

Restart **neutron_server**. Check use cases on [Neutron documentation](https://docs.openstack.org/neutron/rocky/admin/config-dns-int-ext-serv.html).




