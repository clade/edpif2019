from distutils.core import setup
__version__ = "alpha"

long_description="""This is a very nice package 

"""

setup(name='my_package',
      version=__version__,
      description='A very nice package',
      mong_description=long_description,
      author=u'François Pignon',
      author_email='francois.pignon@trucmuch.fr',
      url='',
      packages=['my_package'],
     )
