import json
import sys

terms = ['jmp', 'br', 'call', 'ret']

def create_blocks(instructions):
	blocks = []
	cur = []
	for instr in instructions:
		if 'op' in instr:
			cur.append(instr)
			if instr['op'] in terms:
				blocks.append(cur)
				cur = []
		else:
			if cur: # can only be label
				blocks.append(cur)
			cur = [instr]
	if cur:
		blocks.append(cur)
	return blocks
	
def block_map(blocks):
	out = {}
	for block in blocks:
		if 'label' in block[0]:
			name = block[0]['label']
			block = block[1:]
		else:
			name = 'b{}'.format(len(out)) # unique name
			
		out[name] = block
		
	return out

def get_cfg(blockmap):
	out = {}
	for i, (name, block) in enumerate(blockmap.items()):
		last = block[-1]
		if last['op'] in ['jmp', 'br']:
			suc = last['labels']
		elif last['op'] == 'ret':
			suc = []
		else:
			if i == len(blockmap) - 1:
				suc = []
			else:
				suc = [list(blockmap.keys())[i + 1]]
		out[name] = suc
	return out
		
def edges(cfg):
	succ = {b: [] for b in cfg}
	pred = {b: [] for b in cfg}
	for b in cfg:
		for out in cfg[b]:
			succ[b].append(out)
			pred[out].append(b)
	return succ, pred

def mycfg():
	prog = json.load(sys.stdin)
	func = prog['functions'][0]
	blocks = create_blocks(func['instrs'])
	blockmap = block_map(blocks)
	cfg = get_cfg(blockmap)
	
	return blocks, cfg

if __name__ == "__main__":
	mycfg()