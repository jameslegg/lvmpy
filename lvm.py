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
    '''Remove an LV'''
    lvrmcmd = '/sbin/lvremove'
    lv = Popen([lvrmcmd, '-f', self.fq_lvn], stdout=PIPE, stderr=PIPE) 
    lv_output = lv.communicate()
    #blocks at this point if the command hangs for any reason
    lv_ret_code = lv.wait()
    if not ( lv_ret_code == 0 ):
      raise OpFailError, lvrmcmd + lv_output[1]
    self.__del__()

  def attr(self, attr, refresh=False):
    '''Return LV attributes on request'''
    if refresh:
      self.__get_lv_fields(self)
    return self.lv_fields[attr]

  def snapshot(self, snapshot, snapsize):
    '''Create a Snapshot of an LV and return an lv object of that snapshot'''
    lvcreatecmd = '/sbin/lvcreate'
    lvsnap = Popen([lvcreatecmd, '--size', snapsize, '--name', snapshot, '--snapshot', self.fq_lvn], stdout=PIPE, stderr=PIPE)
    lvsnap_output = lvsnap.communicate()
    lvsnap_ret_code = lvsnap.wait()
    if not ( lvsnap_ret_code == 0):
      raise OpFailError, lvcreatecmd + lvsnap_output[1]
    new_snap = self.__class__(self.lv_fields['LVM2_VG_NAME'], snapshot)
    new_snap.__get_lv_fields()
    return new_snap

  def merge(self):
    '''Merge a snapshot back into LV'''
    lvmergecmd = '/sbin/lvconvert'
    lvmerge = Popen([lvmergecmd, '--merge', self.fq_lvn], stdout=PIPE, stderr=PIPE)
    lvmerge_output = lvmerge.communicate()
    lvmerge_ret_code = lvmerge.wait()
    if not ( lvmerge_ret_code == 0):
      raise OpFailError, lvmergecmd + lvmerge_output[1]

  def exists(self):
    '''Check if the underyling lv or snapshot exists'''
    lvscmd = '/sbin/lvs'
    nohead = '--noheadings'
    lvs = Popen([lvscmd, nohead, self.fq_lvn], stdout=PIPE, stderr=PIPE) 
    lvs_output = lvs.communicate()[0]
    lvs_ret_code = lvs.wait()
    if lvs_ret_code == 0:
      return True
    else:
      return False

  def __get_lv_fields(self):
    '''Return all the LV and VG fields'''
    lvscmd = '/sbin/lvs'
    nmprfx = '--nameprefixes'
    nohead = '--noheadings'
    opt = '-o'
    get_fields = 'lv_all,vg_all'
    lvs = Popen([lvscmd, nmprfx, nohead, opt, get_fields, self.fq_lvn], stdout=PIPE, stderr=PIPE) 
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

  def issnap(self):
     "Returns True if the lv is a snapshot"
     lv_attr = list(self.lv_fields['LVM2_LV_ATTR'])
     #First bit is S for Snapshot or s for merging snapshot
     if lv_attr[0] == 'S' or lv_attr[0] == 's':
       return True
     else:
      return False

  def __init__(self, vg_name=None, lv_name=None):
    self.lv = object 
    self.lv_fields = dict()
    #minimum required to refer to an LV
    #These don't have to be supplier here if calling create() later
    if vg_name is not None and lv_name is not None:
      self.fq_lvn = vg_name + "/" + lv_name

  def __del__(self):
    del self
