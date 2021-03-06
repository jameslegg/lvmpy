lvmpy
=====
my little python toolkit for manipulating LVM

Early version of the intend documentation is below - note for anybody apart from myself is that  much of this isn't yet implemented.

lv - logical volumes object

exception lv.NoVgSpaceError
  Raise when there is not enough space in the VG to complete the the operation requested

exception lv.OpFailError
  Raise when when the lvm shell command returns an error code, return the contents of the output.

exception lv.NotSnapError
  Raise when when an operation specific to a snapshot is attempted on a normal LV.

LV Object Creation and Instantination

lv(lv_name, vg_name)
  Returns an LV Object if exists, may be used as lv() on its own if you want to use lv.create(lv_name,vg,size) later.

lv.create(lv_name,vg,size)
  Creates an LV and returns an LV Object connected to the new device.
  Raises OpFailError if unable to create and NoVgSpaceError if our off VG Space.

LV Object Operations

lv.attr(lv_attr, refresh=False)
  A dictionery object of all the LV fields as documented in LVS(8). For Example lv_attr['LVM2_LV_NAME'] is the name of the LV.
  if optional aurgument refresh is True the dictonery returned will be updated before returning the attribute specified at all 
  other times the dictionery returned is caputered the first time the lv object is imported.

lv.snapshot(varname, int)
  Create a snapshot of the LV with a name varname and the %size int.
  Raise an NoSpaceError or OpFailError if unable to complete.
  Returns an lv object (with attr fields pre-populated) of the newly created snapshot

lv.merge()
  Merge an LV snapshot back into the origin.
  Raises NotSnapError when attempted to a normal LV.
  Will reinitiate lv.attr and lv.snapshot so that pending operations are updated

lv.remove()
  Removes the LV 
  Raises OpFailError if unable to remove.

lv.issnap()
  Returns True if a snapshot (or is a merging snapshot)
  Returns False if not a snapshot
