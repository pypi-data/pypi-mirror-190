# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysungrow',
 'pysungrow.definitions',
 'pysungrow.definitions.devices',
 'pysungrow.definitions.variables',
 'pysungrow.lib']

package_data = \
{'': ['*']}

install_requires = \
['pymodbus>=2.5.3']

setup_kwargs = {
    'name': 'pysungrow',
    'version': '1.1.0',
    'description': 'Read and manipulate Sungrow inverters',
    'long_description': '# pysungrow - Python interface to Sungrow inverters\n\n![PyPI](https://img.shields.io/pypi/v/pysungrow)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysungrow)\n![PyPI - Status](https://img.shields.io/pypi/status/pysungrow)\n![GitHub](https://img.shields.io/github/license/02jandal/pysungrow)\n[![CI](https://github.com/02JanDal/pysungrow/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/02JanDal/pysungrow/actions/workflows/ci.yaml)\n\nThis Python package provides abstractions over the Modbus protocol used by inverters of the brand Sungrow.\n\n## Features\n\n- Both getting and setting data\n- Fully async\n- Fully typed\n- Supports most forms of Modbus (TCP, UDP, TLS and Serial)\n- (Theoretically) supports most Sungrow inverters, both string and hybrid\n- High test coverage\n\n## Supported inverters\n\n**Tested:** SH10RT\n\n**In theory:** SG60KTL, SG60KU, SG33KTL-M, SG36KTL-M, SG40KTL-M, SG50KTL-M, SG60KTL-M, SG60KU-M, SG49K5J, SG8KTL-M, SG10KTL-M, SG12KTL-M, SG80KTL, SG80KTL-M, SG80HV, SG125HV, SH5K-20, SH3K6, SH4K6, SH5K-V13, SH5K-30, SH3K6-30, SH4K6-30, SH5.0RS, SH3.6RS, SH4.6RS, SH6.0RS, SH8.0RT, SH6.0RT, SH5.0RT\n\nDo you have an inverter that\'s not been tested yet? Please follow the instructions under _Getting started_ including running the `get` command, and report the result in a [new issue](https://github.com/02JanDal/pysungrow/issues/new).\n\n## Getting started\n\nInstall using `pip`:\n\n```bash\npip install pysungrow\n```\n\nSee below for usaging from Python. Also comes with a simple command line interface:\n\n```\npysungrow [-p PORT] [-s SLAVE] [HOST] identify\npysungrow [-p PORT] [-s SLAVE] [HOST] get [-k KEY]\npysungrow [-p PORT] [-s SLAVE] [HOST] set [KEY] [VALUE]\n```\n\nIt is recommended to start using these commands to verify that you can connect to your inverter successfully.\n\n## Usage\n\n### Getting data from the inverter\n\n```python\nfrom pysungrow import identify, SungrowClient\nfrom pymodbus.client import AsyncModbusTcpClient\n\nasync def example_get():\n    modbus_client = AsyncModbusTcpClient("192.168.1.228")\n\n    # first we need to identify the model of inverter...\n    serial_number, device, output_type = await identify(modbus_client)\n\n    # ...then we can create a client...\n    client = SungrowClient(modbus_client, device, output_type)\n\n    # ...using which we can get data\n    return await client.get("total_dc_power")\n```\n\nNote that the first call to `client.get` will fetch all variables defined for your model of inverter. You can limit this by first manually triggering a fetch using `await client.refresh(["total_dc_power"])`.\n\n### Controlling the inverter\n\n```python\nfrom pysungrow import identify, SungrowClient\nfrom pysungrow.definitions.variables.hybrid import ChargeDischargeCommand\nfrom pymodbus.client import AsyncModbusTcpClient\n\nasync def example_set():\n    modbus_client = AsyncModbusTcpClient("192.168.1.228")\n\n    # first we need to identify the model of inverter...\n    serial_number, device, output_type = await identify(modbus_client)\n\n    # ...then we can create a client...\n    client = SungrowClient(modbus_client, device, output_type)\n\n    # ...using which we can control the inverter\n    await client.set("charge_discharge_command", ChargeDischargeCommand.CHARGE)\n```\n\n## Contributing\n\nContributions are always welcome!\n\nFor code contributions please make sure that all automated checks pass. The easiest way to do this is using these commands:\n\n```bash\npre-commit run --all-files\npytest\n```\n## Acknowledgements\n\nThere are a few other similar projects available (however neither of them fit my needs):\n\n - [SungrowInverter](https://github.com/mvandersteen/SungrowInverter) by @mvandersteen\n - [HomeAssistant Modbus mappings](https://github.com/mkaiser/Sungrow-SHx-Inverter-Modbus-Home-Assistant) by @mkaiser\n - [sungrow-websocket](https://github.com/wallento/sungrow-websocket) by @wallento\n \n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Jan Dalheimer',
    'author_email': 'jan@dalheimer.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/02JanDal/pysungrow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
