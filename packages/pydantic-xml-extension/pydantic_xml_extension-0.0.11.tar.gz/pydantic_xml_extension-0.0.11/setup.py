# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_xml']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'pydantic-xml-extension',
    'version': '0.0.11',
    'description': '',
    'long_description': '# Pydantic XML Extension\n\nAllows Pydantic models to render to XML.\n\n## Install\n\n`pip install pydantic-xml-extension`\n\n## Examples\n\n### Generating XML from a model\n```python\nfrom pydantic_xml import XmlBaseModel, XmlAttribute\n\nclass ExampleModel(XmlBaseModel):\n    name: Annotated[str, fields.Field(alias="Name")]\n    age: int\n\nmodel = ExampleModel(Name="test", age=12)\nmodel.set_xml_attribute("name", XmlAttribute(key="id", value="123"))\nmodel.set_xml_attribute("age", XmlAttribute(key="custom", value="value"))\nprint(model.xml())\n>> <?xml version="1.0" encoding="utf-8"?>\n>> <Model><Name id="123">test</Name><age custom="value">12</age></Model>\n```\n\n### Creating a model from XML\n```python\nfrom pydantic_xml import XmlBaseModel, XmlAttribute\n\nclass ExampleModel(XmlBaseModel):\n    name: Annotated[str, fields.Field(alias="Name")]\n    age: int\n\ninput_xml = \'<Model><Name id="123">test</Name><age custom="value">12</age></Model>\'\n\nmodel = ExampleModel.parse_xml(input_xml)\n\nprint(model)\n>> Model(name="test", age=12)\n\nprint(model.dict())\n>> {"Name": "test", "age": 12}\n\nprint(model.dict(by_alias=False))\n>> {"name": "test", "age": 12}\n\nprint(model.xml())\n>> <?xml version="1.0" encoding="utf-8"?>\n>> <Model><Name id="123">test</Name><age custom="value">12</age></Model>\n```\n',
    'author': 'Patrick Withams',
    'author_email': 'pwithams@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwithams/pydantic-xml-extension',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
