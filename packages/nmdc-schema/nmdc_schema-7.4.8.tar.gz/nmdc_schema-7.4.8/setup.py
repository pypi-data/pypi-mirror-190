# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nmdc_schema']

package_data = \
{'': ['*']}

install_requires = \
['linkml-runtime>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['fetch-nmdc-schema = '
                     'nmdc_schema.nmdc_data:get_nmdc_jsonschema',
                     'generate_import_slots_regardless = '
                     'nmdc_schema.generate_import_slots_regardless:main',
                     'get_mixs_slots_matching_slot_list = '
                     'nmdc_schema.get_mixs_slots_matching_slot_list:main',
                     'get_mixs_slots_used_in_schema = '
                     'nmdc_schema.get_mixs_slots_used_in_schema:main',
                     'get_slots_from_class = '
                     'nmdc_schema.get_slots_from_class:main',
                     'minimal_get_submissions = '
                     'nmdc_schema.minimal_get_submissions:cli',
                     'mixs_deep_diff = nmdc_schema.mixs_deep_diff:cli',
                     'mixs_slot_text_mining = '
                     'nmdc_schema.mixs_slot_text_mining:cli',
                     'nmdc-data = nmdc_schema.nmdc_data:cli',
                     'nmdc-version = nmdc_schema.nmdc_version:cli',
                     'slot_roster = nmdc_schema.slot_roster:cli']}

setup_kwargs = {
    'name': 'nmdc-schema',
    'version': '7.4.8',
    'description': 'Schema resources for the National Microbiome Data Collaborative (NMDC)',
    'long_description': '<p align="center">\n    <img src="images/nmdc_logo_long.jpeg" width="100" height="40"/>\n</p>\n\n# National Microbiome Data Collaborative Schema\n\n[![PyPI - License](https://img.shields.io/pypi/l/nmdc-schema)](https://github.com/microbiomedata/nmdc-schema/blob/main/LICENSE)\n[![PyPI version](https://badge.fury.io/py/nmdc-schema.svg)](https://badge.fury.io/py/nmdc-schema)\n\nThe NMDC is a multi-organizational effort to integrate microbiome data across diverse areas in medicine, agriculture,\nbioenergy, and the environment. This integrated platform facilitates comprehensive discovery of and access to\nmultidisciplinary microbiome data in order to unlock new possibilities with microbiome data science.\n\nThis repository mainly defines a [LinkML](https://github.com/linkml/linkml) schema for managing metadata from\nthe [National Microbiome Data Collaborative (NMDC)](https://microbiomedata.org/).\n\n## Repository Contents Overview\n\nSome products that are maintained, and tasks orchestrated within this repository are:\n\n- Maintenance of LinkML YAML that specifies the NMDC Schema\n    - [src/schema/nmdc.yaml](src/schema/nmdc.yaml)\n    - and various other YAML schemas imported by it,\n      like [prov.yaml](src/schema/prov.yaml), [annotation.yaml](src/schema/annotation.yaml), etc. all which you can find\n      in the [src/schema](src/schema/) folder\n- Makefile targets for converting the schema from it\'s native LinkML YAML format to other artifact\n  like [JSON Schema](project/jsonschema/nmdc.schema.json)\n- Build, deployment and distribution of the schema as a PyPI package\n- Automatic publishing of refreshed documentation upon change to the schema,\n  accessible [here](https://microbiomedata.github.io/nmdc-schema/)\n\n## Background\n\nThe NMDC [Introduction to metadata and ontologies](https://microbiomedata.org/introduction-to-metadata-and-ontologies/)\nprimer provides some the context for this project.\n\n## Maintaining the Schema\n\n**New system requirement: [Mike Farah\'s GO-based yq](https://github.com/mikefarah/yq)**\n\nSee [MAINTAINERS.md](MAINTAINERS.md) for instructions on maintaining and updating the schema.\n',
    'author': 'Bill Duncan',
    'author_email': 'wdduncan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://microbiomedata.github.io/nmdc-schema/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
