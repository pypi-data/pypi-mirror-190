# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_xml']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'pydantic-xml-converter',
    'version': '0.0.13',
    'description': '',
    'long_description': '# Pydantic XML Converter\n\nAllows existing Pydantic models to be converted to/from XML with support for XML attributes.\n\n## Install\n\n`pip install pydantic-xml-extension`\n\n## Examples\n\n### Generating XML from an existing Pydantic model\n```python\nfrom pydantic import fields, BaseModel\nfrom pydantic_xml import PydanticXmlConverter, XmlAttribute\n\nclass CustomBaseModel(BaseModel):\n    class Config:\n        allow_population_by_field_name = True\n        \nclass ExistingModel(CustomBaseModel):\n    name: Annotated[str, fields.Field(alias="Name")]\n    age: int\n\nmodel = ExistingModel(Name="test", age=12)\nconverter = PydanticXmlConverter("Model")\nconverter.set_xml_attribute("name", XmlAttribute(key="id", value="123"))\nconverter.set_xml_attribute("age", XmlAttribute(key="custom", value="value"))\nprint(converter.xml(model))\n>> <?xml version="1.0" encoding="utf-8"?>\n>> <Model><Name id="123">test</Name><age custom="value">12</age></Model>\n```\n\n### Creating an instance of an existing Pydantic model from XML\n```python\nfrom pydantic_xml import XmlBaseModel, XmlAttribute\n\nclass CustomBaseModel(BaseModel):\n    class Config:\n        allow_population_by_field_name = True\n\nclass ExistingModel(XmlBaseModel):\n    name: Annotated[str, fields.Field(alias="Name")]\n    age: int\n\ninput_xml = \'<Model><Name id="123">test</Name><age custom="value">12</age></Model>\'\n\nconverter = PydanticXmlConverter("Model")\nmodel = converter.parse_xml(input_xml, ExistingModel)\n\nprint(model)\n>> Model(name="test", age=12)\n\nprint(converter.generate_dict(model))\n>> {"Name": "test", "age": 12}\n\nprint(converter.generate_dict(model, by_alias=False))\n>> {"name": "test", "age": 12}\n\nprint(converter.generate_xml(model))\n>> <?xml version="1.0" encoding="utf-8"?>\n>> <Model><Name id="123">test</Name><age custom="value">12</age></Model>\n```\n\nto view or access the saved attributes identified during parsing, you use the `converter.xml_attributes` attribute. \n',
    'author': 'Patrick Withams',
    'author_email': 'pwithams@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwithams/pydantic-xml-converter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
