# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_migrations_ci',
 'django_migrations_ci.backends',
 'django_migrations_ci.management',
 'django_migrations_ci.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=3,<5']

entry_points = \
{'pytest11': ['migrateci = django_migrations_ci.pytest_plugin']}

setup_kwargs = {
    'name': 'django-migrations-ci',
    'version': '0.6.2',
    'description': 'Django migrations CI optimization',
    'long_description': '# django-migrations-ci\n\nReuse database state on CI. Run migrations on CI tests only for changes.\n\nMigrations are slow, but you have to run it on CI for testing reasons, so avoid\nto run them when the database state was already tested.\n\n## Install\n\nInstall the package with pip:\n\n```shell\npip install django-migrations-ci\n```\n\nAdd `django_migrations_ci` to Django settings `INSTALLED_APPS`.\n\n```python\nINSTALLED_APPS = [\n    ...,  # other packages\n    "django_migrations_ci",\n]\n```\n\n## How to use\n\nThe command `migrateci` execute all migrations and save dump files `migrateci-*`.\n\nIf these files already exist on disk, they are used to prepare the database\nwithout running all migrations again.\n\n## Workflow\n\nThis is how the "run test" CI job should work.\n\n```shell\n./manage.py migrateci\n./manage.py test --keepdb\n```\n\nIt works with `pytest-django` too as a plugin:\n\n```shell\npytest --migrateci --reuse-db\n```\n\nThe recommended way to work with it is configuring default [pytest `addopts`](https://docs.pytest.org/en/7.1.x/example/simple.html#how-to-change-command-line-options-defaults) with `--migrateci --reuse-db` to run without recreating database. When you want to recreate, run pytest with `--create-db` that has precedence over `--reuse-db`.\n\n\n## Parallel tests\n\n```shell\n./manage.py migrateci --parallel $(nproc)\n./manage.py test --keepdb --parallel $(nproc)\n```\n\n### Parallel tests with pytest-django\n\n```shell\npytest --migrateci --reuse-db --parallel $(nproc)\n```\n\nAlso check [database names for parallel tests](#database-names-for-parallel-tests).\n\n## Settings\n\n##### `MIGRATECI_STORAGE="django.core.files.storage.FileSystemStorage"`\n\nFile storage class. The [django-storages](https://pypi.org/project/django-storages/) package has many backends implemented.\n\nSaving cache files to an external storage allow the lib to reuse partial migrations.\nWhen you write a new migration, it will try to get a cache without this\nlast migration and load from it, running only the new migrations.\n\nThe [example app has a basic S3 configuration](example/settings.py#L29-L34), but it\'s possible\nto use any custom backend:\n\n```python\nfrom storages.backends.s3boto3 import S3Boto3Storage\n\nclass MigrateCIStorage(S3Boto3Storage):\n    bucket_name = "mybucket-migrateci-cache"\n    region_name = "us-east-1"\n    object_parameters = {\n        "StorageClass": "REDUCED_REDUNDANCY",\n    }\n```\n\n##### `MIGRATECI_LOCATION=""`\n\n[File storage API](https://docs.djangoproject.com/en/4.1/ref/files/storage/#the-filesystemstorage-class) has a location arg that all backend use in some way.\n\nIf no storage is defined, it defaults to `~/.migrateci` to make it easy to work local.\n\n##### `MIGRATECI_PYTEST=False`\n\nThe [`pytest-django`](https://pypi.org/project/pytest-django) package use custom test database names.\n\nIf you use it and don´t change their default fixtures, just use `MIGRATECI_PYTEST=True`.\n\n\n#### `MIGRATECI_PARALLEL=None`\n\nBefore tests, Django execute all migrations in one database and clone it to be able to run parallel tests.\nUse `MIGRATECI_PARALLEL="auto"` to create one database per process or define the exact number of processes with `MIGRATECI_PARALLEL=4`.\n\nIt supports how Django test and how [pytest-xdist](https://pypi.org/project/pytest-xdist) works.\n\n#### `MIGRATECI_DEPTH=1`\n\nThis is how we decide which migration cache to use.\n\nFirst, it\'ll try to find a cache with all migration files, but in some cases it\'s not possible,\nlike when you just pushed a new migration.\n\nFor `MIGRATECI_DEPTH=1`, it\'ll remove one migration a time for each Django app installed and check if some cached migration exists. It support the most common use case and it\'s reasonably fast.\n\nBigger values cause a cost operation, it\'ll remove N migrations a time and check if some cached migration exists. It\'s a combination of every Django app. E.g. for 10 apps, it\'ll take at most 10^N checks, with some hashing operations.\n\n### Command line settings\n\nAll below settings can be defined through command line args.\n\n```\nmanage.py migrateci [-h] [-n PARALLEL] [--storage STORAGE_CLASS] [--location LOCATION]\n[--pytest] [--depth DEPTH] [-v {0,1,2,3}]\n\noptions:\n  -h, --help            show this help message and exit\n  -n PARALLEL, --parallel PARALLEL\n  --storage STORAGE_CLASS\n  --location LOCATION\n  --pytest\n  --depth DEPTH\n  -v {0,1,2,3}\n```\n\n## Local migration caching\n\nAs a stretch of this package, it\'s possible to use the same strategy during local\ndevelopment. It\'ll by default cache files at `~/.migrateci`.\n\n```shell\n./manage.py migrateci --parallel $(nproc)\n./manage.py test --keepdb --parallel $(nproc)\n```\n\n## Why migrations are slow?\n\nDjango migrations are slow because of state recreation for every migration and other internal Django magic.\n\nIn the past, I tried to optimize that on Django core, but learnt it\'s a [running issue](https://code.djangoproject.com/ticket/29898).\n\n## Supported databases\n\n* mysql\n* postgresql\n* sqlite3\n\nDjango default run sqlite3 tests as in memory database and does not work because\n`migrateci` runs in a different process. Add a test database name to settings,\nlike [sqlite test settings](django_migrations_ci/tests/testapp/settings_sqlite.py).\n\nDjango supports oracle, but the dump function is not implemented here.\n\n## Database names for parallel tests\n\nDjango test framework has a `--parallel N` flag to test with N parallel processes,\nnaming databases from 1 to N.\n\n* On sqlite3, a `db.sqlite3` generate `db_N.sqlite3` files.\n* On other databases, a `db` generate `test_db_N`.\n\nPytest `pytest-django` use `pytest-xdist` for parallel support, naming databases\nfrom 0 to N-1.\n\n* On sqlite3, a `db.sqlite3` generate `db.sqlite3_gwN` files.\n* On other databases, a `db` generate `test_db_gwN`.\n',
    'author': 'Iuri de Silvio',
    'author_email': 'iurisilvio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
