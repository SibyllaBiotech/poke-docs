=========
Tutorials
=========

Background
----------

Cryptic pockets are transient cavities in proteins that can be revealed by local structural fluctuations or binding with small molecules. These regions are typically far from the catalytic site. Computational approaches, such as mixed-solvent molecular dynamics simulations, enhanced sampling, and pocket prediction tools, can be used to detect cryptic pockets. They can also be detected experimentally through biophysical techniques, such as X-ray crystallography. :cite:`bemelmans2025computational, vajda2018cryptic, mou2025discovery`

TEM-1 beta-lactamase is an example of a protein that reveals cryptic pockets when simulated in a mixed solvent. :cite:`bemelmans2025computational` Nevertheless, these pockets have also been observed through crystallography experiments. :cite:`vajda2018cryptic, horn2004allosteric`

In order to test the ability of Poké to capture the appearance of cryptic pockets in proteins, we simulated TEM-1 beta lactamase in mixed-solvent. Among the multiple TEM apo structures available in Protein Data Bank, we chose PDB ID 1LI9 (1.5 Å resolution) for our purpose. The simulations were performed with GROMACS. First, we placed the protein in a simulation box of 7.6 x 7.6 x 7.6 nm. Then, we solvated the system with the TIP3P water model and neutralized it with a 150mM concentration of NaCl. Then, to generate the mixed-solvent we added a 30mM concentration of Benzene. The protein and the benzene have been parameterized with the CHARMM36 force field. 
The system was equilibrated at physiological conditions of pressure (1 atm) and temperature (37°C) using an NPT ensemble. Then, the productive run was carried out at constant pressure and temperature for a total simulation time of 10 µs. 
The opening of the cryptic pocket has been also monitored through RMSD.

.. image:: _static/plots/rmsd_cryptic-fortutorial.png


Pocket inspection with poké
---------------------------

Loading files:
''''''''''''''

The test files we will be working with feature the 10 µs trajectory of TEM protein in mixed solvent: ``ref.gro`` is the structure file from which we will be able to load the trajectory file, ``ligands.xtc``.

.. note::

  To avoid visual mismatching between the positions of the benzene molecules and the pockets detected, we recommend applying a periodic-boundary-condition (PBC) correction to the positions of the ligands in the trajectory.


Calculation of the distribution of pockets in the protein and distribution of pocket properties.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

We define a ``density grid`` with the volume points of the pockets inspected in TEM protein.

.. code-block:: bash

   poke ref.gro ligands.xtc -dx -ss protein -a protein -so protein --sort score -ls -o density_inspection_all

The results are returned as a NumPy array stored in ``density.dx`` and ``density.mrc``. The first format (``density.dx``) is a text-based file containing structured blocks of information: grid origin and spacing, number of grid points and the actual density values. This format is easily readable with PyMol.
The second format (``density.mrc``) contains  density point information in binary format. The file consists of a header that stores the grid size, origin, voxel spacing, map statistics, and data type. This format type is more suitable for Chimera, though it can also be parsed by PyMol.


.. image:: _static/plots/density_allpockets.png


.. code-block:: bash
    
    poke ref.gro ligands.xtc -dg -ss protein -a protein -so protein --sort score -ls -o histograms_all


.. image:: _static/plots/Score.png
  :alt: Score



.. image:: _static/plots/Volume.png
  :alt: Volume



.. image:: _static/plots/Hydrophobicity.png
  :alt: Hydrophobicity



.. image:: _static/plots/Enclosure.png
  :alt: Enclosure



