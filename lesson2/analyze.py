import json
import sys

def unused_vars():
	prog = json.load(sys.stdin)
	
	used_vars = set()
	for func in prog['functions']:
		for instr in func['instrs']:
			used_vars.update(instr.get('args', []))
			
	for func in prog['functions']:
		for instr in func['instrs']:
			if 'dest' in instr and instr['dest'] not in used_vars:
				print(f"Unused variable: {instr['dest']} in function '{func['name']}'")
        
		

if __name__ == "__main__":
	unused_vars()