Installation
************

To install Wills Media Server you will need some technical knowledge at this
moment in time.

Requirements
============

You will need these dependencies to run WillsMediaServer.

- Python >= 3.5
- Flask 1.0.2
- Flask_SQLAlchemy 2.3.2
- gevent 1.2.2
- ffmpeg
- A Working Computer

Method 1 (The Hardish way)
==========================

1. Clone the repository then cd into it::

    git clone https://github.com/WillsMediaServer/WMS-Core
    cd WMS-Core

2. Download all dependencies::

    pip install -r requirements.txt

3. Start it::

    python start.py

.. note::
    If you dont want to install the packages globally you can install them to the
    libraries directory with ``pip install -r requirements.txt --target=libraries/``
    from the WMS root directory

Method 2 (The easier way)
=========================

.. note::
    The Easier way hasn't been created yet

    - Write docs on installer
    - Actually create an installer