Inspection of pocket volumes of the best 1000 pockets 
'''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: bash
    
    poke ref.gro ligands.xtc -dvp -ss protein -a protein -so all --sort score -ls -o all_best_1000 -n 1000

The output includes ``descriptors.csv``, ``structure.pdb``, ``volumes.pdb``, and a ``pymol.pml`` session file that reads ``structure.pdb`` and ``volumes.pdb`` directly to visualize the pockets.
``Descriptors.csv`` contains parameters that define the inspected pockets, such as the trajectory frame in which they were detected, their score, volume, and hydrophobicity. It also contains information about the residues and atoms that make up the pockets.

.. note:: 

  It is important to mention that Poké can detect multiple pocket conformations within a single trajectory. These conformations can either have a different shape or be an extension of a pre-existing pocket.

An example of two pockets that share the same trajectory frame are shown here:

.. raw:: html

  <div style="display:flex; gap:16px; align-items:flex-start;">
    <div id="viewport1" style="width:800px; height:600px; border:1px solid #ccc;"></div>

    <div id="menu" style="font-family:Arial, sans-serif;">
      <h3>Select pocket conformation</h3>
      <label><input type="checkbox" id="p40"> Conformation 1</label><br>
      <label><input type="checkbox" id="p462"> Conformation 2</label><br><br>

      <button id="resetView1">Reset view</button>
      <div id="status1" style="margin-top:12px; font-size:0.9em; color:#333;"></div>
    </div>
  </div>

  <script src="https://unpkg.com/ngl@latest/dist/ngl.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      // --- configure paths here (try the first; if 404s occur, try the alternative list below) ---
      var structures = {
        p40: "_static/pockets/p40_prot-pocket.pdb",
        p462: "_static/pockets/p462_prot-pocket.pdb"
      };

      var status1 = document.getElementById('status1');
      function setStatus(msg, isError) {
        status1.textContent = msg;
        status1.style.color = isError ? 'crimson' : '#333';
        console.log(msg);
      }

      // Create stage (use DOM element reference)
      var stage1;
      try {
        stage1 = new NGL.Stage(document.getElementById('viewport1'), { backgroundColor: "white" });
      } catch (e) {
        setStatus("Error creating NGL stage: " + e.message, true);
        throw e;
      }

      window.addEventListener('resize', function() { stage1.handleResize(); }, false);

      var loaded = {}; // store components by name

      // pick distinct colors for quick visual separation
      var colors = { p40: "red", p462: "blue" };

      // safe loader with logging
      function loadStructure(name) {
        setStatus("Loading " + name + " ...");
        return stage1.loadFile(structures[name]).then(function(comp) {
          loaded[name] = comp;
          comp.setName(name);
          // add a cartoon representation; if you want spheres/surfaces adjust here
          comp.addRepresentation('cartoon', { color: colors[name] || 'chainname' });
          comp.addRepresentation('surface', { sele: 'all and not 1-799', opacity: 0.3, color: colors[name] || 'chainname' });
          comp.autoView();
          setStatus(name + " loaded.");
          return comp;
        }).catch(function(err){
          setStatus("Failed to load " + name + " — check path and network (see console).", true);
          console.error("NGL load error for", name, err);
          throw err;
        });
      }

      // toggle function bound to checkboxes
      function toggleStructure(name, checked) {
        if (checked) {
          if (loaded[name]) {
            loaded[name].setVisibility(true);
            setStatus(name + " shown.");
            stage1.autoView();
          } else {
            loadStructure(name).then(() => stage1.autoView()).catch(()=>{});
          }
        } else {
          if (loaded[name]) {
            loaded[name].setVisibility(false);
            setStatus(name + " hidden.");
          } else {
            setStatus(name + " is not loaded yet.");
          }
        }
      }

      // wire checkboxes
      ['p40','p462'].forEach(function(name){
        var cb = document.getElementById(name);
        if (!cb) {
          console.warn("Checkbox not found for", name);
          return;
        }
        cb.addEventListener('change', function(e){
          toggleStructure(name, e.target.checked);
        });
      });

      document.getElementById('resetView1').addEventListener('click', function() {
        stage1.autoView();
      });

      // Helpful: try preloading none, or preload one (uncomment if you want p15 preloaded by default)
      // loadStructure('p15').catch(()=>{});
      setStatus("Ready — toggle boxes to load/show structures. Open browser console / network tab if something fails.");
    });
  </script>



Two examples of pockets identified through visual inspection are shown below:

.. raw:: html

  <div style="display:flex; gap:16px; align-items:flex-start;">
    <div id="viewport2" style="width:800px; height:600px; border:1px solid #ccc;"></div>

    <div id="menu" style="font-family:Arial, sans-serif;">
      <h3>Select protein conformation</h3>
      <label><input type="checkbox" id="p12"> Conformation 3</label><br>
      <label><input type="checkbox" id="p63"> Conformation 4</label><br><br>

      <button id="resetView2">Reset view</button>
      <div id="status2" style="margin-top:12px; font-size:0.9em; color:#333;"></div>
    </div>
  </div>

  <script src="https://unpkg.com/ngl@latest/dist/ngl.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      // --- configure paths here (try the first; if 404s occur, try the alternative list below) ---
      var structures = {
        p12: "_static/pockets/p12_prot-pocket.pdb",
        p63: "_static/pockets/p63_prot-pocket.pdb"
      };

      var status2 = document.getElementById('status2');
      function setStatus(msg, isError) {
        status2.textContent = msg;
        status2.style.color = isError ? 'crimson' : '#333';
        console.log(msg);
      }

      // Create stage (use DOM element reference)
      var stage2;
      try {
        stage2 = new NGL.Stage(document.getElementById('viewport2'), { backgroundColor: "white" });
      } catch (e) {
        setStatus("Error creating NGL stage: " + e.message, true);
        throw e;
      }

      window.addEventListener('resize', function() { stage2.handleResize(); }, false);

      var loaded = {}; // store components by name

      // pick distinct colors for quick visual separation
      var colors = { p12: "red", p63: "blue" };

      // safe loader with logging
      function loadStructure(name) {
        setStatus("Loading " + name + " ...");
        return stage2.loadFile(structures[name]).then(function(comp) {
          loaded[name] = comp;
          comp.setName(name);
          // add a cartoon representation; if you want spheres/surfaces adjust here
          comp.addRepresentation('cartoon', { color: colors[name] || 'chainname' });
          comp.addRepresentation('surface', { sele: 'all and not 1-799', opacity: 0.3, color: colors[name] || 'chainname' });
          comp.autoView();
          setStatus(name + " loaded.");
          return comp;
        }).catch(function(err){
          setStatus("Failed to load " + name + " — check path and network (see console).", true);
          console.error("NGL load error for", name, err);
          throw err;
        });
      }

      // toggle function bound to checkboxes
      function toggleStructure(name, checked) {
        if (checked) {
          if (loaded[name]) {
            loaded[name].setVisibility(true);
            setStatus(name + " shown.");
            stage2.autoView();
          } else {
            loadStructure(name).then(() => stage2.autoView()).catch(()=>{});
          }
        } else {
          if (loaded[name]) {
            loaded[name].setVisibility(false);
            setStatus(name + " hidden.");
          } else {
            setStatus(name + " is not loaded yet.");
          }
        }
      }

      // wire checkboxes
      ['p12','p63'].forEach(function(name){
        var cb = document.getElementById(name);
        if (!cb) {
          console.warn("Checkbox not found for", name);
          return;
        }
        cb.addEventListener('change', function(e){
          toggleStructure(name, e.target.checked);
        });
      });

      document.getElementById('resetView2').addEventListener('click', function() {
        stage2.autoView();
      });

      // Helpful: try preloading none, or preload one (uncomment if you want p15 preloaded by default)
      // loadStructure('p15').catch(()=>{});
      setStatus("Ready — toggle boxes to load/show structures. Open browser console / network tab if something fails.");
    });
  </script>




Identification of pockets on the cryptic site
'''''''''''''''''''''''''''''''''''''''''''''

