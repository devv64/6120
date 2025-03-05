import cfg as mycfg

def find_doms(blocks):
    dom = {s: set(blocks.keys()) for s in blocks}
    entry = next(iter(blocks))
    dom[entry] = {entry}

    changed = True
    while changed:
        changed = False
        for s in blocks:
            if s == entry:
                continue

            new_dom = set(blocks.keys())
            for p in pred[s]:
                new_dom.intersection_update(dom[p])

            new_dom.add(s)
            if new_dom != dom[s]:
                dom[s] = new_dom
                changed = True
    return dom

def immediate_dominators(dom):
    idom = {}
    entry = next(iter(dom))
    idom[entry] = None

    for node in dom:
        if node == entry:
            continue
            
        dominators = dom[node].copy()
        dominators.remove(node)
        
        for d in dominators:
            immediate = True
            for other in dominators:
                if d != other and d in dom[other]:
                    immediate = False
                    break
            if immediate:
                idom[node] = d
                break

    return idom

def dominator_tree(idom):
    tree = {node: set() for node in idom}
    
    for node, node_idom in idom.items():
        if node_idom is not None:
            tree[node_idom].add(node)
            
    return tree

def post_dominators(cfg, succ):
    post_dom = {s: set(cfg.keys()) for s in cfg}
    exit_node = [n for n in cfg if not succ[n]]
    exit_node = exit_node[0] if exit_node else None
    post_dom[exit_node] = {exit_node} if exit_node else set()

    changed = True
    while changed:
        changed = False
        for s in cfg:
            if s == exit_node:
                continue

            new_post_dom = set(cfg.keys())
            for succ_node in succ[s]:
                new_post_dom.intersection_update(post_dom[succ_node])

            new_post_dom.add(s)
            if new_post_dom != post_dom[s]:
                post_dom[s] = new_post_dom
                changed = True
    return post_dom

def dominance_frontier(cfg, dom, idom, preds):
    dom_front = {s: set() for s in dom}

    for node in cfg:
        for other in cfg:
            for pred in preds[other]:
                if node in dom[pred] and node not in dom[other]:
                    dom_front[node].add(other)
                    break

    return dom_front


if __name__ == "__main__":
    blocks, cfg = mycfg.mycfg()
    succ, pred = mycfg.edges(cfg)
    dom = find_doms(cfg)
    idom = immediate_dominators(dom)
    tree = dominator_tree(idom)
    post_dom = post_dominators(cfg, succ)
    dom_front = dominance_frontier(cfg, dom, idom, pred)
    print("Dominators:")
    for node, dom_set in dom.items():
        print(f"{node}: {', '.join(dom_set)}")

    print("--"*20)
    print("Dominator Tree:")
    for node, children in tree.items():
        print(f"{node}: {', '.join(children)}")
    print("--"*20)

    print("Immediate Dominators:")
    for node, idom in idom.items():
        print(f"{node}: {idom}")
    print("--"*20)

    print("Dominance Frontier:")
    for node, dom_front_set in dom_front.items():
        print(f"{node}: {', '.join(dom_front_set)}")

