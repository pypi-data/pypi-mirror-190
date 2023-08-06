# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amqtt',
 'amqtt.mqtt',
 'amqtt.mqtt.protocol',
 'amqtt.plugins',
 'amqtt.plugins.sys',
 'amqtt.scripts']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.0,<7.0',
 'docopt>=0.6.0,<0.7.0',
 'passlib>=1.7.0,<2.0.0',
 'transitions>=0.8.0,<0.9.0',
 'websockets>=9.0,<11.0']

extras_require = \
{'ci': ['coveralls>=3.0.1,<4.0.0']}

entry_points = \
{'amqtt.broker.plugins': ['auth_anonymous = '
                          'amqtt.plugins.authentication:AnonymousAuthPlugin',
                          'auth_file = '
                          'amqtt.plugins.authentication:FileAuthPlugin',
                          'broker_sys = '
                          'amqtt.plugins.sys.broker:BrokerSysPlugin',
                          'event_logger_plugin = '
                          'amqtt.plugins.logging:EventLoggerPlugin',
                          'packet_logger_plugin = '
                          'amqtt.plugins.logging:PacketLoggerPlugin',
                          'topic_acl = '
                          'amqtt.plugins.topic_checking:TopicAccessControlListPlugin',
                          'topic_taboo = '
                          'amqtt.plugins.topic_checking:TopicTabooPlugin'],
 'amqtt.client.plugins': ['packet_logger_plugin = '
                          'amqtt.plugins.logging:PacketLoggerPlugin'],
 'amqtt.test.plugins': ['event_plugin = '
                        'tests.plugins.test_manager:EventTestPlugin',
                        'packet_logger_plugin = '
                        'amqtt.plugins.logging:PacketLoggerPlugin',
                        'test_plugin = '
                        'tests.plugins.test_manager:EmptyTestPlugin'],
 'console_scripts': ['amqtt = amqtt.scripts.broker_script:main',
                     'amqtt_pub = amqtt.scripts.pub_script:main',
                     'amqtt_sub = amqtt.scripts.sub_script:main']}

setup_kwargs = {
    'name': 'amqtt',
    'version': '0.11.0b1',
    'description': 'MQTT client/broker using Python asyncio',
    'long_description': None,
    'author': 'aMQTT Contributers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Yakifo/amqtt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
