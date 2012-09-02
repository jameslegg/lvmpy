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
    #see notes about timeouts in tearDown()
    time.sleep(1)
  def test_size(self):
    self.assertEqual(self.lv_size, self.testlv.attr('LVM2_LV_SIZE'))

  def test_lvname(self):
    self.assertEqual(self.lv_name, self.testlv.attr('LVM2_LV_NAME'))

  def test_vgname(self):
    self.assertEqual(self.vg_name, self.testlv.attr('LVM2_VG_NAME'))

  def test_exists_lv(self):
    self.assertTrue(self.testlvsnapshot.exists())

  def test_create_snapshot(self):
    self.new_snap = self.testlv.snapshot('cows', '300m')
    self.assertIsInstance(self.new_snap, lvm.lv)
    
  def test_exists_snapshot(self):
    self.assertTrue(self.testlv.exists())

  def test_remove_snapshot(self):
    self.testlvsnapshot.remove()
    self.assertFalse(self.testlvsnapshot.exists())

  def test_merge_snapshot(self):
    self.testlvsnapshot.merge()
    self.assertTrue(self.testlvsnapshot.issnap())

  def test_fail_merge_lv(self):
    with self.assertRaises(lvm.OpFailError):
      self.testlv.merge()
    self.assertFalse(self.testlv.issnap())

  def test_name_snap(self):
    self.assertEqual(self.test_snap, self.testlvsnapshot.attr('LVM2_LV_NAME'))

  def test_size_snap(self):
    self.assertEqual(self.test_snap_size, self.testlvsnapshot.attr('LVM2_LV_SIZE'))

  def tearDown(self):
    #The try and sleep try again are because sometimes
    #you can't delete an LV immediatly after creation
    #lvm also hangs if you don't wait a little before executing
    #an lvs on a just merged volume!
    #http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=659762
    #TODO
    #implement some sensible retry methods across the entire tool
    #to handle this sort of thing
    if self.testlvsnapshot.exists():
      try:
        self.testlvsnapshot.remove()
      except:
        time.sleep(2)
        self.testlvsnapshot.remove()
    #clear up after the create_snapshot test
    try:
      self.new_snap.exists()
      self.new_snap.remove()
    except:
      #self.new_snap does not exist  
      next
    try:
      self.testlv.remove()
    except:
      time.sleep(2)
      self.testlv.remove()

if __name__ == '__main__':
  unittest.main()
