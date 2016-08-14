#! /usr/bin/env python

import rheem_controller.auth
import getpass

if __name__ == "__main__":
    try:
        ra = rheem_controller.auth.Auth()
        print("THIS PROGRAM TESTS AGAINST RHEEM'S LIVE API.  IT REQUIRES REAL "
              "CREDENTIALS.")
        username = getpass.getpass("Enter username (will not echo): ")
        password = getpass.getpass("Enter password (will not echo): ")
        ra.start(username, password)
        print("Got token %s" % ra._access_token)
        assert(ra._access_token)
    except Exception as e:
        import pdb
        pdb.set_trace()
