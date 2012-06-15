#!/usr/bin/env python

import os
import lvm
import unittest

class TestSequenceFunctions(unittest.TestCase):

  def setUp(self):
    self.testlv = lvm.lv()

  def tearDown(self):
    self.testlv.remove()

  def test_create(self):
    lv_name = "testlv"
    vg_name = "VGi0"
<<<<<<< HEAD
    lv_size = "5"
=======
    lv_size = "5G"
>>>>>>> aecaad76eb0c9096826e4b1385709005bace5ed2
    self.testlv.create(lv_name, vg_name, lv_size)
    self.assertTrue(self.testlv)

  def test_size(self):
    lv_name = "testlv"
    vg_name = "VGi0"
    lv_size = "5"
    self.testlv.create(lv_name, vg_name, lv_size)
    attr = "LVM2_LV_SIZE"
<<<<<<< HEAD
    size = self.testlv.field(attr)
    self.assertTrue( size == lv_size + ".00g")

  def test_field(self):
    lv_name = "testlv"
    vg_name = "VGi0"
    lv_size = "5"
    self.testlv.create(lv_name, vg_name, lv_size)
    field = "NON_EXISTANT_ATTR"
    self.assertRaises(lvm.NoLvAttrError, self.testlv.field, field)
=======
    size = self.testlv.attr(attr)
    self.assertTrue( size == lv_size + ".00g")

  def test_attr_except(self):
    lv_name = "testlv"
    vg_name = "VGi0"
    lv_size = "5G"
    self.testlv.create(lv_name, vg_name, lv_size)
    attr = "NON_EXISTANT_ATTR"
    self.assertRaises(lvm.NoLvAttrError, self.testlv.attr, attr)
>>>>>>> aecaad76eb0c9096826e4b1385709005bace5ed2

if __name__ == '__main__':
    unittest.main()

