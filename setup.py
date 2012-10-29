# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import os

version = open(os.path.join("src", "sc", "contentrules",
                            "localrole", "version.txt")).read().strip()

long_description = (open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
                    open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read())

setup(name='sc.contentrules.localrole',
      version=version,
      description="Plone content rule to apply a local role to a content",
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='contentrules action plone localrole',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc', 'sc.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.stringinterp',
      ],
      extras_require={
          'develop': [
              'Sphinx',
              'manuel',
              'pep8',
              'setuptools-flakes',
          ],
          'test': [
              'interlude',
              'plone.app.testing'
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
