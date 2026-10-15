/* Interactive pocket viewer used in the Tutorials page.
 * One call per viewer. config = {
 *   viewport: id of the <div> that holds the 3D view,
 *   status:   id of the <div> that shows messages,
 *   reset:    id of the "Reset view" button,
 *   structures: { checkboxId: "path/to/file.pdb", ... },
 *   colors:     { checkboxId: "red", ... }
 * }
 * Each checkbox id must match a key in `structures`. Requires NGL to be loaded first. */
function pokeViewer(config) {
  document.addEventListener('DOMContentLoaded', function () {
    var status = document.getElementById(config.status);
    function setStatus(msg, isError) {
      status.textContent = msg;
      status.style.color = isError ? 'crimson' : '#333';
      console.log(msg);
    }

    var stage;
    try {
      stage = new NGL.Stage(document.getElementById(config.viewport), { backgroundColor: "white" });
    } catch (e) {
      setStatus("Error creating NGL stage: " + e.message, true);
      throw e;
    }
    window.addEventListener('resize', function () { stage.handleResize(); }, false);

    var loaded = {};   // NGL components by checkbox id

    function loadStructure(name) {
      setStatus("Loading " + name + " ...");
      return stage.loadFile(config.structures[name]).then(function (comp) {
        loaded[name] = comp;
        comp.setName(name);
        var color = config.colors[name] || 'chainname';
        comp.addRepresentation('cartoon', { color: color });
        comp.addRepresentation('surface', { sele: 'all and not 1-799', opacity: 0.3, color: color });
        comp.autoView();
        setStatus(name + " loaded.");
        return comp;
      }).catch(function (err) {
        setStatus("Failed to load " + name + " — check path and network (see console).", true);
        console.error("NGL load error for", name, err);
        throw err;
      });
    }

    function toggleStructure(name, checked) {
      if (checked) {
        if (loaded[name]) {
          loaded[name].setVisibility(true);
          setStatus(name + " shown.");
          stage.autoView();
        } else {
          loadStructure(name).then(function () { stage.autoView(); }).catch(function () {});
        }
      } else if (loaded[name]) {
        loaded[name].setVisibility(false);
        setStatus(name + " hidden.");
      } else {
        setStatus(name + " is not loaded yet.");
      }
    }

    Object.keys(config.structures).forEach(function (name) {
      var cb = document.getElementById(name);
      if (!cb) { console.warn("Checkbox not found for", name); return; }
      cb.addEventListener('change', function (e) { toggleStructure(name, e.target.checked); });
    });

    document.getElementById(config.reset).addEventListener('click', function () { stage.autoView(); });

    setStatus("Ready — toggle boxes to load/show structures. Open browser console / network tab if something fails.");
  });
}
