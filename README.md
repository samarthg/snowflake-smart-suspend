=======================
Snowflake-Smart-Suspend
=======================

Snowflake-Smart-Suspend intelligently suspends the running warehouse which are not being used and reaching hour boundary.
Currently designed for warehouses with auto-resume enabled and without auto-suspend for better optimisation.

Usage and Details
============================

Installation::

    pip install snowflake-smart-suspend

Typical usage often looks like this::

    smart_suspend start -c connections -r <role which has access to warehouses of interest> -s 55 -i 30 -w <space separated list of warehouses>

You can find the details about all the options with::

    smart_suspend -h
    smart_suspend --help

Configurations
==============
If you have snowsql installed and running on the server ``smart-suspend`` will work *out of the box*
If not you will have to have file at location ``HOME/.snowsql/config`` with snowflake cred::

    [connections]
    accountname = <account name>
    username = <username>
    password = <password>

Logging
==============
Logs could be find in ``/var/log/smartsuspend/system.log``. You might need to adjust the permissions to log directory during installation.

Dependancies
============

* Its written for Python3 which is the present and future of the language