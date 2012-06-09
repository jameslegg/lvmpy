#!/usr/bin/env python

import os
import lvm

def main():

  lv_name = "testlv"
  vg_name = "VGi0"
  lv_size = "5G"

  
  testlv = lvm.lv()
  testlv.create(lv_name, vg_name, lv_size)
 
  print  testlv.attr['LVM2_LV_SIZE']

  if [ testlv.attr['LVM2_LV_SIZE'] == lv_size ]:
    print "PASS"
  else:
    print "FAIL"

  try:
    test.remove()
  except OpFailError, (e):
    print "FAIL: Unable to remove" + e.parameter

if __name__ == '__main__':
    main()

