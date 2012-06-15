import os
from subprocess import Popen, PIPE

class OpFailError(Exception):
  def __init__(self, lvc_error):
    self.stderr = lvc_error
  def __str__(self):
    return repr(self.stderr)

class NoLvAttrError(Exception):
  def __init__(self, lvc_error):
    self.stderr = lvc_error
  def __str__(self):
    return repr(self.stderr)


class lv(object):
  '''Class to Manipulate LVM logical volumes'''

  def __del__(self):
    del self

  def create(self, lv_name, vg_name, lv_size):
    '''Create an LV and return an lv object that reffers to it'''
    self.fq_lvn = vg_name + "/" + lv_name
    lvcreatecmd = '/sbin/lvcreate'
    lv = Popen([lvcreatecmd, '-L', lv_size + "G", '-n', lv_name, vg_name], stdout=PIPE, stderr=PIPE) 
    lv_output = lv.communicate()
    #blocks at this point if the command hangs for any reason
    lv_ret_code = lv.wait()
    #TODO implement VG objects to allow size check before attempting LV creation
    if not ( lv_ret_code == 0 ):
      raise OpFailError, lvcreatecmd + lv_output[1]
    #populate all the attributes
    self.all_lv_fields = {}
    self.__get_lv_fields()


  def remove(self):
    '''Remove the LV'''
    lvrmcmd = '/sbin/lvremove'
    lv = Popen([lvrmcmd, '-f', self.fq_lvn], stdout=PIPE, stderr=PIPE) 
    lv_output = lv.communicate()
    #blocks at this point if the command hangs for any reason
    lv_ret_code = lv.wait()
    if not ( lv_ret_code == 0 ):
      raise OpFailError, lvrmcmd + lv_output[1]
    self.__del__()

  def attr(self, attr, refresh=False):
    """Return an lv attribute specifed"""
    if refresh:
      self.__get_lv_fields()
    try:
      myattr = self.all_lv_fields[attr]
    except KeyError, e:
      raise NoLvAttrError, attr + " not availble"
    return myattr

  #update Dictioneries with LV fields
  def __get_lv_fields(self):
    """Get the LV and VG fields"""
    lvscmd = '/sbin/lvs'
    nmprfx = '--nameprefixes'
    nohead = '--noheadings'
    opt = '-o'
    get_fields = 'lv_all,vg_all'
    lvs = Popen([lvscmd, nmprfx, nohead, opt, get_fields, self.fq_lvn], stdout=PIPE) 
    lvs_output = lvs.communicate()[0]
    for field in lvs_output.split():
      lv_field = field.split('=')
      #not all fields are populated
      try:
        name = lv_field[0]
        val = lv_field[1]
        self.all_lv_fields[name] = val.replace("'","")
      except IndexError, e:
        val = ""
        name = lv_field[0]
        self.all_lv_fields[name] = val.replace("'","")


  #figure out the attributes of an LV
  def __get_lv_attr2(self, attr):
     "Get out the lv_attr bits"
     lvf = __get_lv_fields(self) 
     lv_attr = lvf['LVM2_LV_ATTR'].split("")
     print lv_attr
     #volume type
     lv = {}
     if lv_attr[0] == 'S':
       #lv['Snapshot']
       return self.lv

  
