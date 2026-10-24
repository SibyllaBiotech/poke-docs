Welcome to the Poké user guide
==============================

.. toctree::
   :maxdepth: 2
   :hidden:

   Getting Started
   Descriptors
   Outputs
   Filters
   Structure Preparation
   CLI Reference
   Python Package
   Plugin
   Tutorials

.. image:: img/poke-banner.svg
   :alt: banner
   :width: 800px
   :align: center
   :class: banner

This guide documents Poké |release|.

**Poké** is a high-performance pocket scouting engine. It uses an energy-based approach to
identify low-energy regions on protein surfaces. These regions are characterized by a set of
physical descriptors, which are used by a neural network to assign a ligandability score to
the pocket.

It is designed to be used on long molecular dynamics trajectories, but it works equally well
on single frames.

**Get Started**

If you are new to Poké, start here:

* :doc:`Getting Started` to install the package and run it on a structure or a trajectory
* :doc:`Tutorials` for a worked example on a cryptic pocket of TEM-1 β-lactamase

**How to cite**

If you use Poké in your research, please cite:

   Colasurdo, E., Boldrini, A., Terruzzi, L., Langini, C., Risueño Fernández, C., Varricchio, C.,
   Primavera, E., Cassese, E., Patsilinakos, A. & Spagnolli, G. *Poké: Fast and Reliable
   Neural-Network-Based Identification of Protein Ligandable Sites.* ACS Omega (2026).
   https://doi.org/10.1021/acsomega.6c04816

**Code and data**

* Source code on GitHub: https://github.com/SibyllaBiotech/poke
* Source of this guide on GitHub: https://github.com/SibyllaBiotech/poke-docs
* Source code archived on Zenodo: https://doi.org/10.5281/zenodo.19634786
* Datasets used in the paper, on Zenodo: https://doi.org/10.5281/zenodo.19635030

**Licence**

Poké is free software released under the `MIT licence
<https://github.com/SibyllaBiotech/poke/blob/main/LICENSE>`_. The text and figures of this
guide are released under the `CC BY 4.0 <https://creativecommons.org/licenses/by/4.0/>`_ licence.
