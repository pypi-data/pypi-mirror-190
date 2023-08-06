# Change the content according to your package.

# It is very important to update this file every time there is a new version release in Pypi,
# since the imported classes could be used otherwise an error will appear.
# from <<directory.filename.py>> import <<classname>>
from newpackage.newpackage import Newpackage
from newpackage.seconpackage import Newsito
from newpackage.thirdpackage import Newnewsito

# To avoid having to update the setup.py file on each version release, we can declare here some
# important data such as who last modified the package, their email to contact us and what version
# they are on, in the same way. mode add new descriptions on how to use and execute its functions
__author__  = 'D.Mendez'            # <---- Last developer who modified the package
__email__   = 'danielmen@gmail.com' # <---- His email
__version__ = '0.1.1'               # <---- Version

# module level doc-string
__doc__ = """
newpackage
================

Description
-----------
newpackage is a Python package created for demonstration purposes.
This information will show up when using the help function.

-------
Example to use the Newpackage class
>>> # Import library
>>> from newpackage import Newpackage
>>> # Initialize
>>> model = Newpackage(message='Hello World')
>>> # Run the model
>>> model.show()
-------
Example to use the Newsito class
>>> # Import library
>>> from seconpackage import Newsito
>>> # Initialize
>>> Newsito('Hello there')
>>> Newsito()
-------
Example to use the Newnewsito class
>>> # Import library
>>> from thirdpackage import Newnewsito
>>> # Initialize
>>> Newnewsito()

"""