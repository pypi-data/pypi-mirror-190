# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamodb_python']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.65,<2.0.0',
 'botocore>=1.29.65,<2.0.0',
 'ddbcereal>=2.1.1,<3.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'dynamodb-python',
    'version': '0.1.2',
    'description': '',
    'long_description': '# dynamodb-python\n\n## Installation\n\n## Requirements\n\n### Dependencies\n\n- python = "^3.9"\n- ddbcereal\n- botocore\n- boto3\n- requests\n\n### Credentials\n\nYou will first need to set your AWS credentials. Since this library uses `boto3` under the hood, you can use the same methods as described in the [boto3 documentation](https://boto3.readthedocs.io/en/latest/guide/configuration.html). In short, AWS looks for credentials in these places:\n\n1. Environment variables\n2. Shared credentials file (`~/.aws/credentials`)\n3. AWS config file (`~/.aws/config`)\n\nYou cacn also pass a dictionary to `DynamoDB` class:\n\n```python\nfrom dynamodb_python import DynamoDB\n\ndynamodb = DynamoDB(credentials={\n    "aws_access_key_id": ACCESS_KEY,\n    "aws_secret_access_key": SECRET_KEY,\n    "aws_session_token": SESSION_TOKEN\n})\n```\n\n## How to use\n\nHaving a table called `table_name`, you can access it like this:\n\n```python\nfrom dynamodb_python import DynamoDB\n\ndynamodb = DynamoDB()\ntable = dynamodb.table_name\n```\n\nAnd then you can get an item like this:\n\n```python\ntable.read_item(key={"partition_key": "key", "sort_key": "sort_key" })  # NOTE that sort_key is optional\n```\n\nOr you can get a list of items with the same key like this:\n\n```python\ntable.read_items(key={"partition_key": "key"})  # NOTE that you can also pass in boto3 condition key \n```\n\nOr you can write an item like this:\n\n```python\ntable.write(key={"partition_key": "key", "sort_key": "sort_key"}, data={"data": "data"})\n```\n',
    'author': 'domas-v',
    'author_email': 'domas.vaitmonas93@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
