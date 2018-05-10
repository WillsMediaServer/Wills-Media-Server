Installation
************

To install Wills Media Server you will need some technical knowledge at this
moment in time.

Requirements
============

You will need these dependencies to run WillsMediaServer.

- Python >= 3.5
- pip
- ffmpeg
- A Working Computer

Method 1 (The Hardish way)
==========================

1. Clone the repository then cd into it::

    git clone https://github.com/WillsMediaServer/WMS-Core
    cd WMS-Core

2. Download all dependencies::

    pip install -r requirements.txt

3. Download and build WMS-UI in the libraries folder::

    cd libraries/
    git clone https://github.com/WillsMediaServer/WMS-UI
    cd WMS-UI
    npm install
    npm run build

4. Start it::

    cd ../../
    python start.py

.. note::
    If you dont want to install the packages globally you can install them to the
    libraries directory with ``pip install -r requirements.txt --target=libraries/``
    from the WMS root directory

Method 2 (The easier way)
=========================

.. note::
    The Easier way hasn't been created yet - TODO

    - Write docs on installer
    - Actually create an installer