Using PDB ID 1PZO as a reference to understand the position of the cryptic pocket, we identified some pockets in the cryptic area in our simulations. In particular, pockets 15, 26, 31, 34, and 67 of the top 1,000 contain benzene molecules. Using the descriptors.csv file, we extracted the residues common to pockets 15, 26, 31, 34, and 67 that define the cryptic region. We then ran poké again with this residue definition:

Residue definition= [225,290,229,230,231,261,263,250,251,279,248,282,283,221,286,287]

.. code-block:: bash
    
    poke ref.gro ligands.xtc -dg -ss protein -a protein -so all --sort score -ls -f 'len(resids & {225,290,229,230,231,261,263,250,251,279,248,282,283,221,286,287})>6' -o table-common
    # to get the total number of pockets found and the distribution of pocket descriptors.
    poke ref.gro ligands.xtc -dvp -ss protein -a protein -so all --sort score -ls -f 'len(resids & {225,290,229,230,231,261,263,250,251,279,248,282,283,221,286,287})>6'  -n 300 -o table-common
    # to get the best 300 pockets and afterwards do visual inspection of them


.. raw:: html

  <div style="display:flex; gap:16px; align-items:flex-start;">
    <div id="viewport3" style="width:800px; height:600px; border:1px solid #ccc;"></div>

    <div id="menu" style="font-family:Arial, sans-serif;">
      <h3>Select protein conformation</h3>
      <label><input type="checkbox" id="p15"> Conformation 5</label><br>
      <label><input type="checkbox" id="p26"> Conformation 6</label><br>
      <label><input type="checkbox" id="p31"> Conformation 7</label><br>
      <label><input type="checkbox" id="p34"> Conformation 8</label><br>
      <label><input type="checkbox" id="p67"> Conformation 9</label><br><br>

      <button id="resetView3">Reset view</button>
      <div id="status3" style="margin-top:12px; font-size:0.9em; color:#333;"></div>
    </div>
  </div>

  <script src="https://unpkg.com/ngl@latest/dist/ngl.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      // --- configure paths here (try the first; if 404s occur, try the alternative list below) ---
      var structures = {
        p15: "_static/pockets/p15_prot-pocket.pdb",
        p26: "_static/pockets/p26_prot-pocket.pdb",
        p31: "_static/pockets/p31_prot-pocket.pdb",
        p34: "_static/pockets/p34_prot-pocket.pdb",
        p67: "_static/pockets/p67_prot-pocket.pdb"
      };

      var status3 = document.getElementById('status3');
      function setStatus(msg, isError) {
        status3.textContent = msg;
        status3.style.color = isError ? 'crimson' : '#333';
        console.log(msg);
      }

      // Create stage (use DOM element reference)
      var stage3;
      try {
        stage3 = new NGL.Stage(document.getElementById('viewport3'), { backgroundColor: "white" });
      } catch (e) {
        setStatus("Error creating NGL stage: " + e.message, true);
        throw e;
      }

      window.addEventListener('resize', function() { stage3.handleResize(); }, false);

      var loaded = {}; // store components by name

      // pick distinct colors for quick visual separation
      var colors = { p15: "red", p26: "blue", p31: "green", p34: "orange", p67: "purple" };

      // safe loader with logging
      function loadStructure(name) {
        setStatus("Loading " + name + " ...");
        return stage3.loadFile(structures[name]).then(function(comp) {
          loaded[name] = comp;
          comp.setName(name);
          // add a cartoon representation; if you want spheres/surfaces adjust here
          comp.addRepresentation('cartoon', { color: colors[name] || 'chainname' });
          comp.addRepresentation('surface', { sele: 'all and not 1-799', opacity: 0.3, color: colors[name] || 'chainname' });
          comp.autoView();
          setStatus(name + " loaded.");
          return comp;
        }).catch(function(err){
          setStatus("Failed to load " + name + " — check path and network (see console).", true);
          console.error("NGL load error for", name, err);
          throw err;
        });
      }

      // toggle function bound to checkboxes
      function toggleStructure(name, checked) {
        if (checked) {
          if (loaded[name]) {
            loaded[name].setVisibility(true);
            setStatus(name + " shown.");
            stage3.autoView();
          } else {
            loadStructure(name).then(() => stage3.autoView()).catch(()=>{});
          }
        } else {
          if (loaded[name]) {
            loaded[name].setVisibility(false);
            setStatus(name + " hidden.");
          } else {
            setStatus(name + " is not loaded yet.");
          }
        }
      }

      // wire checkboxes
      ['p15','p26','p31','p34','p67'].forEach(function(name){
        var cb = document.getElementById(name);
        if (!cb) {
          console.warn("Checkbox not found for", name);
          return;
        }
        cb.addEventListener('change', function(e){
          toggleStructure(name, e.target.checked);
        });
      });

      document.getElementById('resetView3').addEventListener('click', function() {
        stage3.autoView();
      });

      // Helpful: try preloading none, or preload one (uncomment if you want p15 preloaded by default)
      // loadStructure('p15').catch(()=>{});
      setStatus("Ready — toggle boxes to load/show structures. Open browser console / network tab if something fails.");
    });
  </script>






