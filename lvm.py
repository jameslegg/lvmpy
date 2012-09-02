import os
from subprocess import Popen, PIPE

class OpFailError(Exception):

  def __init__(self, lvc_error):
    self.stderr = lvc_error
  def __str__(self):
    return repr(self.stderr)


class lv:
  '''Class to Manipulate LVM logical volumes'''
  fq_lvn = str
  lv_fields = {}

  def create(self, lv_name, vg_name, lv_size):
    '''Create an LV and return an lv object that refers to it'''
    self.fq_lvn = vg_name + "/" + lv_name
    lvcreatecmd = '/sbin/lvcreate'
    lv = Popen([lvcreatecmd, '-L', lv_size, '-n', lv_name, vg_name], stdout=PIPE, stderr=PIPE) 
    lv_output = lv.communicate()
    #blocks at this point if the command hangs for any reason
    lv_ret_code = lv.wait()
    #TODO implement VG objects to allow size check before attempting LV creation
    #if ( lv_ret_code == 5 ) and 
    #  raise NoVgSpaceError, lvrmcmd + lv_output[1]
    if not ( lv_ret_code == 0 ):
      raise OpFailError, lvcreatecmd + lv_output[1]
    self.__get_lv_fields()
    return self

  def remove(self):
    '''Create an LV and return and lv object that reffers to it'''
    lvrmcmd = '/sbin/lvremove'
    lv_path = self.lv_fields['LVM2_VG_NAME'] + "/" + self.lv_fields['LVM2_LV_NAME']
    lv = Popen([lvrmcmd, '-f', lv_path], stdout=PIPE, stderr=PIPE) 
    lv_output = lv.communicate()
    #blocks at this point if the command hangs for any reason
    lv_ret_code = lv.wait()
    if not ( lv_ret_code == 0 ):
      raise OpFailError, lvmrmcmd + lv_output[1]

  def attr(self, attr, refresh=False):
    '''Return LV attributes on request'''
    if refresh:
      self.__get_lv_fields(self)
    return self.lv_fields[attr]

  def snapshot(self, snapshot, snapsize):
    '''Create a Snapshot of an LV and return an lv object of that snapshot'''
    lvcreatecmd = '/sbin/lvcreate'
    lv_path = self.lv_fields['LVM2_VG_NAME'] + "/" + self.lv_fields['LVM2_LV_NAME']
    lvsnap = Popen([lvcreatecmd, '--size', snapsize, '--name', snapshot, '--snapshot', lv_path], stdout=PIPE, stderr=PIPE)
    lvsnap_output = lvsnap.communicate()
    lvsnap_ret_code = lvsnap.wait()
    if not ( lvsnap_ret_code == 0):
      raise OpFailError, lvcreatecmd + lvsnap_output[1]
    new_snap = self.__class__(self.lv_fields['LVM2_VG_NAME'], snapshot)
    new_snap.__get_lv_fields()
    return new_snap

   

  #return Dictioneries with LV fields
  def __get_lv_fields(self):
    "Get the LV and VG fields"
    lvscmd = '/sbin/lvs'
    nmprfx = '--nameprefixes'
    nohead = '--noheadings'
    opt = '-o'
    get_fields = 'lv_all,vg_all'
    lvs = Popen([lvscmd, nmprfx, nohead, opt, get_fields, self.fq_lvn], stdout=PIPE) 
    lvs_output = lvs.communicate()[0]
    lvs_ret_code = lvs.wait()
    if not ( lvs_ret_code == 0 ):
      raise OpFailError, lvs + lvs_output[1]
    for field in lvs_output.split():
      lv_field = field.strip().split('=')
      # To cope with values containing whitespace 
      # we ignore felds containing just a single apostraphe
      if lv_field[0] == "'":
        continue
      self.lv_fields[lv_field[0]] = lv_field[1].strip().replace("'","")

  #figure out the attributes of an LV
  def __get_lv_attr(lv):
     "Get out the lv_attr bits"
     lvf = get_lv_fields(lv) 
     lv_attr = lvf['LVM2_LV_ATTR'].split("")
     #volume type
     lv = {}
     if lv_attr[0] == 'S':
       lv['Snapshot']
     return lv 

  def __init__(self, vg_name=None, lv_name=None):
    self.lv = object 
    self.lv_fields = dict()
    #minimum required to refer to an LV
    #These don't have to be supplier here if calling create() later
    if vg_name is not None and lv_name is not None:
      self.fq_lvn = vg_name + "/" + lv_name

  def __del__(self):
    del self
