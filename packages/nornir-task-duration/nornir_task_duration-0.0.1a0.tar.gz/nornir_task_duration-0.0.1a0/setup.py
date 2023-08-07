# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_task_duration',
 'nornir_task_duration.plugins',
 'nornir_task_duration.plugins.processors']

package_data = \
{'': ['*']}

install_requires = \
['nornir-utils>=0.2.0,<0.3.0', 'nornir>=3,<4']

setup_kwargs = {
    'name': 'nornir-task-duration',
    'version': '0.0.1a0',
    'description': 'Nornir processor plugin which calculates the duration of each task',
    'long_description': '# nornir_task_duration\n\n`Nornir processor plugin` which calculates the duration of each task\n\nThis plugin will store the duration of each task as attribute in the Nornir result objects.\n\n## Installation\n\n```bash\npip install nornir_task_duration\n```\n\n## Purpose\n\nThe plugin will add new class attributes to the Nornir results:\n\n- **total_duration**: this is the total duration to process all hosts, this is added to the AggregatedResult\n- **host_duration**: this is the totoal duration to process a single host, this is added to the host\'s MultiResult\n- **duration**: this is added to the Result of each task\n\n## Usage\n\nThis example shows the usage of the processor and an example how to print a summary. You may want to use the duration during the task execution or in another print plugin.\n\n```python\n\nfrom nornir import InitNornir\nfrom nornir.core.task import Result, Task, AggregatedResult, MultiResult\nfrom nornir_task_duration.plugins.processors import TaskDuration\n\nnr = InitNornir(\n    inventory={\n        "plugin": "YAMLInventory",\n        "options": {\n            "host_file": "tests/inventory/hosts.yaml",\n            "group_file": "tests/inventory/groups.yaml",\n            "defaults_file": "tests/inventory/defaults.yaml",\n        },\n    }\n)\n\nnrp = nr.with_processors([TaskDuration()])\n\nresults = nrp.run(task=some_task)\n\ndef printer(res):\n    if type(res) is AggregatedResult:\n        print(f"TOTAL DURATION:{res.total_duration}")\n        for r in res:\n            print(f" * HOST:{r} - DURATION:{res[r].host_duration}")\n            printer(res[r])\n    if type(res) is MultiResult:\n        for r in res:\n            printer(r)\n    if type(res) is Result:\n        print(f"  -- task:{res.name} - duration:{res.duration}")\n\nprinter(results)\n\n\n# TOTAL DURATION:12\n#   * HOST:test1 - DURATION:9\n#      -- task:ROOT-TASK - duration:9\n#      -- task:task1 - duration:4\n#      -- task:task2 - duration:3\n#      -- task:task2 - duration:3\n#   * HOST:test2 - DURATION:12\n#      -- task:ROOT-TASK - duration:12\n#      -- task:task1 - duration:4\n#      -- task:task2 - duration:3\n#      -- task:task2 - duration:3\n\n```\n',
    'author': 'Maarten Wallraf',
    'author_email': 'mwallraf@2nms.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
