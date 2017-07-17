#Leaf Network Mapper Utilities

A set of scripts for converting tracings of leaf venation into network structure.

##Contents

Leveraging existing methods for tracing leaf veins and measuring vein density, this repository includes scripts for data export from ImageJ and scripts run in Python3 to convert that data into a graph structure and calculate useful network metrics. Archived and draft versions of this code are also included.

##Dependencies

###Data Export

The data export protocol requires an image (in any format) that has been traced into an overlay in using the image processing program [ImageJ](https://imagej.net/Welcome). Scripts written to interface with ImageJ API rely on the Jython framework and are thus wrtten in Python2. They can be installed as plug-ins by placing them in `ImageJ.app/scripts/` or `ImageJ.app/plugins/Scripts`.

The data export process outputs a CSV file including every line segment ROI produced in tracing.

###Graph Generation and Analysis

Following data export, the `ROI_to_graph` is run in Python3, outside of ImageJ, and depends on the [`graph-tool`](https://graph-tool.skewed.de/) module. It exports a graph object (in `gt` file format, but with other options available). From here, `graph-tool` is used to calculate network metrics.

##To-Do

This repository is a work in progress representing the first component of my doctoral dissertation at the University of Minnesota. It is actively updated, and may contain bugs or idiosyncracies. Please contact if you have any
questions.

* Improved batch processing
* Better user interface options
* Refined network analysis, including implementation of flow models and fault tolerence testing.
* Improved final data export and storage
* Complete ImageJ integration
