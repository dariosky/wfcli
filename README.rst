wfcli
=====

A way to automate app/website/domain hosted in
`WebFaction <https://www.webfaction.com/?aid=4937>`__ from Python or
from the command line.

Features
--------

-  Transfer insecure domains from http to https creating the
   certificates with `LetsEncrypt <https://letsencrypt.org/>`__. Using
   the `acme.sh <https://github.com/Neilpang/acme.sh>`__.

Installation
------------

Install via PYPI:

::

    pip install wfcli

Webfaction authentication
-------------------------

You should be able to access the webfaction host via ssh and provide the
username and password of the control panel to access via API.

You can use the ``--webfaction-host``, ``--webfaction-user``,
``--webfaction-password`` to set the credentials, or you can define the
environment variables WEBFACTION\_USER, WEBFACTION\_PASS,
WEBFACTION\_HOST

If you have multiple WebFaction machines, you can specify the machine
name for connecting via API in WEBFACTION\_MACHINE\_NAME environment
variable.

Usage examples:
---------------

The examples below assume you already set the environment variable or
you're authenticated via the auth parameters.

Convert a domain <yourdomain.com>, an all subdomains to https:

::

    wfcli secure <yourdomain.com>

This will do all the required passages: \* install acme.sh on the
WebFaction host \*
