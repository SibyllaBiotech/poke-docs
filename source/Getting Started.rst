===============
Getting Started
===============

Installation
------------

Poké is available on PyPI under the name ``poke-scouter``.
To install it with pip run:

.. code-block:: bash

   python -m pip install poke-scouter

The package provides the ``poke`` command and the ``poke`` Python module.

Alternatively, the package can be installed directly from ``github`` as follows:

.. code-block:: bash

   git clone https://github.com/SibyllaBiotech/poke 
   pip install ./poke 

Basic Example
-------------

.. note::
   All input structures passed to Poké must be protonated and the atom names should match the CHARMM or AMBER convention.

Single Structure
''''''''''''''''

Poké can be used on a single structure (pdb, gro, or pdbqt) with the following command:

.. code-block:: bash   

   poke -dvp protein.pdb 

The result will appear in a folder called the same as the input file (in this example ``protein``) in the current working directory. The options ``-dvp`` are used to specify the desired output files:

* ``-d`` for the descriptors
* ``-v`` for the volumes (a pdb file with the points of the pocket)
* ``-p`` for a pymol script to visualize the pockets

Further information on the options that can be entered can be found in the following section **Options**.

Multiple Structures
'''''''''''''''''''

Poké can also be used on multiple files:

.. code-block:: bash  

   poke -dvp protein1.pdb protein2.pdb 

In this case it will create two output folders called ``protein1`` and ``protein2``.

MD Trajectory
'''''''''''''

In order to run the scouter on all the frames of a trajectory (xtc, trr, or dcd), a reference must be specified to know the atom types (its position will not be used):

.. code-block:: bash  

   poke -dvp reference.pdb trajectory.xtc 

Normally Poké does not produce a new trajectory, but it is possible to extract the frames with at least one pocket using the ``-e`` flag. In this case, the extracted frames are written in a new trajectory file. The frames can be sorted by a property using the ``-s`` flag. The sorting is performed in descending order. For example to extract the frames with at least a pocket and sort them by the score of the pocket use:

.. code-block:: bash

   poke -dvp -e -s score protein.pdb 

Multiple trajectories can be concatenated with:

.. code-block:: bash

   poke -dvp reference.pdb trajectory1.xtc trajectory2.xtc 

If the input is a long list of different files, they can be put in a text file ``.txt`` with a path for each line and passed to Poké:

.. code-block:: bash

   poke -dvp list.txt 



Options
'''''''

``poke -h`` prints every option with a short description. The same list, grouped by topic,
is in the :doc:`CLI Reference`.
