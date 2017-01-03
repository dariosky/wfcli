wfcli
=====

A way to automate app/website/domain hosted in
 [WebFaction](https://www.webfaction.com/?aid=4937)
 from Python or from the command line.

## Features

* Transfer insecure domains from http to https creating
 the certificates with [LetsEncrypt](https://letsencrypt.org/).
Using the [acme.sh](https://github.com/Neilpang/acme.sh).

 	
## Installation

Install via PYPI:
	
	pip install wfcli
	

## Webfaction authentication


You should be able to access the webfaction host via ssh and provide the username and
password of the control panel to access via API.

You can use the `--webfaction-host`, `--webfaction-user`, `--webfaction-password` to set the
credentials, or you can define the environment variables
WEBFACTION_USER, WEBFACTION_PASS, WEBFACTION_HOST

If you have multiple WebFaction machines, you can specify the machine name for connecting via API
in WEBFACTION_MACHINE_NAME environment variable.

## Usage examples:

The examples below assume you already set the environment variable or you're authenticated
via the auth parameters.

Convert a domain <yourdomain.com>, an all subdomains to https:
	
	wfcli secure <yourdomain.com>

This will do all the required passages:
* install acme.sh on the WebFaction host
* create a certificate with LetsEncrypt for the domain
and all the subdomains verifying it if needed
* add the certificate in the Webfaction CP
* clone all the insecure website as a secured copy with the new
certificate enabled
* Convert all the insecure website to a redirect to their secure counterpart

Two utility application will be created: one used to redirect the insecure sites to the secure ones,
another to verifify the domain with letsencrypt.

## API usage example:

The same thing can be done via Python:

```python
from wfcli import WebfactionWebsiteToSsl
w = WebfactionWebsiteToSsl()
w.secure(domain="yourdomain.com")
```
