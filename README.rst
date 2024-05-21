pysteps-importer-metranet
=========================

Pysteps importer plugin for reading metranet files with py-radlib

This code is a modification of the `Pysteps
importer <https://pysteps.readthedocs.io/en/stable/generated/pysteps.io.importers.import_mch_metranet.html>`__
for 8-bit Meteoswiss radar data, but with ``py-radlib`` used for reading
the data.

License
-------

-  BSD-3 license

Documentation
-------------

Here write a short description of the plugin, indicating the importers
that provides.

Importer ``mch_metranet_radlib`` for MeteoSwiss radar products in the
8-bit Metranet format. The importer uses the py-radlib library for
reading the data.

Installation instructions
-------------------------

Install the importer with pip:

.. code:: bash

   pip install git+https://github.com/ritvje/pysteps-importer-metranet

Note that the ``py-radlib`` library is not installed automatically, so
you should install it manually before using the importer.

After that, the importer is available through the command
``pysteps.io.get_method("mch_metranet_radlib", "importer")``.

Credits
-------

-  This package was created with Cookiecutter\* and the
   ``pysteps/cookiecutter-pysteps-plugin``\ \* project template.

-  The ``pysteps/cookiecutter-pysteps-plugin`` template was adapted from
   the cookiecutter-pypackage\_ template.

   -  cookiecutter-pypackage:
      https://github.com/audreyfeldroy/cookiecutter-pypackage
   -  Cookiecutter: https://github.com/audreyr/cookiecutter
   -  ``pysteps/cookiecutter-pysteps-plugin``:
      https://github.com/pysteps/cookiecutter-pysteps-plugin
