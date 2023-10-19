import numpy as np
import glob

all_arrays = []

npfiles = glob.glob("vectors/*.npy")
npfiles.sort()
for npfile in npfiles:
  with open(npfile, 'br') as f:
    all_arrays.append(np.load(f))

all_arrays = np.array(all_arrays)

with open('vectors.npy', 'wb') as f:
  np.save(f, all_arrays)    
