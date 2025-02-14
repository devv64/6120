import json
import sys
import cfg as mycfg


# ! from https://github.com/sampsyo/bril/blob/main/examples/df.py
def fmt(val):
    """Guess a good way to format a data flow value. (Works for sets and
    dicts, at least.)
    """
    if isinstance(val, set):
        if val:
            return ', '.join(v for v in sorted(val))
        else:
            return '∅'
    elif isinstance(val, dict):
        if val:
            return ', '.join('{}: {}'.format(k, v)
                             for k, v in sorted(val.items()))
        else:
            return '∅'
    else:
        return str(val)

def df(cfg, merge, transfer):
	cfg_mapping = {}
	for i, x in enumerate(cfg):
		cfg_mapping[x] = i
	succ, pred = mycfg.edges(cfg)
	# * init
	worklist = list(cfg.keys())
	input = {worklist[0]: {}}
	output = {b: {} for b in cfg}
	while worklist != []:
		b = worklist.pop()
		input[b] = merge(output[p] for p in pred[b])
		out = transfer(blocks[cfg_mapping[b]], input[b])
		if out != output[b]:
			output[b] = out
			worklist += succ[b]
	return input, output
	
# * reaching definitions
def rd_merge(lst):
    return set(i for l in lst for i in l)

def rd_transfer(block, prev_input):
	out = set(prev_input)
	for instr in block:
		if 'dest' in instr:
			out.add(instr['dest'])
	return out

# * constant propagation
def cp_merge(val_list):
    out = {}
    for lst in val_list:
        for name, val in lst.items():
            if name in out:
                if out[name] != val:
                    out[name] = '?'
            else:
                out[name] = val
    return out

def cp_transfer(block, prev_input):
    out = dict(prev_input)
    for instr in block:
        if 'dest' in instr:
            if instr['op'] == 'const':
                out[instr['dest']] = instr['value']
            else:
                out[instr['dest']] = '?'
    return out

if __name__ == "__main__":
	blocks, cfg = mycfg.mycfg()
	inp, out = df(cfg, cp_merge, cp_transfer)
	for block in cfg:
		print('{}:'.format(block))
		print('  in: ', fmt(inp[block]))
		print('  out:', fmt(out[block]))
	
    # * computing data flow analysis, not producing new bril code
	