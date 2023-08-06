from setuptools import setup, find_packages

version = '2.3.0'

setup(name='plone.locking',
      version=version,
      description="webdav locking support",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 5.2",
          "Framework :: Plone :: 6.0",
          "Framework :: Plone :: Core",
          "Framework :: Zope :: 4",
          "Framework :: Zope :: 5",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
        ],
      keywords='locking webdav plone',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='https://pypi.org/project/plone.locking',
      license='GPL version 2',
      packages=find_packages(),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
      extras_require=dict(
        test=[
            'plone.app.contenttypes',
            'plone.app.testing',
        ]
      ),
      install_requires=[
        'setuptools',
        'zope.annotation',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.viewlet',
        'Acquisition',
        'DateTime',
        'Products.CMFCore',
        'ZODB',
        'Zope',
      ],
      )
