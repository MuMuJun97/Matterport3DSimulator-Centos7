import os 
import sys 
from pathlib import Path 

rootdir = (Path(__file__).parent / 'build').resolve()

print("\nTEST MatterSim ......\n")
print("PATH: ",rootdir)

sys.path.append(rootdir.__str__())

import MatterSim
sim = MatterSim.Simulator()
sim.setRenderingEnabled(False)
sim.initialize()

print('TEST MatterSim SUCCESS\n')