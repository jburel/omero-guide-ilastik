#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2020 University of Dundee.
#
#   Redistribution and use in source and binary forms, with or without modification, 
#   are permitted provided that the following conditions are met:
# 
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#   Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
#   INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#   HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#   OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Version: 1.0
#

import numpy

import omero.clients
from omero.gateway import BlitzGateway

import time


# Connect to the server
def connect(hostname, username, password):
    conn = BlitzGateway(username, password,
                        host=hostname, secure=True)
    conn.connect()
    return conn


# Load-images
def load_images(conn, dataset_id):
    return conn.getObjects('Image', opts={'dataset': dataset_id})


def load_image(conn, image_id):
    return conn.getObject('Image', image_id)


# Load-data
def load_numpy_array(image):
    pixels = image.getPrimaryPixels()
    size_z = image.getSizeZ()
    size_c = image.getSizeC()
    size_t = image.getSizeT()
    size_y = image.getSizeY()
    size_x = image.getSizeX()
    z, t, c = 0, 0, 0  # first plane of the image
    zct_list = []
    for t in range(size_t):
        for z in range(size_z):  # get the Z-stack
            for c in range(size_c):  # all channels
                zct_list.append((z, c, t))
    values = []
    # Load all the planes as YX numpy array
    planes = pixels.getPlanes(zct_list)
    j = 0
    k = 0
    tmp_c = []
    tmp_z = []
    s = "z:%s t:%s c:%s y:%s x:%s" % (size_z, size_t, size_c, size_y, size_x)
    print(s)
    # axis tzyxc
    print("Downloading image %s" % image.getName())
    for i, p in enumerate(planes):
        if k < size_z:
            if j < size_c:
                tmp_c.append(p)
                j = j + 1
                if j == size_c:
                    # use dstack to have c at the end
                    tmp_z.append(numpy.dstack(tmp_c))
                    tmp_c = []
                    j = 0
                    k = k + 1
        if k == size_z:  # done with the stack
            values.append(numpy.stack(tmp_z))
            tmp_z = []
            k = 0
    return numpy.stack(values)


# Disconnect
def disconnect(conn):
    conn.close()


# main
def main():
    try:
        # Collect user credentials
        host = 'ws://idr.openmicroscopy.org/omero-ws'  # noqa
        username = 'public'
        password = 'public'
        dataset_id = '7754'
        image_id = '6001240'
        # Connect to the server
        conn = connect(host, username, password)
        conn.c.enableKeepAlive(60)

        # Load the images in the dataset
        # images = load_images(conn, dataset_id)
        # Load the image
        image = load_image(conn, image_id)

        # Load the binary data
        t0 = time.process_time()
        load_numpy_array(image)
        t1 = time.process_time() - t0
        print(t1)

    finally:
        disconnect(conn)
    print("done")


if __name__ == "__main__":
    main()
