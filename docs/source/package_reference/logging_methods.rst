Logging methods
----------------------------------------------------

`datasets` tries to be very transparent and explicit about it's inner working bt this can be quite verbose at some time.
A series of logging methods let you easily adjust the level of logging of the whole library.

Functions
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: datasets.logging.get_verbosity

.. autofunction:: datasets.logging.set_verbosity

.. autofunction:: datasets.logging.set_verbosity_info

.. autofunction:: datasets.logging.set_verbosity_warning

.. autofunction:: datasets.logging.set_verbosity_debug

.. autofunction:: datasets.logging.set_verbosity_error

.. autofunction:: datasets.logging.disable_default_handler

.. autofunction:: datasets.logging.enable_default_handler

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

