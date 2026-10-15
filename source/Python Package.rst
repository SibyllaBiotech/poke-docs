==============
Python Package
==============

Poké can be used from Python for maximum flexibility. ``Poke.from_mdanalysis`` builds a scouter
from an MDAnalysis ``AtomGroup`` (as on the command line, the atoms must be protonated and named
after the CHARMM or Amber convention), and ``get_pockets`` returns one ``Pocket`` object per
pocket found in the given coordinates. The sample structure used below is a frame from the
mixed-solvent simulation of the :doc:`Tutorials`, so it still contains benzene molecules;
Poké has force-field parameters for protein and nucleic-acid residues, cofactors and ions,
but not for benzene, which is why only the protein is passed to the scouter:

.. testcode::

   from MDAnalysis import Universe
   from poke import Poke

   u = Universe("structure.pdb")
   protein = u.select_atoms("protein")   # leave out the benzene molecules of the simulation

   scouter = Poke.from_mdanalysis(protein)
   pockets = scouter.get_pockets(protein.positions)

   for pocket in pockets:
       residues = protein[pocket.atoms].residues
       print(f"score {pocket.score:.1f}  core volume {pocket.volume:.0f} Å³  "
             f"hydrophobicity {pocket.hydrophobicity:.2f}  "
             f"residues {' '.join(str(r) for r in residues.resids)}")

Each ``Pocket`` carries the same descriptors that the command line writes to
``descriptors.csv``: ``score``, ``volume``, ``surface``, ``accessible``, ``hydrophobicity``,
``enclosure``, ``lengths``, ``n_polar_atoms``, ``n_charged_atoms`` and ``n_apolar_atoms``.
``pocket.atoms`` holds the indices of the pocket atoms in the atom group given to the scouter,
which is how the residues are recovered above. For the sample structure shipped with this
guide, a frame of TEM-1 β-lactamase, the output is:

.. testoutput::

   score 5.8  core volume 18 Å³  hydrophobicity 0.69  residues 79 82 83 86 88 142 147 148 150 151
   score 5.9  core volume 18 Å³  hydrophobicity 0.57  residues 70 73 105 130 132 170 216 237 238 240

To scan a trajectory, call ``get_pockets`` once per frame with that frame's coordinates;
the scouter itself is built only once, because the atom parameters do not change:

.. code-block:: python

   for ts in u.trajectory:
       pockets = scouter.get_pockets(protein.positions)

.. testcode::
   :hide:

   assert len(pockets) > 0, "the example structure should contain at least one pocket"
