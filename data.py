from collections import namedtuple

class Failstack:
  def __init__(self, val, max_val):
    self.val = val
    self.base = val
    self.max_val = max_val
    self.used = 0
  def up(self):
    self.val = min(self.val + 3, self.max_val) 
  def reset(self):
    self.val = self.base
    self.used += 1
  def get_value(self):
    val_est = {
      20 : 15.33,
      30 : 30,
      40 : 75,
      90 : 999
    }
    return max(0, self.used-1) * val_est[self.base]

def perc_to_real(perc): return perc/100

def get_yellow():
  fs = [
    Failstack(20, 30), 
    Failstack(30, 40), 
    Failstack(40, 90),
    Failstack(90, 190)
  ]
  crons = [1, 38, 113, 429]
  chances = [
    #perc_to_real(11.76),
    (perc_to_real(7.69), perc_to_real(1.18)),  
    (perc_to_real(6.25), perc_to_real(0.77)),
    (perc_to_real(2.00), perc_to_real(0.63)),
    (perc_to_real(0.30), perc_to_real(0.03))
  ] 
  return { "fs" : fs, "crons" : crons, "chances" : chances }

