===============
Getting Started
===============

Installation
------------

Poké is available on PyPI under the name ``poke-scouter``. To install it with pip run:

.. code-block:: bash

   python -m pip install poke-scouter

The package provides the ``poke`` command and the ``poke`` Python module. It requires Python 3.11 or later.

Alternatively, the package can be installed directly from GitHub:

.. code-block:: bash

   git clone https://github.com/SibyllaBiotech/poke
   pip install ./poke

Basic Examples
--------------

.. note::
   All input structures passed to Poké must be protonated and the atom names should match
   the CHARMM or Amber convention. Alternatively, use the ``--prepare`` flag to let Poké add 
   the hydrogens itself (see :doc:`Structure Preparation`).

Single Structure
''''''''''''''''

Poké can be used on a single structure (pdb, cif, mmcif, gro, or pdbqt) with the following command:

.. code-block:: bash

   poke -dvp protein.pdb

The result will appear in a folder named after the input file (in this example ``protein``)
in the current working directory. The flags ``-dvp`` specify the desired output files:

* ``-d`` for the descriptors CSV file (see :doc:`Descriptors`)
* ``-v`` for the volumes, a PDB file with the grid points of each pocket
* ``-p`` for a PyMOL script to visualize the pockets

The other output files are described in :doc:`Outputs`.

Multiple Structures
'''''''''''''''''''

Poké can also be used on multiple files:

.. code-block:: bash

   poke -dvp protein1.pdb protein2.pdb

In this case it will create two output folders called ``protein1`` and ``protein2``.

If the input is a long list of files, they can be listed in a text file (``.txt``, one path
per line) and passed to Poké:

.. code-block:: bash

   poke -dvp list.txt

MD Trajectory
'''''''''''''

To run the scouter on all the frames of a trajectory (xtc, trr, or dcd), a reference
structure must be provided to define the atom types (its positions will not be used):

.. code-block:: bash

   poke -dvp reference.pdb trajectory.xtc

Multiple trajectories can be concatenated:

.. code-block:: bash

   poke -dvp reference.pdb trajectory1.xtc trajectory2.xtc

Normally Poké does not produce a new trajectory, but the frames with at least one pocket can
be extracted into one with the ``-e`` flag. The pockets can be sorted by any property with
the ``-s`` flag, in descending order, and ``-n`` keeps only the first ones. For example, to
extract the frames with a pocket and keep the ten best pockets by score:

.. code-block:: bash

   poke -dvp -e -s score -n 10 reference.pdb trajectory.xtc

Pockets can also be filtered by their properties or by the residues they involve; see
:doc:`Filters`.

A file with several models, such as an NMR ensemble in PDB or mmCIF format, is read like a
trajectory: each model is a frame.

Options
'''''''

``poke -h`` prints every option with a short description. The same list, grouped by topic,
is in the :doc:`CLI Reference`.
