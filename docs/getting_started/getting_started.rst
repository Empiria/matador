.. installing_python:

Python 3
========

   Ensure you have a Python 3 interpreter installed on your machine. The recommended interpreter is Anaconda from continuum.io and, on Windows, is the only interpreter on which matador has been tested.

   * Download the Anaconda interpreter from https://www.continuum.io/downloads

      Ensure you choose a Python 3.x (3.5 at the time of writing) version rather
      than a 2.x version.

   * Install the interpreter using the download from above and accept all the default options.

   * From a command prompt, enter the following command::

      python --version

   and you should see something similar to::

      Python 3.5.0 :: Anaconda 2.4.0 (64-bit)

.. installing_matador:

Installing Matador
==================

Your Python installation should include the Python Package Manager, Pip, which
can now be used to install Matador:

   * From a command prompt, enter the following command::

      pip install matador

  * When the installation has finished, test that it worked with::

      matador --help

  You should see something similar to::

      usage: matador [-h] [-l LOGGING_DESTINATION] [-v VERBOSITY] command

      Taming the bull: Change management for Agresso systems

      positional arguments:
        command               Command

      optional arguments:
        -h, --help            show this help message and exit
        -l LOGGING_DESTINATION, --logging LOGGING_DESTINATION
                              logging (none, console or file)
        -v VERBOSITY, --verbosity VERBOSITY
                              Logging level. DEBUG, INFO, ERROR or CRITICAL
      usage: matador [-h] [-l LOGGING_DESTINATION] [-v VERBOSITY] command

      Taming the bull: Change management for Agresso systems

      positional arguments:
        command               Command

      optional arguments:
        -h, --help            show this help message and exit
        -l LOGGING_DESTINATION, --logging LOGGING_DESTINATION
                              logging (none, console or file)
        -v VERBOSITY, --verbosity VERBOSITY
                              Logging level. DEBUG, INFO, ERROR or CRITICAL

A Matador Project
=================

Most Matador commands will only execute successfully from within a valid project
folder.

If you are working on an existing project, simply clone its repository
to a directory of your choice and change into that directory.

e.g. on Windows, to create a folder for a project named 'toreador' within an
existing 'c:\\projects' folder::

    cd c:\projects
    git clone <url for the toreador project>
    cd toreador
