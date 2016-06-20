# rheem_controller

## CI Status

[![Build Status](https://travis-ci.org/spresse1/rheem_controller.svg?branch=master)](https://travis-ci.org/spresse1/rheem_controller)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/442183750d6e495abfbc0eb5e21a2242)](https://www.codacy.com/app/spresse1/rheem_controller?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=spresse1/rheem_controller&amp;utm_campaign=Badge_Coverage)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/442183750d6e495abfbc0eb5e21a2242)](https://www.codacy.com/app/spresse1/rheem_controller)

## Purpose

This project aims to provide a pythonic interface to the Rheem EcoNet API (http://io.myrheem.com/).  (Yes, their web page is terribly designed.  To access the API we will be interfacing, select 'EcoNet' in the dropdown, then wait for the page to reload).  This project aims to eventually provide more advanced control - such as schedules.  It also hopes to provide an API suitable for use with larger home automation projects.

## Installation

Pending.  Will be `pip install rheem_controller`

## Use

See API documentation.

## Dev installation

In the root directory, run:
```shell
pip install -U virtualenv
virtualenv .
. bin/activate
pip install -r requirements.txt -r dev-requirements.txt
```

## Documentation
To build the documentation, run:
`tox -e docs`

To build a target other than html, set the environment variable DOC_TARGET.  Valid values are the same as those for sphinx.

## Testing
To test, run either:

1. `tox` (preferred)
2. `py.test test`

This module should have a 100% test coverage and tests are set to fail if this is not the case.

### Modifying tests

All tests are currently located in tests/ and any tests using python's unittest module placed in this directory should run.


