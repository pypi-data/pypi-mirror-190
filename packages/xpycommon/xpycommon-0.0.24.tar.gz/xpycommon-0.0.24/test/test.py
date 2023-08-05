#!/usr/bin/env python

import sys

from xpycommon import ValNameDesc, ValNameDescs
from xpycommon.common import upgrade
from xpycommon.at_cmd import AtCode, AtCodes
from xpycommon.log import Logger, DEBUG
from xpycommon.ui import red
from xpycommon.bluetooth import oui_org_uap_to_naps

from xpycommon.android import adb_devices_long, check_single_adb_device
from xpycommon.android import get_adb_transport_ids



logger = Logger(__name__, DEBUG, filename='./log')


def main():
    """"""
    print(check_single_adb_device())
    print(get_adb_transport_ids())


if __name__ == '__main__':
    main()
