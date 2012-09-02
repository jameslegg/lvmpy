#!/usr/bin/env python

import os
import lvm
import unittest
import time

class TestLvFunctions(unittest.TestCase):
  lv_name = "testlv"
  vg_name = "testvg"
  test_snap = 'testsnap1'
  #supplied in the format LVM2 stores sizes to make validation easier
  test_snap_size = '2.00g'
  lv_size = "4.00g"
  def setUp(self):
    self.testlv = lvm.lv()
    self.testlv.create(self.lv_name, self.vg_name, self.lv_size)
    self.testlvsnapshot = self.testlv.snapshot(self.test_snap, self.test_snap_size)

  def test_size(self):
    self.assertEqual(self.lv_size, self.testlv.attr('LVM2_LV_SIZE'))

  def test_lvname(self):
    self.assertEqual(self.lv_name, self.testlv.attr('LVM2_LV_NAME'))

  def test_vgname(self):
    self.assertEqual(self.vg_name, self.testlv.attr('LVM2_VG_NAME'))

  def test_create_snapshot(self):
    new_snap = self.testlv.snapshot('cows', '300m')
    
  def test_remove_snapsnot(self):
    self.testlvsnapshot.remove()

  def test_name_snap(self):
    self.assertEqual(self.test_snap, self.testlvsnapshot.attr('LVM2_LV_NAME'))

  def test_size_snap(self):
    self.assertEqual(self.test_snap_size, self.testlvsnapshot.attr('LVM2_LV_SIZE'))

  def tearDown(self):
    #can't delete an LV immediatly after creation
    time.sleep(0.1)
    self.testlv.remove()

if __name__ == '__main__':
  unittest.main()
