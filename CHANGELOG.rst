Changelog
#########

Unreleased
----------

v4.0.1 (2017-06-22)
-------------------

* Enhancement: Each command and its options now have help text available


v4.0.0 (2017-06-21)
-------------------

* Incompatibility: ``deploy.py`` and ``remove.py`` files in tickets now need
  to import from ``matador.cli.deployment``

v3.1.0 (2017-06-15)
-------------------

* New Feature: Deployment command ``remove_report_file()``

v3.0.0 (2017-06-14)
-------------------

* Incompatibility: Deployment command classes have been deprecated and replaced
  by equivalent callables. e.g. ``DeploySqlFile()`` has been replaced by
  ``deploy_sql_file()``
