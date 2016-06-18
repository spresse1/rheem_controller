# rheem-controller

## CI Status

[![Build Status](https://travis-ci.org/spresse1/rheem-controller.svg?branch=master)](https://travis-ci.org/spresse1/rheem-controller)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/PROJECTMD5)](https://www.codacy.com/app/spresse1/remote_thermostat?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=spresse1/remote_thermostat&amp;utm_campaign=Badge_Coverage)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/PROJECTMD5)](https://www.codacy.com/app/steve_7/rheem-controller)

## Purpose

## Installation

## Use

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


