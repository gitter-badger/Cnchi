#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  updater.py
#
#  Copyright © 2013,2014 Antergos
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

""" Module to update Cnchi """

import urllib

import json
import hashlib
import os
import info
import logging
import shutil
import canonical.misc as misc

import download

_update_info_url = "https://raw.github.com/Antergos/Cnchi/master/update.info"
_master_zip_url = "https://github.com/Antergos/Cnchi/archive/master.zip"

_src_dir = os.path.dirname(__file__) or '.'
_base_dir = os.path.join(_src_dir, "..")

def get_md5_from_file(filename):
    with open(filename, 'rb') as myfile:
        buf = myfile.read()
        md5 = get_md5_from_text(buf)
    return md5
        
def get_md5_from_text(text):
    """ Gets md5 hash from str """
    md5 = hashlib.md5()
    md5.update(text)
    return md5.hexdigest()
 
class Updater():
    def __init__(self, force_update):
        self.remote_version = ""
        
        self.md5s = {}
        
        # Get local info (local update.info)
        with open("/usr/share/cnchi/update.info", "r") as local_update_info:
            response = local_update_info.read()
            if len(response) > 0:
                updateInfo = json.loads(response)
                self.local_files = updateInfo['files']

        # Download update.info (contains info of all Cnchi's files)
        request = download.url_open(_update_info_url)
        
        if request is not None:
            response = request.read().decode('utf-8')
            if len(response) > 0:
                updateInfo = json.loads(response)
                self.remote_version = updateInfo['version']
                for remote_file in updateInfo['files']:
                    self.md5s[remote_file['name']] = remote_file['md5']
                
                logging.info(_("Cnchi Internet version: %s"), self.remote_version)
                self.force = force_update

    def is_remote_version_newer(self):
        """ Returns true if the Internet version of Cnchi is newer than the local one """
        if self.force:
             return True

        # Version is always: x.y.z
        local_ver = info.CNCHI_VERSION.split(".")
        remote_ver = self.remote_version.split(".")

        local = [int(local_ver[0]), int(local_ver[1]), int(local_ver[2])]
        remote = [int(remote_ver[0]), int(remote_ver[1]), int(remote_ver[2])]

        if remote[0] > local[0]:
            return True

        if remote[0] == local[0] and remote[1] > local[1]:
            return True

        if remote[0] == local[0] and remote[1] == local[1] and remote[2] > local[2]:
            return True

        return False

    def should_update_local_file(self, remote_name, remote_md5):
        """ Checks if remote file is different from the local one (just compares md5)"""
        for local_file in self.local_files:
            if local_file['name'] == remote_name and local_file['md5'] != remote_md5 and '__' not in local_file['name']:
                return True
        return False

    def update(self):
        ''' Check if a new version is available and
            update all files only if necessary (or forced) '''
        update_cnchi = False
        
        if self.force:
            logging.info(_("Updating installer with the Internet version..."))
            update_cnchi = True
        elif self.is_remote_version_newer():
            logging.info(_("New version found. Updating installer..."))
            update_cnchi = True

            if update_cnchi:
                res = self.download_master_zip()
                if not res:
                    logging.error(_("Can't download new Cnchi version."))
                    return False

        return update_cnchi

    def download_master_zip(self):
        """ Download new Cnchi version from github """
        request = download.url_open(_master_zip_url)
        
        if request is None:
            return False

        dst_path = "/tmp/cnchi-%s.zip" % self.remote_version

        logging.debug(_("Downloading new version of Cnchi..."))
        if not os.path.exists(dst_path):
            with open(dst_path, 'wb') as zip_file:
                (data, error) = download.url_open_read(request)

                while len(data) > 0 and error == False:
                    zip_file.write(data)
                    (data, error) = download.url_open_read(request)
                
                if error:
                     return False
        
        # master.zip file is downloaded, we must unzip it
        logging.debug(_("Uncompressing new version..."))
        try:
            self.unzip_and_copy(dst_path, "/tmp")
        except Exception as err:
            logging.error(err)
            return False
        
        return True

    def unzip_and_copy(self, zip_path, dst_dir):
        """ Unzip (decompress) a zip file using zipfile standard module """       
        import zipfile

        with zipfile.ZipFile(zip_path) as zip_file:
            for member in zip_file.infolist():
                zip_file.extract(member, dst_dir)
                full_path = os.path.join(dst_dir, member.filename)
                dst_full_path = os.path.join("/usr/share/cnchi", full_path.split("/tmp/Cnchi-master/")[1])
                if os.path.isfile(dst_full_path):
                    if dst_full_path in self.md5s:
                        md5 = get_md5_from_file(full_path)
                        if self.md5s[dst_full_path] == md5:
                            #print(full_path, dst_full_path, md5)
                            try:
                                with misc.raised_privileges():
                                    shutil.copyfile(full_path, dst_full_path)
                            except FileNotFoundError:
                                logging.error(_("Can't copy %s to %s"), full_path, dst_full_path)
