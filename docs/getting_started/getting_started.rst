Pre-Requisites
==============

There are two items of software that you will need to install before you can
install Matador itself:

#.  Git

    Download and install the current version for your operating system from
    https://git-scm.com/download

#.  The Anaconda Python Distribution

    Download and install the current version of Anaconda for Python 3 (e.g. 3.5)
    from https://www.continuum.io/downloads


Installing Matador
==================

Your Python installation should include the Python Package Manager, Pip, which
can now be used to install Matador. From a command line, type::

    pip install matador

You should now be able to call Matador commands from your command line. To test,
enter::

    matador --help

and you should see::

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
