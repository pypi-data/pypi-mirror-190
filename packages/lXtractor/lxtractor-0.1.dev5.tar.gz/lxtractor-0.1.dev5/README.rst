lXtractor
=========

.. image:: https://coveralls.io/repos/github/edikedik/lXtractor/badge.svg
    :target: https://coveralls.io/github/edikedik/lXtractor
    :alt: Branch coverage

.. image:: https://readthedocs.org/projects/lxtractor/badge/?version=latest
    :target: https://lxtractor.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation status

.. image:: https://img.shields.io/pypi/v/lXtractor.svg
    :target: https://pypi.org/project/lXtractor
    :alt: PyPi status

.. image:: https://img.shields.io/pypi/pyversions/lXtractor.svg
    :target: https://pypi.org/project/lXtractor
    :alt: Python version

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
   :alt: Hatch project
   :target: https://github.com/pypa/hatch

Installation
============

First, create a fresh conda environment::

    conda create -n lxt python=3.10 -y

Currently, `lXtractor` uses `mafft <https://mafft.cbrc.jp/alignment/software/>`_
to handle mappings between a sequence and MSA columns. Consequently, it expects
mafft to be available in ``$PATH$``. You can either install mafft system-wide
or use conda::

    conda install -c conda-forge mafft -y
    conda activate lXt

Using pip
---------

..code :: python
    pip install lXtractor

Using conda
-----------

TBD


From source
-----------

