from random import random, seed
from data import get_yellow
from matplotlib import pyplot as plt
from copy import deepcopy
import numpy as np

SIMULATIONS = 2e3 #number of simulations to be performed 

SIMULATIONS = int(SIMULATIONS)

class RunType:
  Show = 0 #shows the result in a graph
  Save = 1 #saves the result to file
  Both = 2 #save and display

SCRIPT_RUN_TYPE = RunType.Save

class Upgrade:
  PRI = 0 #enumerative to use Upgrade.Improvement instead of number
  DUO = 1
  TRI = 2
  TET = 3
  PEN = 4
  def __init__(
   self, crons, values, start, target, failstacks, chances, dura_up, 
   cron_cost = 1, memory_cost = 2):#1 and 2 million silver respectively
	   
    #cron at livel x [pri, duo, tri, tet, pen]
    self.crons = crons
    #value at livel x [pri, duo, tri, tet, pen]
    self.values = values
    #starting level of the item
    self.start = start
    #actual level of the item (at the beginning, start)
    self.actual = start
    #desired level
    self.target = target
    #durability lost by attempt
    self.dura_up = dura_up
    #failstack to be used at level x [pri, duo, tri, tet, pen]
    self.failstacks = failstacks
    #chance of improvement at level x [pri, duo, tri, tet, pen]
    self.chances = chances
    #cost of a cron (million of silver)
    self.cron_cost = cron_cost
    #cost of a memory (repair 1 of durability)
    self.memory_cost = memory_cost
    #total durability lost so far (0 at the start)
    self.dura_lost = 0
    #total of cron used so far (0 all'inizio)
    self.crons_used = 0
    #failures so far for each level (pri, duo, tri, tet, pen)
    self.fails = [0,0,0,0,0]
    #attempts to upgrade to level (pri, duo, tri, tet, pen)
    self.tries = [0,0,0,0,0]
    #attempts made to improve the item
    self.up_tries = 0

  def calc_prob(self):
    """
    calculates the probability given the current level 
    and the failstack which is equal to chance_base + (failstack * increase_of_chance_per_fs)
    """
    i = self.actual
    r = self.chances[i][0] + self.failstacks[i].val * self.chances[i][1]
    return r
    #return self.chances[i].base + self.chances[i].scale * self.failstacks[i].val
  
  def upgrade(self):
    """
    upgrade event, try to upgrade the item to the next level and record the statistics
    - attempts in general
    - attempts[upgrade]
    - durability lost
    - cron used
    """
    prob = self.calc_prob()
    self.up_tries += 1
    self.tries[self.actual] += 1
    r = random()
    self.dura_lost += self.dura_up
    self.crons_used += self.crons[self.actual]
    if r > prob:
      self.fail()
    else:
      self.succ()

  def run(self, s):
    """
    Runs the simulation until the item is at the desired level
    """
    seed(s)
    while self.actual != self.target:
      self.upgrade()
    #print(self.fails, self.failstacks[0].used)
    #print([x.used for x in self.failstacks])
    return self
  
  def succ(self):
    """
    in case of success the failstack is lost and the item is improved
    """
    self.failstacks[self.actual].reset()
    self.actual += 1

  def fail(self):
    """
    in case of failure:
    - failures are counted for the current level
    - if cron was used: no level is lost and no failstack is gained
    - if no cron was used: level is lost but failstack is gained (+3)
    """
    self.fails[self.actual] += 1
    assert self.actual >= 0, "fuck"
    if self.crons[self.actual] == 0:
      self.failstacks[self.actual].up()
      self.actual = max(self.actual - 1, 0)
  
  def calc_cost(self, failstack_value = True, cron_value = True):
    """
    calculates the cost of the simulation given by:
    cron_used * cost_cron + durability_lost * cost_memory + cost_object_to_upload * attempts_to_up + 
    failstack_cost * quantity_used_per_type 
    """
    i = self.actual
    return (self.values[self.start] + 
      (self.cron_cost * self.crons_used if cron_value else 0) + 
      self.memory_cost * self.dura_lost + 
      self.up_tries * 2 + #upstone 
      (sum(self.failstacks[i].get_value() for i in range(self.start, self.target)) if failstack_value else 0))

  def calc_gain(self):
    """
    gain = sale_price - cost
    """
    return self.values[-1] - self.calc_cost()
  
  def session_duration(self):
    """
    3s per tap + 
    1 minute to make any failstack (optimistic) + 
    5 sec to recover durability
    """
    return self.up_tries * 3 + 60 * sum(fs.used for fs in self.failstacks) + (self.dura_lost / 100) * 5

