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


# ! should do some preprocessing pass such that I rename the earlier instance of a variable if its reused
def lvn(blocks):
    # need to define val - (op, args...)
    for block in blocks:
        CurVarToId = {} # var to id map
        VarToVal = [] # this is the table represented as list of tuple (var, val), list index is ID
        for instr in block:
            # * if value in table
            if 'dest' in instr:
                if instr['op'] == 'const':
                    value = (instr['op'], instr['value'])
                else: 
                    # this .get part might need refactoring... this is essentially the case where variable is not defined in the scope of \
                    # the current block, we might want to keep track of this in the table
                    # ! if VarToVal of this returns a constant, use the actual value instead of variable ([1] instead of [0])
                    args_list = []
                    for arg in instr.get('args', []):
                        # * Undefined variable in scope
                        if CurVarToId.get(arg, None) != None:
                            args_list.append(VarToVal[CurVarToId.get(arg, arg)][0])
                        else:
                             VarToVal.append((arg, arg))
                             args_list.append([arg])
                             CurVarToId[arg] = len(VarToVal)-1
                            
                    value = (instr['op'], args_list)

                # * find index and var if value is in VarToVal already
                if not isinstance(value, bool):
                    num, var = next(((i, k) for i, (k, v) in enumerate(VarToVal) if v == value and not isinstance(v, bool)), (None, None))


                # * if value in table
                # ! this is not working completely right
                # ! bc of how i insert id commands into here, i should be checking differently
                # ! instead of replacing when duplicate values are id'd, replaces duplicate actual id function usages
                if var and instr['op'] != 'id':
                    # replace instr with copy of var
                    # ! here is where i can do const prop, keep track of constants, check if constant, replace w constant
                    instr.update({'op': 'id', 'args': [var]})
                else:
                    VarToVal.append((instr['dest'], value))
                    num = len(VarToVal) - 1
                    # * go through args and put their canonical value
                    if 'args' in instr:
                        for i, arg in enumerate(instr['args']):
                            instr['args'][i] = VarToVal[CurVarToId[arg]][0]

                # add to var to id map
                CurVarToId[instr['dest']] = num

                
    # print(CurVarToId)
    # print(VarToVal)

    return blocks

if __name__ == "__main__":
	prog = json.load(sys.stdin)
	for func in prog['functions']:
		blocks = create_blocks(func['instrs'])
		lvn(blocks)
		func['instrs'] = [instr for block in blocks for instr in block if instr]
	
	json.dump(prog, sys.stdout, indent=2, sort_keys=True)
	