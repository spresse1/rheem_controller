#! /usr/bin/env python

import rheem_controller.rheem_auth
import getpass

if __name__ == "__main__":
    ra = rheem_controller.rheem_auth.RheemAuth()
    print("THIS PROGRAM TESTS AGAINST RHEEM'S LIVE API.  IT REQUIRES REAL "
          "CREDENTIALS.")
    username = getpass.getpass("Enter username (will not echo): ")
    password = getpass.getpass("Enter password (will not echo): ")
    ra.start_auth(username, password)
    print("Got token %s" % ra.token)
    assert(ra.token)
