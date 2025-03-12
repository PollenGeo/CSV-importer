=========================================
 OMERO Rectangle ROI Importer
=========================================

Description:
------------
This Python script connects to an OMERO server and allows users to import rectangular 
ROIs (Regions of Interest) from a CSV file. The extracted ROIs are added to the specified 
OMERO images and are set to be visible across all Z layers.

Features:
---------
- Connects to an OMERO server using user-provided credentials.
- Lists available OMERO groups and allows the user to switch groups.
- Reads and extracts rectangular ROIs from a CSV file.
- Uploads ROIs to the specified OMERO images, making them visible across all Z layers.

CSV File Format:
----------------
The CSV file must contain the following columns:

| Column      | Description                                       |
|------------ |---------------------------------------------------|
| image_id    | ID of the OMERO image where the ROI will be added. |
| type        | Type of ROI (must be "rectangle").                |
| X           | X-coordinate of the rectangle.                    |
| Y           | Y-coordinate of the rectangle.                    |
| Width       | Width of the rectangle.                           |
| Height      | Height of the rectangle.                          |

Requirements:
-------------
The script requires the following Python libraries:
- ezomero
- pandas
- omero-gateway
- tkinter (built-in for most Python distributions)

Installation:
-------------
Before running the script, install the required dependencies:

1. Install necessary Python packages:
pip install ezomero pip install pandas pip install omero-py

2. If `tkinter` is not installed, install it manually (Linux users only):
sudo apt-get install python3-tk

Usage:
------
1. Run the script:
python importcsv.py
2. Enter OMERO server credentials when prompted.
3. Select an OMERO group.
4. Choose a CSV file containing the ROIs.
5. The script will extract and upload ROIs to the specified images.
6. If the operation is successful, a confirmation message will be displayed.

Author:
-------
This script was developed by **Daurys De Alba**.

For inquiries, contact:
- Email: daurysdealbaherra@gmail.com
- Email: DeAlbaD@si.edu
