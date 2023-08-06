# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_pyfgt',
 'nornir_pyfgt.plugins',
 'nornir_pyfgt.plugins.connections',
 'nornir_pyfgt.plugins.tasks']

package_data = \
{'': ['*']}

install_requires = \
['fortigate-api>=1.0.1,<2.0.0']

entry_points = \
{'nornir.plugins.connections': ['pyfgt = '
                                'nornir_pyfgt.plugins.connections:Pyfgt']}

setup_kwargs = {
    'name': 'nornir-pyfgt',
    'version': '1.0.0',
    'description': 'Fortigate-api plugin for Nornir',
    'long_description': '# Fortigate-Api for Nornir\n\n## Plugins\n\nConnections - fortigate-api\n\n## Description\n\n"This plugin integrates the fortigate-api library with the Nornir framework to simplify and automate configuration tasks on Fortigate devices. Using this plugin, you can easily create, delete, get, and update objects in the Fortigate using REST API and SSH. With commonly used objects already implemented, this plugin provides a powerful solution for managing your Fortigate network."\n\n## Installation\n\n```\npip install nornir-pyfgt\n```\n\n## Read the Documentation\n\nlink goes here\n\n## Usages\n\npyfgt get firewall addresses\n\n```python\nfrom nornir import InitNornir\nfrom nornir_pyfgt.plugins.tasks import pyfgt_address\nfrom nornir_utils.plugins.functions import print_result\n\nnr = InitNornir(\n    config_file="your/config/path"\n)\n\n\nresults = nr.run(task=pyfgt_address)\n\nprint_result(results)\n\n```\n\nresults\n\n```\nvvvv pyfgt_address ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO\n[ { \'allow-routing\': \'disable\',\n    \'associated-interface\': \'\',\n    \'cache-ttl\': 0,\n    \'clearpass-spt\': \'unknown\',\n    \'color\': 0,\n    \'comment\': \'\',\n    \'country\': \'\',\n    \'dirty\': \'dirty\',\n    \'fabric-object\': \'disable\',\n    \'filter\': \'\',\n    \'fsso-group\': [],\n    \'interface\': \'\',\n    \'list\': [],\n    \'macaddr\': [],\n    \'name\': \'DEMO\',\n    \'node-ip-only\': \'disable\',\n    \'obj-id\': \'\',\n    \'obj-type\': \'ip\',\n    \'q_origin_key\': \'ADDRESS\',\n    \'sdn\': \'\',\n    \'sdn-addr-type\': \'private\',\n    \'sub-type\': \'sdn\',\n    \'subnet\': \'10.10.10.10 255.255.255.0\',\n    \'tag-detection-level\': \'\',\n    \'tag-type\': \'\',\n    \'tagging\': [],\n    \'type\': \'ipmask\',\n    \'uuid\': \'0cdb9216-a648-51ed-b43f-238c3b127bc2\'},\n    ...\n^^^^ END pyfgt_address ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n```\n\npyfgt get custom URL - Check Fortigate API Documentation for API endpoints\n\n```python\nfrom nornir import InitNornir\nfrom nornir_utils.plugins.functions import print_result\nfrom nornir_pyfgt.plugins.tasks import pyfgt_get_url\n\n\nnr = InitNornir(\n    config_file="your/config/path"\n)\n\n\nresults = nr.run(task=pyfgt_get_url, url="/api/v2/cmdb/user/local")\n\nprint_result(results)\n\n```\n\nresults\n\n```\nvvvv pyfgt_get_url ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO\n[ { \'auth-concurrent-override\': \'disable\',\n    \'auth-concurrent-value\': 0,\n    \'authtimeout\': 0,\n    \'email-to\': \'\',\n    \'fortitoken\': \'\',\n    \'id\': 16777217,\n    \'ldap-server\': \'\',\n    \'name\': \'guest\',\n    \'passwd\': \'ENC XXXX\',\n    \'passwd-policy\': \'\',\n    \'passwd-time\': \'0000-00-00 00:00:00\',\n    \'ppk-identity\': \'\',\n    \'ppk-secret\': \'\',\n    \'q_origin_key\': \'guest\',\n    \'radius-server\': \'\',\n    \'sms-custom-server\': \'\',\n    \'sms-phone\': \'\',\n    \'sms-server\': \'fortiguard\',\n    \'status\': \'enable\',\n    \'tacacs+-server\': \'\',\n    \'two-factor\': \'disable\',\n    \'two-factor-authentication\': \'\',\n    \'two-factor-notification\': \'\',\n    \'type\': \'password\',\n    \'username-sensitivity\': \'enable\',\n    \'workstation\': \'\'}]\n^^^^ END pyfgt_get_url^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n```\n\npyfgt send SSH command\n\n```python\nfrom nornir import InitNornir\nfrom nornir_utils.plugins.functions import print_result\nfrom nornir_pyfgt.plugins.tasks import pyfgt_send_command\n\n\nnr = InitNornir(\n    config_file="your/config/path"\n)\n\n\nresults = nr.run(task=pyfgt_send_command, command="get system interface")\n\nprint_result(results)\n\n```\n\nresults\n\n```\nvvvv pyfgt_send_command ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO\n== [ port1 ]\nname: port1   mode: dhcp    ip: 192.168.0.158 255.255.255.0   status: up    netbios-forward: disable    type: physical   ring-rx: 0   ring-tx: 0   netflow-sampler: disable    sflow-sampler: disable    src-check: enable    explicit-web-proxy: disable    explicit-ftp-proxy: disable    proxy-captive-portal: disable    mtu-override: disable    wccp: disable    drop-overlapped-fragment: disable    drop-fragment: disable\n== [ port2 ]\nname: port2   mode: static    ip: 0.0.0.0 0.0.0.0   status: up    netbios-forward: disable    type: physical   ring-rx: 0   ring-tx: 0   netflow-sampler: disable    sflow-sampler: disable    src-check: enable    explicit-web-proxy: disable    explicit-ftp-proxy: disable    proxy-captive-portal: disable    mtu-override: disable    wccp: disable    drop-overlapped-fragment: disable    drop-fragment: disable\n...\n^^^^ END pyfgt_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n```\n',
    'author': 'GT',
    'author_email': 'geuryt@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
