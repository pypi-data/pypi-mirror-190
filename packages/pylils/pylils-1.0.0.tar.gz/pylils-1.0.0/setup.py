# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lils']

package_data = \
{'': ['*']}

install_requires = \
['lark>=1.1.5,<2.0.0']

extras_require = \
{'dbus': ['pygobject>=3.42.2,<4.0.0']}

entry_points = \
{'console_scripts': ['lils = lils.__main__:main', 'lils-dbus = lils.dbus:main']}

setup_kwargs = {
    'name': 'pylils',
    'version': '1.0.0',
    'description': 'Linux Immersive Learning System',
    'long_description': "## Project Description\n\nImmersive system to run interactive tutorials, hacking learning lessons or just\ngames that integrates with your system. The main idea is to have an\n[INK](https://www.inklestudios.com/ink/) language engine to process the\n**tutorial** scripts and provide an interactive user interface to the user. The\nsystem should be able to listen to different Linux events (like filesystem\nchanges, process is running, the current date, etc) and modify the **tutorial**\nstate depending on that.\n\nExample:\n * We've a tutorial to learn about how to use the linux terminal, a bash\n   introduction\n * The tutorial gives to the user a brief explanation about how to create a\n   directory and waits for the directory to be created\n * Once the system detects that directory, it automatically go forwards, says\n   congrats to the user and continues with the next step\n\nThe main idea is to build the base system with Python and provide a generic\ninterface (dbus, socket, cli) to be able to extend and use from different\nlanguages.\n\nThis idea is based on the [Hack Computer](https://www.hack-computer.com/)\nconcept, but trying to make it simpler and not tied to the desktop. It's a\nsimple concept to have a way to create a more fun learning experience using a\n[Choose Your Own Adventure](https://en.wikipedia.org/wiki/Choose_Your_Own_Adventure)\nlike tutorial flow, with different user input that can happen in a different\nprocess.\n\n\n## Goal for this Hackweek\n\nThis is the full list of goals that will be great to have, in order of\nimportance:\n\n 1. Build a basic python Ink language interpreter\n 1. Create the base system that runs the tutorial, keep the state and provide\n    an API to be used\n 1. Make the base system extensible with **listeners** that can wait for\n    different kind of events:\n    * user option selection\n    * user text input\n    * new file\n    * date change\n    * launch program, close program\n    * system reboot?\n    * ...\n 1. Create initial tutorial about how to write **lils** tutorials / games\n 1. Create different graphical user interfaces (GNOME shell plugin, desktop\n    application, web interface...)\n\n## Resources\n\n * [Hack Computer](https://www.hack-computer.com/)\n * [Hack Web interface](https://try.hack-computer.com/)\n * [INK](https://www.inklestudios.com/ink/)\n",
    'author': 'Daniel Garcia Moreno',
    'author_email': 'daniel.garcia@suse.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
