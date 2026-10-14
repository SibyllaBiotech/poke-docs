===============
Getting Started
===============

Installation
------------

Poké is available as a wheel package for macOS, Windows and Linux on PyPI.
To install Poké with pip run:

.. code-block:: bash
 
   python -m pip install poke 

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

Through the ``poke -h`` you can view the various options that you can specify when you want to run Poké.
The various options are shown below in alphabetical order.

+----------+---------------------+--------------------------------------------+
|  -short  |       --long        |                 Description                |
+==========+=====================+============================================+
|    -a    |       --align       | align the given atoms selection to the     |
|          |                     | reference                                  |
+----------+---------------------+--------------------------------------------+
|    -d    |   --descriptors     | compute the descriptors and save them in a |
|          |                     | csv file                                   |
+----------+---------------------+--------------------------------------------+
|    -dx   |      --density      | save the density map of the pockets in a   |
|          |                     | dx file                                    |
+----------+---------------------+--------------------------------------------+
|    -e    |      --extract      | save the results relative to a new         |
|          |                     | trajectory containing only frames with at  |
|          |                     | least one pocket                           |
+----------+---------------------+--------------------------------------------+
|    -f    |       --filter      | filter the pockets with a condition        |
+----------+---------------------+--------------------------------------------+
|    -g    |       --graph       | plot distributions of pocket descriptors   |
+----------+---------------------+--------------------------------------------+
|    -h    |        --help       | show the help message and exit             |
+----------+---------------------+--------------------------------------------+
|    -k    |       --pickle      | save a pickle with a list of pockets for   |
|          |                     | each frame                                 |
+----------+---------------------+--------------------------------------------+
|    -ls   |   --launch-script   | save launch command in a bash script to be |
|          |                     | able to rerun with the same parameters     |
+----------+---------------------+--------------------------------------------+
|    -n    | --max-output-frames | maximum number of pockets in the output.   |
|          |                     | Only when --sort is used.                  |
+----------+---------------------+--------------------------------------------+
|    -nc   |      --ncores       | number of cores used to parallelize the    |
|          |                     | computation of trajectories or multimodel  |
|          |                     | pdb files                                  |
+----------+---------------------+--------------------------------------------+
|    -o    |       --output      | output path where to create the folder(s)  |
|          |                     | with the results                           |
+----------+---------------------+--------------------------------------------+
|    -p    |       --pymol       | save a pymol script usable to open the     |
|          |                     | pockets found                              |
+----------+---------------------+--------------------------------------------+
|    -q    |       --quiet       | avoid to write the progress for long       |
|          |                     | trajectories                               |
+----------+---------------------+--------------------------------------------+
|    -r    |     --reference     | reference structure used for alignment.    |
|          |                     | Default is the first structure.            |
+----------+---------------------+--------------------------------------------+
|    -s    |        --sort       | sorting by the value of an expression      |
+----------+---------------------+--------------------------------------------+
|    -sf   |  --scoring-function | scoring function used                      |
+----------+---------------------+--------------------------------------------+
|    -so   |  --selection-output | selection of atoms written in the output   |
+----------+---------------------+--------------------------------------------+
|    -ss   | --selection-scouter | selection of atoms used by scouter         |
+----------+---------------------+--------------------------------------------+
|    -v    |      --volumes      | save the volumes in a multi-model PDB file |
+----------+---------------------+--------------------------------------------+
|    -z    |      --compress     | compress the results using gzip, most of   |
|          |                     | the programs can read them without problem |
+----------+---------------------+--------------------------------------------+
