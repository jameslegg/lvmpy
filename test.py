#!/usr/bin/env python

import os
import lvm
import unittest
import time

class TestLvFunctions(unittest.TestCase):
  lv_name = "testlv"
  vg_name = "testvg"
  #supplied in the format LVM2 stores sizes to make validation easier
  lv_size = "4.00g"
  def setUp(self):
    self.testlv = lvm.lv()
    self.testlv.create(self.lv_name, self.vg_name, self.lv_size)

  def test_size(self):
    self.assertEqual(self.lv_size, self.testlv.get_attr('LVM2_LV_SIZE'))

  def test_lvname(self):
    self.assertEqual(self.lv_name, self.testlv.get_attr('LVM2_LV_NAME'))

  def test_vgname(self):
    self.assertEqual(self.vg_name, self.testlv.get_attr('LVM2_VG_NAME'))

  def tearDown(self):
    #can't delete an LV immediatly after creation
    time.sleep(0.5)
    self.testlv.remove()

if __name__ == '__main__':
  unittest.main()
