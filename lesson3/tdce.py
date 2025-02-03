import json
import sys
from cfg import create_blocks

def unused_vars(blocks):	
	change = True
	while change:
		change = False
		used_vars = set()
		for block in blocks:
			for instr in block:
				used_vars.update(instr.get('args', []))
				
		for i, block in enumerate(blocks):
			for j, instr in enumerate(block):
				if 'dest' in instr and instr['dest'] not in used_vars:
					change = True
					# need to remove previous setting of this var, not this current instr (if thinking in block format)
					# print(f"Unused variable: {instr['dest']} in function '{func['name']}'")
					blocks[i][j] = {}
	
	return blocks

if __name__ == "__main__":
	prog = json.load(sys.stdin)
	for func in prog['functions']:
		blocks = create_blocks(func['instrs'])
		unused_vars(blocks)
		func['instrs'] = [instr for block in blocks for instr in block if instr]  
	
	json.dump(prog, sys.stdout, indent=2, sort_keys=True)
	