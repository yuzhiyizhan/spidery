from setuptools import setup, find_packages

setup(name='scrapy-mymodule',
      entry_points={
          'scrapy.commands': [
              'my_command=my_scrapy_module.commands:MyCommand',
          ],
      },
      )
