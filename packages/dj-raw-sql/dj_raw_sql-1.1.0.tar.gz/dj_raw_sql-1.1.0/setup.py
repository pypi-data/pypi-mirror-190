# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dj_raw_sql']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2']

setup_kwargs = {
    'name': 'dj-raw-sql',
    'version': '1.1.0',
    'description': 'This is a Django wrapper to make it easier to write raw SQL queries.',
    'long_description': '# dj-raw-sql\n\nThis is a Django wrapper to make it easier to write raw SQL queries.\n\n## Get Started\n\nThis demo shows how to get the record(s) from the database\n\n``` py title="queries.py" linenums="1"\n# queries.py\nfrom dj_raw_sql import execute_sql\n\n@execute_sql()\ndef get_music_by_id(id: int):\n    return "SELECT * FROM dj_app_music WHERE id = %s", (id,)\n```\n\n``` py title="models.py" linenums="1"\n# models.py\nfrom django.db import models\n\n# Our demo model\nclass Music(models.Model):\n    name = models.CharField(max_length=150)\n    create_at = models.DateTimeField(auto_now_add=True)\n    update_at = models.DateTimeField(auto_now=True)\n    is_delete = models.BooleanField(default=False)\n```\n\n``` py title="views.py" linenums="1"\n# views.py\nfrom django.http import JsonResponse\nfrom django.views import View\n\nfrom my_app.queries import get_music_by_id\n\n\nclass MyView(View):\n    def get(self, request, *args, **kwargs):\n        music: tuple[tuple] = get_music_by_id(id=1)\n        return JsonResponse({"name": music[0][1]})\n```\n\n## Benchmarks\n\n**Q**: How were performance tests conducted?\n\n**A**: tests/test_collection/ performance tests are located here. A dataset of 5000 elements was generated and loaded into the database. Then the query "SELECT * FROM dj_app_music LIMIT %s" was called, where the value of LIMIT changed from 10 to 5000 in each test.\n\n---\nTest results\n\n| Number of items |    fetchall   | to_ordereddict=True |\n|-----------------|:-------------:|:-------------------:|\n| 10              | 0.00006       | 0.00011             |\n| 100             | 0.00017       | 0.00025             |\n| 1000            | 0.00138       | 0.00207             |\n| 5000            | 0.00658       | 0.01052             |\n\n## Improve project\n\nIf you want to improve the project then create "Issues" . If you want to help with writing tests or typing, create a "pull request".',
    'author': 'Roman Sotnikov',
    'author_email': 'axeman.ofic@gmail.com',
    'maintainer': 'Roman',
    'maintainer_email': 'axeman.ofic@gmail.com',
    'url': 'https://github.com/axemanofic/dj-raw-sql',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
