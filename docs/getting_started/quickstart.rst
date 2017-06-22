.. installing_python:

Python 3.6
==========

   Matador requires Python 3.6 or later.

   The recommended distributing is miniconda from continuum.io and, on Windows,
   is the only distribution on which matador has been tested.

   * Download the miniconda interpreter from https://conda.io/miniconda.html

      Ensure you choose a Python 3.x version rather than a 2.x version.

   * Install the interpreter using the download from above and accept all the
     default options.

   * From a command prompt, enter the following command::

      python --version

   and you should see something similar to::

      Python 3.6.1 :: Continuum Analytics, Inc.

.. installing_matador:

Installing Matador
==================

Your Python installation should include the Python Package Manager, Pip, which
can now be used to install Matador:

   * From a command prompt, enter the following command::

      pip install matador

  * When the installation has finished, test that it worked with::

      matador --version

  You should see something similar to::

      matador version 4.0.0

A Matador Project
=================

Most Matador commands will only execute successfully from within a valid
matador project folder.

If you are working on an existing project, simply clone its repository
to a directory of your choice and change into that directory.

e.g. on Windows, to create a folder for a project named 'toreador' within an
existing 'c:\\projects' folder::

    cd c:\projects
    git clone <url for the toreador project>
    cd toreador

If you are starting a new project, you can use the matador command ``init`` to
create the necessary project structure.

e.g. on Windows, to to create a new project named 'toreador' within an existing
'c:\\projects' folder::

   cd c:\\projects
   matador init --project toreador