Due to benzene scouting, a total of 827,542 pocket conformations were found in the cryptic area. Of these conformations, 157,749 belong to the same trajectory frame. On average, all pocket conformations inspected from the top 300 present a volume of 96 Å³, a score of 6.6 a.u., a hydrophobicity of 0.92 a.u., and an Enclosure of 0.95 a.u., meaning that the pockets are quite buried and apolar, as expected.

.. raw:: html

  <div style="display:flex; gap:16px; align-items:flex-start;">
    <div id="viewport4" style="width:800px; height:600px; border:1px solid #ccc;"></div>

    <div id="menu" style="font-family:Arial, sans-serif;">
      <h3>Select protein conformation</h3>
      <label><input type="checkbox" id="p9"> Conformation 10</label><br>
      <label><input type="checkbox" id="p41"> Conformation 11</label><br><br>

      <button id="resetView4">Reset view</button>
      <div id="status4" style="margin-top:12px; font-size:0.9em; color:#333;"></div>
    </div>
  </div>

  <script src="https://unpkg.com/ngl@latest/dist/ngl.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      // --- configure paths here (try the first; if 404s occur, try the alternative list below) ---
      var structures = {
        p9: "_static/pockets/p9_prot-pocket.pdb",
        p41: "_static/pockets/p41_prot-pocket.pdb"
      };

      var status4 = document.getElementById('status4');
      function setStatus(msg, isError) {
        status4.textContent = msg;
        status4.style.color = isError ? 'crimson' : '#333';
        console.log(msg);
      }

      // Create stage (use DOM element reference)
      var stage4;
      try {
        stage4 = new NGL.Stage(document.getElementById('viewport4'), { backgroundColor: "white" });
      } catch (e) {
        setStatus("Error creating NGL stage: " + e.message, true);
        throw e;
      }

      window.addEventListener('resize', function() { stage4.handleResize(); }, false);

      var loaded = {}; // store components by name

      // pick distinct colors for quick visual separation
      var colors = { p9: "red", p41: "blue" };

      // safe loader with logging
      function loadStructure(name) {
        setStatus("Loading " + name + " ...");
        return stage4.loadFile(structures[name]).then(function(comp) {
          loaded[name] = comp;
          comp.setName(name);
          // add a cartoon representation; if you want spheres/surfaces adjust here
          comp.addRepresentation('cartoon', { color: colors[name] || 'chainname' });
          comp.addRepresentation('surface', { sele: 'all and not 1-799', opacity: 0.3, color: colors[name] || 'chainname' });
          comp.autoView();
          setStatus(name + " loaded.");
          return comp;
        }).catch(function(err){
          setStatus("Failed to load " + name + " — check path and network (see console).", true);
          console.error("NGL load error for", name, err);
          throw err;
        });
      }

      // toggle function bound to checkboxes
      function toggleStructure(name, checked) {
        if (checked) {
          if (loaded[name]) {
            loaded[name].setVisibility(true);
            setStatus(name + " shown.");
            stage4.autoView();
          } else {
            loadStructure(name).then(() => stage4.autoView()).catch(()=>{});
          }
        } else {
          if (loaded[name]) {
            loaded[name].setVisibility(false);
            setStatus(name + " hidden.");
          } else {
            setStatus(name + " is not loaded yet.");
          }
        }
      }

      // wire checkboxes
      ['p9','p41'].forEach(function(name){
        var cb = document.getElementById(name);
        if (!cb) {
          console.warn("Checkbox not found for", name);
          return;
        }
        cb.addEventListener('change', function(e){
          toggleStructure(name, e.target.checked);
        });
      });

      document.getElementById('resetView4').addEventListener('click', function() {
        stage4.autoView();
      });

      // Helpful: try preloading none, or preload one (uncomment if you want p15 preloaded by default)
      // loadStructure('p15').catch(()=>{});
      setStatus("Ready — toggle boxes to load/show structures. Open browser console / network tab if something fails.");
    });
  </script>




.. bibliography::
  :filter: docname in docnames