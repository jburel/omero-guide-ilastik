Use ilastik using Fiji scripting facility and OMERO
===================================================

Description
-----------

In this section, the segmentation (using Pixel classification routine
of ilastik) of the multi-z images is run in a batch mode.
For this we provide scripts which run ilastik in a headless mode. 
The scripts provide for ilastik a batch of images (coming from an OMERO Dataset) and ilastik is segmenting these
images according to the parameters configured and saved in the ``ilp`` in
the manual step above. We offer two scripts covering this workflow, one
running in Fiji, and the other using the python frames to export images
directly from OMERO to the ilastik running headlessly. Also, we describe
in this part how to use ilastik routine Object classification to
classify objects on images from OMERO manually.

We will show:

- How to run a script in Fiji, consuming the ``ilp`` file and running the segmentation of the images coming from an OMERO Dataset, 
- How to save the ROIs on the original images in OMERO.

Setup
-----

**ilastik installation**

- ilastik has been installed on the local machine. See \ https://www.ilastik.org/\  for details.

**ilastik plugin for Fiji installation instructions**

- Start Fiji. Update it (``Help > Update ImageJ``).
- in the ``Manage Update Sites`` check the checkbox next to the "ilastik" site.
- After the update was successful, restart your Fiji.
- The new ilastik menu item should be under Plugins menu.

Note: The ilastik menu item might be the last in the Plugins dropdown,
not necessarily alphabetically ordered.

**OMERO plugin for Fiji installation instructions**

- For installation instructions, go to `Fiji installation <https://omero-guides.readthedocs.io/en/latest/fiji/docs/installation.html>`_.

Resources
---------

-  Images from IDR `idr0062 <https://idr.openmicroscopy.org/search/?query=Name:idr0062>`_.

-  Groovy script :download:`analyse_dataset_ilastik.groovy <../scripts/analyse_dataset_ilastik.groovy>`

Step-by-step
------------

Scripting workflow on z-stacks using ilastik headless, Fiji and OMERO
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this example we will use the Groovy script :download:`analyse_dataset_ilastik.groovy <../scripts/analyse_dataset_ilastik.groovy>`.
The script uses the OMERO `JAVA API <https://docs.openmicroscopy.org/latest/omero/developers/Java.html>`_.

Connect to the server:

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Connect
    :end-before: // Load-images

Load the images contained in the specified dataset:

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Load-images
    :end-before: // Open-image

Open the images one-by-one using the Bio-Formats plugin:

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Open-image
    :end-before: // Check-exists

Export each image as h5 to a local folder specified interactively by the user during the run of the script. It is assumed that the folder specified by the user contains the ilastik Project prepared beforehand. The export is facilitated by the ilastik plugin for Fiji.

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Export as h5
    :end-before: // Close export


Start ilastik headless, using the ``Pixel classification`` module 
The script feeds into the ``Pixel classification`` ilastik module the ilastik Project created during the manual step and also the raw the new created h5 image in the step above.

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Import h5
    :end-before: // end pixel classification

The headless ilastik ``Pixel classification"`` module produces ``Probabilities`` map - this map is immediately opened into Fiji via the ilastik plugin for Fiji.

In Fiji, the Analyze Particles plugin is run on the "Probabilities" map to produce ROIs. 

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Analyse the images
    :end-before: // Save the ROIs


Once the ROIs are produced, they are saved to OMERO onto the original image which.

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Save-rois
    :end-before: // Beginning


Disconnect when done

.. literalinclude:: ../scripts/analyse_dataset_ilastik.groovy
    :start-after: // Close the connection
    :end-before: // End
