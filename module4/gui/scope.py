import vxi11
import numpy as np


class SCPI(object):
    def __init__(self, instr):
        self.instr = instr
        
    def get_idn(self):
        return tuple(self.instr.ask('*IDN?').split(','))
    
    idn = property(get_idn)
    
    def scpi_ask(self, cmd):
        cmd = cmd if cmd.endswith('?') else cmd + '?'
        return self.instr.ask(cmd)
    
    def scpi_write(self, cmd_name, *args):
        arg_string = ','.join([repr(elm) for elm in args])
        cmd = '{cmd_name} {arg_string}'.format(cmd_name=cmd_name, 
                                              arg_string=arg_string)
        
    def scpi_ask_for_float(self, cmd):
        return float(self.scpi_ask(cmd))

class TektronixScope(SCPI):
    def get_manufacturer(self):
        return self.get_idn()[0]
    
    def _check_channel_number(self, channel_number):
        assert channel_number in [1, 2, 3, 4], "Channel number should be 1, 2, 3 or 4"
    
    
    def get_channel_scale(self, channel_number):
        self._check_channel_number(channel_number)
        cmd_name = 'CH{:d}:SCA'.format(channel_number)
        return self.scpi_ask_for_float(cmd_name)
    
    def set_channel_scale(self, channel_number, scale):
        self._check_channel_number(channel_number)
        cmd_name = 'CH{:d}:SCA'.format(channel_number)
        self.scpi_write(cmd_name, scale)
        
    def set_data_source(self, channel_number):
        self._check_channel_number(channel_number)
        cmd = 'DAT:SOUR'
        arg = 'CH{:d}'.format(channel_number)
        self.scpi_write(cmd, arg)
        
    def get_waveform(self, channel_number):
        self.set_data_source(channel_number)
        self.instr.write('CURVE?')
        raw_data = self.instr.read_raw()
        header_length = int(raw_data[1:2])+2
        typ = np.dtype('int16').newbyteorder('>')
        data = np.frombuffer(raw_data[header_length:-1], dtype=typ)
        offset = self.scpi_ask_for_float('WFMO:YOF')
        mul_factor = self.scpi_ask_for_float('WFMO:YMUL')
        return (data-offset)*mul_factor

