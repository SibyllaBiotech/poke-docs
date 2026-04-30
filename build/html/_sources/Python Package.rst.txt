==============
Python Package
==============

The scouter can be used though python to achieve maximum flexibility:

.. code-block:: python

   from poke import Poke
   from MDAnalysis import Universe

   u = Universe('1gkc.pdb')
   
   scouter = Poke()
   scouter.load_atoms_properties_from_mdanalysis(u.atoms)
   pockets = scouter.get_pockets(u.atoms.positions)
  
   for p in pockets:
      print(p)


.. note::

   When the scouter is used from command line, the option ``-k`` can be used to save pockets in a pickle file. 

.. important::

   COME MAI QUESTA INFORMAZIONE E' RIPORTATA QUI?
