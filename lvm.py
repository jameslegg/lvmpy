import os
from subprocess import Popen, PIPE

class OpFailError(Exception):
  def __init__(self, lvc_error):
    self.stderr = lvc_error
  def __str__(self):
    return repr(self.stderr)


class lv:
  '''Class to Manipulate LVM logical volumes'''

  def create(self, lv_name, vg_name, lv_size):
    '''Create an LV and return an lv object that reffers to it'''
    global fq_lvn = vg_name + "/" + lv_name
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
    lv_path = self['LVM2_VG_NAME'] + "/" + self['LVM2_LV_NAME']
    print lv_path
    lv = Popen([lvrmcmd, '-f', lv_path], stdout=PIPE, stderr=PIPE) 
    lv_output = lv.communicate()
    #blocks at this point if the command hangs for any reason
    lv_ret_code = lv.wait()
    if not ( lv_ret_code == 0 ):
      raise OpFailError, lvrmcmd + lv_output[1]
    __del__()

  #return Dictioneries with LV fields
  def __get_lv_fields(self):
    "Get the LV and VG fields"
    lvscmd = '/sbin/lvs'
    nmprfx = '--nameprefixes'
    nohead = '--noheadings'
    opt = '-o'
    get_fields = 'lv_all,vg_all'
    print lvscmd + nmprfx + nohead + opt + get_fields 
    lvs = Popen([lvscmd, nmprfx, nohead, opt, get_fields, ], stdout=PIPE) 
    lvs_output = lvs.communicate()[0]
    for field in lvs_output.split():
      lv_field = field.split('=')
      all_lv_fields[lv_field[0]] = lv_field[1].replace("'","")


  #figure out the attributes of an LV
  def __get_lv_attr(lv):
     "Get out the lv_attr bits"
     lvf = get_lv_fields(lv) 
     lv_attr = lvf['LVM2_LV_ATTR'].split("")
     print lv_attr
     #volume type
     lv = {}
     if lv_attr[0] == 'S':
       lv['Snapshot']
     return lv 

  def __init___(self, vg_name=None, lv_name=None):
    self.lv = object 
    all_lv_fields = {} 
    #minimum required to refer to an LV
    fq_lvn = vg_name + "/" + lv_name
    return self

  def __del__(self):
    del self
