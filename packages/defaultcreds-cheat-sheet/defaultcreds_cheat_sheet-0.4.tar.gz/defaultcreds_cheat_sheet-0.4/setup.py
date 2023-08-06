# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['DefaultCreds']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.5.0,<0.6.0',
 'pathlib>=1.0.1,<2.0.0',
 'prettytable==3.6.0',
 'requests>=2.28.2,<3.0.0',
 'tinydb>=4.7.1,<5.0.0']

entry_points = \
{'console_scripts': ['creds = DefaultCreds.creds:run']}

setup_kwargs = {
    'name': 'defaultcreds-cheat-sheet',
    'version': '0.4',
    'description': 'One place for all the default credentials to assist pentesters during an engagement, this document has several products default login/password gathered from multiple sources.',
    'long_description': '[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)\n\n# Default Credentials Cheat Sheet\n\n<p align="center">\n  <img src="https://media.moddb.com/cache/images/games/1/65/64034/thumb_620x2000/Lockpicking.jpg"/>\n</p>\n\n**One place for all the default credentials to assist pentesters during an engagement, this document has several products default login/password gathered from multiple sources.**\n\n> P.S : Most of the credentials were extracted from changeme,routersploit and Seclists projects, you can use these tools to automate the process https://github.com/ztgrace/changeme , https://github.com/threat9/routersploit (kudos for the awesome work)\n\n- [x] Project in progress\n\n## Motivation\n- One document for the most known vendors default credentials\n- Assist pentesters during a pentest/red teaming engagement\n- **Helping the Blue teamers to secure the company infrastructure assets by discovering this security flaw in order to mitigate it**. See \n[OWASP Guide [WSTG-ATHN-02] - Testing_for_Default_Credentials](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/04-Authentication_Testing/02-Testing_for_Default_Credentials "OWASP Guide")\n\n\n#### Short stats of the dataset\n\n|       | Product/Vendor |\tUsername | Password |\n| --- | --- | --- | --- |\n| **count**\t| 3460\t| 3460\t| 3460 |\n| **unique** |\t1182\t| 1086 |\t1601 |\n| **top** |\tOracle| <blank> | <blank> |\n| **freq** |\t235 |\t718 |\t461 |\n\n#### Sources\n\n- [Changeme](https://github.com/ztgrace/changeme "Changeme project")\n- [Routersploit]( https://github.com/threat9/routersploit "Routersploit project")\n- [betterdefaultpasslist]( https://github.com/govolution/betterdefaultpasslist "betterdefaultpasslist")\n- [Seclists]( https://github.com/danielmiessler/SecLists/tree/master/Passwords/Default-Credentials "Seclist project")\n- [ics-default-passwords](https://github.com/arnaudsoullie/ics-default-passwords) (thanks to @noraj)\n- Vendors documentations/blogs\n\n#### Creds script\n\nYou can turn the cheat sheet into a cli command and perform search queries for a specific product.\n\n* Usage Guide\n```bash\n# Search for product creds\n➤ python3 creds search tomcat                                                                                                      \n+----------------------------------+------------+------------+\n| Product                          |  username  |  password  |\n+----------------------------------+------------+------------+\n| apache tomcat (web)              |   tomcat   |   tomcat   |\n| apache tomcat (web)              |   admin    |   admin    |\n...\n+----------------------------------+------------+------------+\n\n# Update records\n➤ python3 creds update\nCheck for new updates...🔍\nNew updates are available 🚧\n[+] Download database...\n\n# Export Creds to files (could be used for brute force attacks)\n➤ python3 creds search tomcat export\n+----------------------------------+------------+------------+\n| Product                          |  username  |  password  |\n+----------------------------------+------------+------------+\n| apache tomcat (web)              |   tomcat   |   tomcat   |\n| apache tomcat (web)              |   admin    |   admin    |\n...\n+----------------------------------+------------+------------+\n\n[+] Creds saved to /tmp/tomcat-usernames.txt , /tmp/tomcat-passwords.txt 📥\n```\n  \n[![asciicast](https://asciinema.org/a/526599.svg)](https://asciinema.org/a/526599)\n  \n#### Pass Station\n\n[noraj][noraj] created CLI & library to search for default credentials among this database using `DefaultCreds-Cheat-Sheet.csv`.\nThe tool is named [Pass Station][pass-station] ([Doc][ps-doc]) and has some powerful search feature (fields, switches, regexp, highlight) and output (simple table, pretty table, JSON, YAML, CSV).\n\n[![asciicast](https://asciinema.org/a/397713.svg)](https://asciinema.org/a/397713)\n\n[noraj]:https://pwn.by/noraj/\n[pass-station]:https://github.com/sec-it/pass-station\n[ps-doc]:https://sec-it.github.io/pass-station/\n\n## Contribute\n\nIf you cannot find the password for a specific product, please submit a pull request to update the dataset.<br>\n\n> ### Disclaimer\n> **For educational purposes only, use it at your own responsibility.** \n',
    'author': 'ihebski',
    'author_email': 'botsy.project@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ihebski/DefaultCreds-cheat-sheet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
