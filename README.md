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

exception lv.NoLvAttrError
  Raise when no Attribute of this type exists for the LV.

LV Object Creation and Instantination

lv(lv_name, vg_name)
  Returns an LV Object if exists, may be used as lv() on it's own if you want to use lv.create(lv_name,vg,size) later.

lv.create(lv_name,vg,size)
  Creates an LV and returns an LV Object connected to the new device. size is specified in Gigabytes.
  Raises OpFailError if unable to create and NoVgSpaceError if our off VG Space.

LV Object Operations

lv.field(lv_field, refresh=False)
  A dictionery object of all the LV fields as documented in LVS(8). For Example lv_field['LVM2_LV_NAME'] is the name of the LV.
  If the optional aurgument refresh=True the dictonery containing the fields will be updated by accessing running the lvs command before returning the attribute specified. 
  At all other times the value returned is captured the first time the lv object is instance is created.

lv.reload()
  Reload the attributes stored by underlying LV, done automatically after a snapshot is taken. 
  Intended to be used when waiting for a snapshot to merge or to refreshed other dynamic values.

lv.snapshot(varname, int)
  Create a snapshot of the LV with a name varname and the %size int.
  Raise an NoSpaceError or OpFailErrot if unable to complete.

lv.merge()
  Merge an LV snapshot back into the origin.
  Raises NotSnapError when attempted to a normal LV.
  Will reinitiate lv.attr and lv.snapshot so that pending operations are updated

lv.remove()
  Removes the LV 
  Raises OpFailError if unable to remove.
