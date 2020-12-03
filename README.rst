My Clipping to org-mode notes
=============================

|PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/pyclip2org.svg
   :target: https://pypi.org/project/pyclip2org/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pyclip2org
   :target: https://pypi.org/project/pyclip2org
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/pyclip2org
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/pyclip2org/latest.svg?label=Read%20the%20Docs
   :target: https://pyclip2org.readthedocs.io/
   :alt: Read the documentation at https://pyclip2org.readthedocs.io/
.. |Tests| image:: https://github.com/ppalazon/pyclip2org/workflows/Tests/badge.svg
   :target: https://github.com/ppalazon/pyclip2org/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/ppalazon/pyclip2org/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ppalazon/pyclip2org
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Features
--------

* Parse 'My Clippings.txt' generated file
* Extract highlights, marks and notes
* Export to org-mode files separated by books

Requirements
------------

* You will need a 'My Clippings.txt' file in English or Spanish


Installation
------------

You can install *My Clipping to org-mode notes* via pip_ from PyPI_:

.. code:: console

   $ pip install pyclip2org


Usage
-----

Once you've installed, you can execute

.. code:: console

   $ pyclip2org -l en -o ~/org/kindle -c /media/Kindle/documents/My\ Clippings.txt

Please see the `Command-line Reference <Usage_>`_ for details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the MIT_ license,
*My Clipping to org-mode notes* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.
This project is based on
`Managing kindle highlights with Python and GitHub <https://duarteocarmo.com/blog/managing-kindle-highlights-with-python-and-github.html>`_

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT: http://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/ppalazon/pyclip2org/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://pyclip2org.readthedocs.io/en/latest/usage.html
