.. poké documentation master file, created by
   sphinx-quickstart on Tue Jul 15 12:04:06 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Poké documentation
=============================

.. toctree::
   :maxdepth: 2
   :hidden:

   Getting Started
   Descriptors
   Filters
   Python Package
   Plugin
   Tutorials

.. image:: img/poke-banner.png
   :alt: banner
   :width: 800px
   :align: center


**Poké scouter** is a blazing fast pocket scouter based on CHARMM forcefield. It uses an energy-based approach to identify the low-energy regions of the protein and it is able to compute a set of descriptors for each pocket useful to characterize it. The descriptors are used then by a neural network model to assign a druggability score to the pocket.

Designed to be used on long molecular dynamics trajectories, but it can be used also on single frames.

**Get Started**

If you are new to *poké*, explore the following resources to install ``poke`` package, access tutorials and dive into the documentation:
* :doc:`Getting Started`
* :doc:`Tutorials`

