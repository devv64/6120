import json
import sys
from cfg import create_blocks

''''
LVM works to have same effect as 3 optimizations combined:
    - Dead code elimination (DCE)
    - Copy propagation
    - Common subexpression elimination (CSE)

Common thread between all of these is because they consider variables rather than values
Essentially: # Variables Defined <= # Values Used


'''