def get_cronned_try(values, stats, start):
  """
  It makes a 'cronned' attempt, in the stats array there is an array that governs which crons are used (for which level) 
  basically cron:=[0,0,0,>0] means that in quarter (TET) is cronned
  """
  s = deepcopy(stats)
  u = [
    Upgrade(deepcopy(s['crons']), [100,0,0,0,18000], start, Upgrade.PEN, deepcopy(s['fs']), deepcopy(s['chances']), 3) 
    for _ in range(int(SIMULATIONS))
  ]
  u = [x.run(s) for s, x in enumerate(u)]
  return u

if SCRIPT_RUN_TYPE == RunType.Show:
  def save_fig(name):
    plt.show()
elif SCRIPT_RUN_TYPE == RunType.Save:
  def save_fig(name):
    plt.savefig(name + ".png")
    plt.clf()
else:
  def save_fig(name):
    plt.savefig(name + ".png")
    plt.show()
    plt.clf()
"""
save_name(stats, name):
_name is the statistic to be saved
stats is the set of simulations
name is the name of the file (and the title of the graph)
"""

def save_crons_usage(stats, name):
  stats = [x.crons_used for x in stats]
  plt.hist(stats, bins=30, density= True)
  print("crons: ", avg(stats))
  plt.title(name)
  save_fig(name)

def save_avg_fails(stats, name):
  stats = [
    [
      (f/x.tries[i]) if x.tries[i] != 0 else 0
      for i, f in enumerate(x.fails)
    ] 
    for x in stats
  ]
  """
  takes the recorded failures as an array (simulations X upgrades) 
  and averages them on the simulation axis, resulting in an array (upgrade)
  where 0 is pri, 1 is duo, 2 is tri, 3 is tet and 4 is pen
  """
  stats = np.mean(stats, axis=0)
  plt.plot(list(range(5)), stats)
  plt.title("Avg fails")
  plt.show()

def avg(s): return sum(s)/len(s)

def save_cost(s, name):
  stats = [x.calc_cost() for x in s]
  plt.hist(stats, density = True, bins=30)
  plt.xlabel("Cost")
  plt.ylabel("Probability")
  print("Cost (pay both)", avg(stats))
  plt.title("Cost" + name)
  save_fig(name)

  stats = [x.calc_cost(failstack_value=False, cron_value=True) for x in s]
  plt.hist(stats, density = True, bins=30)
  plt.title(name + "(free fs, pay cron)")
  plt.xlabel("Cost")
  plt.ylabel("Probability")
  print("Cost (free fs, pay cron)", avg(stats))
  save_fig(name + "_free_fs_pay_cron")

  stats = [x.calc_cost(failstack_value=True, cron_value=False) for x in s]
  plt.hist(stats, density = True, bins=30)
  plt.title(name + "(pay fs, free cron")
  plt.xlabel("Cost")
  plt.ylabel("Probability")
  print("Cost (pay fs, free cron)", avg(stats))
  save_fig(name + "_pay_fs_free_cron")

  stats = [x.calc_cost(failstack_value=False, cron_value=False) for x in s]
  plt.hist(stats, density = True, bins=30)
  plt.xlabel("Cost")
  plt.ylabel("Probability")
  plt.title(name + "(free fs, free cron)")
  print("Cost (free fs, free cron)", avg(stats))
  save_fig(name + "_free_fs_free_cron")

def save_gain(stats, name):
  stats = [x.calc_gain() for x in stats]
  plt.hist(stats, density = True, bins = 30)
  plt.title(name)
  plt.xlabel("Gain")
  plt.ylabel("Probability")
  print("gain: ", avg(stats))
  plt.title(name)
  save_fig(name)

def save_time(stats, name):
  stats = [x.session_duration() for x in stats]
  plt.hist(stats, density = True, bins=30)
  plt.title(name)
  plt.xlabel("Time (s)")
  plt.ylabel("Probability")
  import datetime
  print("Time (h:m:s.ms): ", str(datetime.timedelta(seconds=avg(stats))))
  save_fig(name)

def simul_part_crons(cron_only):
  stats = get_yellow()
  for i in range(4):
    if i not in cron_only:
      stats['crons'][i] = 0
  t = get_cronned_try([0,0,0,0,0], stats, 0)
  cspec = "all" if len(cron_only) == 4 else "_".join(str(x) for x in cron_only)
  save_crons_usage(t, "crons_from_0_tri_cron" + cspec)
  save_cost(t, "cost_PRI_PEN_cron" + cspec)
  save_gain(t, "gain_PRI_PEN_cron" + cspec)
  save_time(t, "time_PRI_PEN_cron" + cspec)
  #save_avg_fails(t, "")

def main():
  from data import get_yellow
  print("cron ALL")
  simul_part_crons([0,1,2,3,4])
  print()
  print("cron TET")
  simul_part_crons([3])
  print()
  print("cron TRI")
  simul_part_crons([2])
  print()
  print("cron DUO")
  simul_part_crons([1])
  print()
  print("cron NONE")
  simul_part_crons([])
  print()

if __name__ == "__main__":
  main()
