# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiolxd', 'aiolxd.api', 'aiolxd.entities']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8,<4.0', 'pydantic>=1.10,<2.0']

setup_kwargs = {
    'name': 'aiolxd',
    'version': '0.1.1',
    'description': 'AsyncIO LXD API for Python 3',
    'long_description': '# aiolxd\n\nWIP AsyncIO LXD API for Python 3.\n\n## **THIS PROJECT IS NOT READY FOR PRODUCTION USE**\n\n## Example\n\n```python\nimport asyncio\n\nfrom aiolxd import LXD\n\n\nasync def main() -> None:\n    async with LXD.with_async("https://localhost:8443", cert=("client.crt", "client.key")) as lxd:\n        create_task = await lxd.instance.create(\n            name="test-instance", source="ubuntu/22.04", type_="virtual-machine"\n        )  # Request the creation of an instance\n        await create_task.wait()  # Wait for the task to complete\n\n        print(await lxd.instance.get("test-instance"))\n        # architecture=\'x86_64\' created_at=\'2023-02-07T13:05:12.631550731Z\'\n        # last_used_at=\'1970-01-01T00:00:00Z\' location=\'none\' name=\'test-instance\'\n        # profiles=[\'default\'] project=\'default\' restore=None stateful=False\n        # status=\'Stopped\' status_code=102 type=\'virtual-machine\' description=\'\'\n        # devices={} ephemeral=False config=InstanceConfig(security_nesting=None)\n\n        delete_task = await lxd.instance.delete("test-instance")  # Request the deletion of an instance\n        await delete_task.wait()  # Wait for the task to complete\n\n\nasyncio.run(main())\n```\n\n## TODO\n\n- [x] Basic API (instance creation, deletion, etc.)\n- [x] Logging\n- [ ] Websocket operation events (websocket support exists, but events are not parsed)\n- [ ] Tests\n- [ ] More API endpoints\n',
    'author': 'Egor Ternovoy',
    'author_email': 'cofob@riseup.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cofob/aiolxd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
