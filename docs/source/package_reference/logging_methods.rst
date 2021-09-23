Logging methods
----------------------------------------------------

🤗 Datasets strives to be transparent and explicit about how it works, but this can be quite verbose at times. We have included a series of logging methods which allow you to easily adjust the level of verbosity of the entire library. Currently the default verbosity of the library is set to ``WARNING``.

To change the level of verbosity, use one of the direct setters. For instance, here is how to change the verbosity to the ``INFO`` level:

.. code-block:: python

    import datasets
    datasets.logging.set_verbosity_info()

You can also use the environment variable ``DATASETS_VERBOSITY`` to override the default verbosity, and set it to one of the following: ``debug``, ``info``, ``warning``, ``error``, ``critical``:

.. code-block:: bash
               
    DATASETS_VERBOSITY=error ./myprogram.py

All the methods of this logging module are documented below. The main ones are:

* :func:`datasets.logging.get_verbosity` to get the current level of verbosity in the logger
* :func:`datasets.logging.set_verbosity` to set the verbosity to the level of your choice

In order from the least to the most verbose (with their corresponding ``int`` values):

1. :obj:`datasets.logging.CRITICAL` or :obj:`datasets.logging.FATAL` (int value, 50): only report the most critical errors.
2. :obj:`datasets.logging.ERROR` (int value, 40): only report errors.
3. :obj:`datasets.logging.WARNING` or :obj:`datasets.logging.WARN` (int value, 30): only reports error and warnings. This the default level used by the library.
4. :obj:`datasets.logging.INFO` (int value, 20): reports error, warnings and basic information.
5. :obj:`datasets.logging.DEBUG` (int value, 10): report all information.


Functions
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: datasets.logging.get_verbosity

.. autofunction:: datasets.logging.set_verbosity

.. autofunction:: datasets.logging.set_verbosity_info

.. autofunction:: datasets.logging.set_verbosity_warning

.. autofunction:: datasets.logging.set_verbosity_debug

.. autofunction:: datasets.logging.set_verbosity_error

.. autofunction:: datasets.logging.disable_propagation

.. autofunction:: datasets.logging.enable_propagation

.. autofunction:: datasets.logging.get_logger

Levels
~~~~~~~~~~~~~~~~~~~~~

.. autodata:: datasets.logging.CRITICAL

.. autodata:: datasets.logging.DEBUG

.. autodata:: datasets.logging.ERROR

.. autodata:: datasets.logging.FATAL

.. autodata:: datasets.logging.INFO

.. autodata:: datasets.logging.NOTSET

.. autodata:: datasets.logging.WARN

.. autodata:: datasets.logging.WARNING

