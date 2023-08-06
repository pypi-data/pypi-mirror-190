

from progress.bar import Bar

class TranferBar(Bar):
    suffix='%(percent)d%% | %(eta_td)s/%(elapsed_td)s | %(size)s | %(speed)s ' 

    @property
    def speed(self):
        if self.elapsed < 1:
            return '--'
        if self.index < self.max:
            bps = 1.0 / self.avg
        else:
            bps = self.index / self.elapsed   
        return size_string(bps, 1) + '/s'
        
    @property
    def size(self):
        return size_string(float(self.max), 0)

def size_string(byte: float, fraction: int):

    fmt = '%%.%d' % fraction + 'f'
    
    if byte < 1024:
        return fmt % byte + ' B'
    
    KB = byte / 1024
    if KB < 1024:
        return fmt % KB + ' KB'

    MB = KB / 1024
    if MB < 1024:
        return fmt % MB + ' MB'

    GB = MB / 1024
    return fmt % GB + ' GB'
