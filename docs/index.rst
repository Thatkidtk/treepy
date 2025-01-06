# docs/index.rst
Welcome to RPTree's documentation!
================================

RPTree is a Python command-line tool for generating visually appealing directory tree diagrams.

Features
--------

* Generate directory tree diagrams with Unicode box-drawing characters or ASCII
* Customize output depth, hidden files visibility, and file size display
* Save output to file or display in console
* Cross-platform compatibility using ``pathlib``
* Async support for large directories
* Multiple output formats (text, JSON, XML, HTML)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   contributing
   changelog

Installation
-----------

To install RPTree::

    pip install rptree

Basic Usage
----------

.. code-block:: bash

    # Generate basic tree
    rptree /path/to/directory

    # Show file sizes
    rptree /path/to/directory --size

    # Limit depth to 2 levels
    rptree /path/to/directory -d 2

API Documentation
---------------

.. automodule:: rptree.rptree
   :members:

.. automodule:: rptree.async_tree
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
