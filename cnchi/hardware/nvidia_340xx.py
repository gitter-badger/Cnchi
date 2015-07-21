#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  nvidia.py
#
#  Copyright © 2013-2015 Antergos
#
#  This file is part of Cnchi.
#
#  Cnchi is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Cnchi is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Cnchi; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Nvidia (propietary) driver installation """

try:
    from hardware.hardware import Hardware
except ImportError:
    from hardware import Hardware

import os

CLASS_NAME = "Nvidia_340xx"
CLASS_ID = "0x0300"
VENDOR_ID = "0x10de"

# Give this driver more priority so it is chosen instead of nvidia-304xx
# (when both are possible)
PRIORITY = 1

# See https://wiki.archlinux.org/index.php/NVIDIA#Installing
# nvidia, nvidia-340xx, nvidia-304xx
# lib32-nvidia-libgl, lib32-nvidia-340xx-libgl or lib32-nvidia-304xx-libgl

"""
For GeForce 8000/9000 and 100-300 series cards [NV5x, NV8x, NV9x and NVAx] from
    around 2006-2010, install the nvidia-340xx or nvidia-340xx-lts package along
    with nvidia-340xx-libgl, available in the official repositories.
"""

DEVICES=[
    "0x0191", "0x0193", "0x0194", "0x0197", "0x019d", "0x019e", "0x0400",
    "0x0401", "0x0402", "0x0403", "0x0404", "0x0405", "0x0406", "0x0407",
    "0x0408", "0x0409", "0x040a", "0x040b", "0x040c", "0x040d", "0x040e",
    "0x040f", "0x0410", "0x0420", "0x0421", "0x0422", "0x0423", "0x0424",
    "0x0425", "0x0426", "0x0427", "0x0428", "0x0429", "0x042a", "0x042b",
    "0x042c", "0x042d", "0x042e", "0x042f", "0x05e0", "0x05e1", "0x05e2",
    "0x05e3", "0x05e6", "0x05e7", "0x05ea", "0x05eb", "0x05ed", "0x05f8",
    "0x05f9", "0x05fd", "0x05fe", "0x05ff", "0x0600", "0x0601", "0x0602",
    "0x0603", "0x0604", "0x0605", "0x0606", "0x0607", "0x0608", "0x0609",
    "0x060a", "0x060b", "0x060c", "0x060d", "0x060f", "0x0610", "0x0611",
    "0x0612", "0x0613", "0x0614", "0x0615", "0x0617", "0x0618", "0x0619",
    "0x061a", "0x061b", "0x061c", "0x061d", "0x061e", "0x061f", "0x0621",
    "0x0622", "0x0623", "0x0625", "0x0626", "0x0627", "0x0628", "0x062a",
    "0x062b", "0x062c", "0x062d", "0x062e", "0x0630", "0x0631", "0x0632",
    "0x0635", "0x0637", "0x0638", "0x063a", "0x0640", "0x0641", "0x0643",
    "0x0644", "0x0645", "0x0646", "0x0647", "0x0648", "0x0649", "0x064a",
    "0x064b", "0x064c", "0x0651", "0x0652", "0x0653", "0x0654", "0x0658",
    "0x0659", "0x065a", "0x065b", "0x065c", "0x06c0", "0x06c4", "0x06ca",
    "0x06cd", "0x06d1", "0x06d2", "0x06d8", "0x06d9", "0x06da", "0x06dc",
    "0x06dd", "0x06de", "0x06df", "0x06e0", "0x06e1", "0x06e2", "0x06e3",
    "0x06e4", "0x06e5", "0x06e6", "0x06e7", "0x06e8", "0x06e9", "0x06ea",
    "0x06eb", "0x06ec", "0x06ef", "0x06f1", "0x06f8", "0x06f9", "0x06fa",
    "0x06fb", "0x06fd", "0x06ff", "0x0840", "0x0844", "0x0845", "0x0846",
    "0x0847", "0x0848", "0x0849", "0x084a", "0x084b", "0x084c", "0x084d",
    "0x084f", "0x0860", "0x0861", "0x0862", "0x0863", "0x0864", "0x0865",
    "0x0866", "0x0867", "0x0868", "0x0869", "0x086a", "0x086c", "0x086d",
    "0x086e", "0x086f", "0x0870", "0x0871", "0x0872", "0x0873", "0x0874",
    "0x0876", "0x087a", "0x087d", "0x087e", "0x087f", "0x08a0", "0x08a2",
    "0x08a3", "0x08a4", "0x08a5", "0x0a20", "0x0a22", "0x0a23", "0x0a26",
    "0x0a27", "0x0a28", "0x0a29", "0x0a2a", "0x0a2b", "0x0a2c", "0x0a2d",
    "0x0a32", "0x0a34", "0x0a35", "0x0a38", "0x0a3c", "0x0a60", "0x0a62",
    "0x0a63", "0x0a64", "0x0a65", "0x0a66", "0x0a67", "0x0a68", "0x0a69",
    "0x0a6a", "0x0a6c", "0x0a6e", "0x0a6f", "0x0a70", "0x0a71", "0x0a72",
    "0x0a73", "0x0a74", "0x0a75", "0x0a76", "0x0a78", "0x0a7a", "0x0a7c",
    "0x0ca0", "0x0ca2", "0x0ca3", "0x0ca4", "0x0ca5", "0x0ca7", "0x0ca8",
    "0x0ca9", "0x0cac", "0x0caf", "0x0cb0", "0x0cb1", "0x0cbc", "0x0dc0",
    "0x0dc4", "0x0dc5", "0x0dc6", "0x0dcd", "0x0dce", "0x0dd1", "0x0dd2",
    "0x0dd3", "0x0dd6", "0x0dd8", "0x0dda", "0x0de0", "0x0de1", "0x0de2",
    "0x0de3", "0x0de4", "0x0de5", "0x0de7", "0x0de8", "0x0de9", "0x0dea",
    "0x0deb", "0x0dec", "0x0ded", "0x0dee", "0x0def", "0x0df0", "0x0df1",
    "0x0df2", "0x0df3", "0x0df4", "0x0df5", "0x0df6", "0x0df7", "0x0df8",
    "0x0df9", "0x0dfa", "0x0dfc", "0x0e22", "0x0e23", "0x0e24", "0x0e30",
    "0x0e31", "0x0e3a", "0x0e3b", "0x0f00", "0x0f01", "0x0f02", "0x0fc0",
    "0x0fc1", "0x0fc2", "0x0fc6", "0x0fc8", "0x0fcd", "0x0fce", "0x0fd1",
    "0x0fd2", "0x0fd3", "0x0fd4", "0x0fd5", "0x0fd8", "0x0fd9", "0x0fdf",
    "0x0fe0", "0x0fe1", "0x0fe2", "0x0fe3", "0x0fe4", "0x0fe9", "0x0fea",
    "0x0fec", "0x0fef", "0x0ff2", "0x0ff3", "0x0ff6", "0x0ff8", "0x0ff9",
    "0x0ffa", "0x0ffb", "0x0ffc", "0x0ffd", "0x0ffe", "0x0fff", "0x1001",
    "0x1004", "0x1005", "0x1007", "0x1008", "0x100a", "0x100c", "0x1021",
    "0x1022", "0x1023", "0x1024", "0x1026", "0x1027", "0x1028", "0x1029",
    "0x103a", "0x103c", "0x1040", "0x1042", "0x1048", "0x1049", "0x104a",
    "0x104b", "0x104c", "0x1050", "0x1051", "0x1052", "0x1054", "0x1055",
    "0x1056", "0x1057", "0x1058", "0x1059", "0x105a", "0x105b", "0x107c",
    "0x107d", "0x1080", "0x1081", "0x1082", "0x1084", "0x1086", "0x1087",
    "0x1088", "0x1089", "0x108b", "0x1091", "0x1094", "0x1096", "0x109a",
    "0x109b", "0x10c0", "0x10c3", "0x10c5", "0x10d8", "0x1180", "0x1183",
    "0x1184", "0x1185", "0x1187", "0x1188", "0x1189", "0x118a", "0x118e",
    "0x118f", "0x1193", "0x1194", "0x1195", "0x1198", "0x1199", "0x119a",
    "0x119d", "0x119e", "0x119f", "0x11a0", "0x11a1", "0x11a2", "0x11a3",
    "0x11a7", "0x11b4", "0x11b6", "0x11b7", "0x11b8", "0x11ba", "0x11bc",
    "0x11bd", "0x11be", "0x11bf", "0x11c0", "0x11c2", "0x11c3", "0x11c4",
    "0x11c5", "0x11c6", "0x11c8", "0x11e0", "0x11e1", "0x11e2", "0x11e3",
    "0x11fa", "0x11fc", "0x1200", "0x1201", "0x1203", "0x1205", "0x1206",
    "0x1207", "0x1208", "0x1210", "0x1211", "0x1212", "0x1213", "0x1241",
    "0x1243", "0x1244", "0x1245", "0x1246", "0x1247", "0x1248", "0x1249",
    "0x124b", "0x124d", "0x1251", "0x1280", "0x1281", "0x1282", "0x1284",
    "0x1286", "0x1287", "0x1288", "0x1290", "0x1291", "0x1292", "0x1293",
    "0x1295", "0x1296", "0x1298", "0x12b9", "0x12ba", "0x1340", "0x1341",
    "0x1380", "0x1381", "0x1382", "0x1390", "0x1391", "0x1392", "0x1393",
    "0x13ba", "0x13bb", "0x1140"]


class Nvidia_340xx(Hardware):
    def __init__(self):
        Hardware.__init__(self, CLASS_NAME, CLASS_ID, VENDOR_ID, DEVICES, PRIORITY)

    def get_packages(self):
        pkgs = ["nvidia-340xx", "nvidia-340xx-utils", "nvidia-340xx-libgl", "libvdpau", "libcl"]
        if os.uname()[-1] == "x86_64":
            pkgs.extend(["lib32-nvidia-340xx-libgl", "lib32-libvdpau"])
        return pkgs

    def post_install(self, dest_dir):
        path = os.path.join(dest_dir, "etc/X11/xorg.conf.d/20-nvidia.conf")
        with open(path, 'w') as nvidia:
            nvidia.write('Section "Device"\n')
            nvidia.write('    Identifier "Nvidia Card"\n')
            nvidia.write('    Driver "nvidia"\n')
            nvidia.write('    VendorName "NVIDIA Corporation"\n')
            nvidia.write('    Option "NoLogo" "true"\n')
            nvidia.write('EndSection\n')

    def is_proprietary(self):
        return True
