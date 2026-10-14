=======
Filters
=======

Atom filtering
==============

It is possible to use only a subset of the atoms in the input file to compute energy maps. The atoms can be selected using the ``-ss`` flag and a selection string. The selection string must be in the format of the ``MDAnalysis`` package. For example if the pdb file contains water molecules, the protein can be selected using:

.. code-block:: bash
   
   poke -dvp -ss "protein" protein.pdb

Using the ``-so`` flag it is possible to select the atoms of the input structure that should be written in the output trajectory. Atoms not present in the ``-so`` selection are anyway used to compute the energy maps unless the ``-ss`` flag is used to remove them.


Pocket filtering
================

The pockets can be filtered by properties or by the residues involved. The filtering is performed using the ``-f`` flag and is a python expression. A pocket is kept only if the expression evaluates to ``True``.

For example, to select only the pockets with a volume greater than A^3:

.. code-block:: bash

   poke -dvp -f "volume > 100" protein.pdb

To select only the pockets with a score greater than 6 and with enclosure greater than 0.5 use:

.. code-block:: bash

   poke -dvp -f "score > 6 and enclosure > 0.5" protein.pdb 

After the sorting, the ``-n`` flag can be used to select only the first ``n`` pockets. For example to select only the best 5 pockets by score use:

.. code-block:: bash

   poke -dvp -s score -n 5 protein.pdb
