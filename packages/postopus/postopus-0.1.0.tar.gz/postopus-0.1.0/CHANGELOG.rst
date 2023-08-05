=========
Changelog
=========

Version 0.1.0
=============

* First alpha version of postopus.
* Supports reading of "cube", "xsf", "vtk", "x=0", "y=0", "z=0", "x=0,y=0", "x=0,z=0", "y=0,z=0", "ncdf", and "nc" field octopus output files.
* The field data is stored in the dictionary `run.systemname.calculationmode.fieldname` for `ScalarFields` and `run.systemname.calculationmode.fieldname(.dimension)` for `VectorFields`. It can be retrieved by using any of the `get()` methods. Depending on the situation, we can use: `get()`, `iget()`, `get_converged()`, or `get_all()`. These methods will return an `xarray` object, also with units support (as strings).
* Comprehensive tutorials on how to use the `xarray` objects for analyzing data and visualizing it, also in combination with other libraries like `holoviews` or `xrft`.
* Supports the reading of many table-like and unstructured files without extension stored in td.general and static folders. The data is stored in the dictionary `run.systemname.calculationmode.filename`. The return type will be either a `pandas.DataFrame` or a string depending on the file type. We do not need to use any of the `get()` methods for files without extensions.
