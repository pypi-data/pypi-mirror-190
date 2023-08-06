==================================
 RsFswp
==================================

.. image:: https://img.shields.io/pypi/v/RsFswp.svg
   :target: https://pypi.org/project/ RsFswp/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsFswp.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsFswp.svg
   :target: https://pypi.python.org/pypi/RsFswp/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsFswp.svg
   :target: https://pypi.python.org/pypi/RsFswp/

Rohde & Schwarz FSWP Phase Noise Analyzer RsFswp instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsFswp import *

    instr = RsFswp('TCPIP::192.168.2.101::hislip0')
    idn = instr.query('*IDN?')
    print('Hello, I am: ' + idn)

Check out the full documentation on `ReadTheDocs <https://RsFswp.readthedocs.io//>`_.

Supported instruments: FSWP, FSPN

The package is hosted here: https://pypi.org/project/RsFswp/

Examples: https://github.com/Rohde-Schwarz/Examples/tree/main/SpectrumAnalyzers/Python/RsFswp_ScpiPackage


Version history
----------------

	Latest release notes summary: Update for FSWP FW 3.0

	Version 3.0.0
		- Update for FSWP FW 3.0

	Version 2.0.1
		- Update Documentation

	Version 2.0.0
		- First released version

