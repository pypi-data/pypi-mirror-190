# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['store_validations_oracle']

package_data = \
{'': ['*']}

install_requires = \
['flatten-json>=0.1.13,<0.2.0',
 'great-expectations>=0.15.41,<0.16.0',
 'oracledb>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'store-validations-oracle',
    'version': '0.1.4',
    'description': 'Used with Great_Expectations to store validation results in an Oracle Database.',
    'long_description': "\n# ge-store-validations-oracle-plugin\n\n## Steps to use the OracleStoreValidationResultsAction from the plugin\n\nInstall this plugin by pasting store_validations_oracle.py from great_expectations/plugins in your corresponding great_expectations/plugins folder.\n\n1. Install the plugin by `pip install store-validations-oracle`. You can put `store-validations-oracle` in the requirements.txt file for CI/CD operations.\n\n2. In your required `checkpoint`, add the following action to your checkpoint `.yml` file.\n\n```yml\n  - name: store_validations_oracle\n    action:\n      class_name: OracleStoreValidationResultsAction\n      module_name: store_validations_oracle.store_validations_oracle\n      username: ${USERNAME}\n      password: ${PASSWORD}\n      hostname: ${HOSTNAME}\n      port: ${PORT}\n      service_name: ${SERVICE_NAME}\n      table_name: ${TABLE_NAME}\n```\n\n3. In your uncommited/config_variables.yml file or if you are using environment variables, add the following variables related to the Oracle Database account:\n\n    * USERNAME\n    * PASSWORD\n    * TABLE_NAME\n\n    Either:\n\n    * HOSTNAME\n    * PORT (defaults to 1521)\n    * SERVICE_NAME (defaults to ORCL)\n\n    Or:\n\n    * CONNECTION_STRING\n\n\n4. If you already have a given table in oracledb, make sure table has below schema.( If you don't have table script will create one , with required schema. )\n\n  ```sql\n  CREATE TABLE TABLE1 \n(\n  BATCH_KEY VARCHAR2(100) NOT NULL \n, META CLOB \n, EVALUATION_PARAMETERS CLOB \n, STATISTICS CLOB \n, SUCCESS VARCHAR2(10) \n, RESULT CLOB \n);\n  ```\n",
    'author': 'Ali Bhayani',
    'author_email': 'ali@cloudshuttle.com.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
