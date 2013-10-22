# This file is part of h5py, a Python interface to the HDF5 library.
#
# http://www.h5py.org
#
# Copyright 2008-2013 Andrew Collette and contributors
#
# License:  Standard 3-clause BSD; see "license.txt" for full license terms
#           and contributor agreement.

from .common import TestCase

import tempfile
import shutil
import os
from h5py import File


class TestVFD(TestCase):

    """
        Features related to retrieving file descriptors from the HDF5 layer.
    """

    def test_descriptor_core(self):
        """ Attempt to retrieve vfd handle on CORE driver raises 
        NotImplementedError """
        with File('TestFileID.test_descriptor_core', driver='core', backing_store=False) as f:
            with self.assertRaises(NotImplementedError):
                f.id.get_vfd_handle()

    def test_descriptor_sec2(self):
        """ Verify get_vfd_handle returns a valid file descriptor """
        fname = self.mktemp()
        with File(fname, driver='sec2') as f:
            descriptor = f.id.get_vfd_handle()
            self.assertNotEqual(descriptor, 0)
            os.fsync(descriptor)


class TestCacheConfig(TestCase):

    """
        Features related to the metadata cache config.
    """

    def setUp(self):
        self.f = File(self.mktemp())

    def tearDown(self):
        self.f.close()

    def test_simple_gets(self):
        """ Test retrieving metadata cache settings """
        hit_rate = self.f.id.get_mdc_hit_rate()
        mdc_size = self.f.id.get_mdc_size()

    def test_hitrate_reset(self):
        """ Test resetting hit rate cache"""
        hit_rate = self.f.id.get_mdc_hit_rate()
        self.f.id.reset_mdc_hit_rate_stats()
        hit_rate = self.f.id.get_mdc_hit_rate()
        self.assertEqual(hit_rate, 0)

    def test_mdc_config_get(self):
        """ Test round-trip metadata cache settings """
        conf = self.f.id.get_mdc_config()
        self.f.id.set_mdc_config(conf)
