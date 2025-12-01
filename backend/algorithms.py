import pandas as pd

def solve_fifo(pages, capacity):
    memory = []
    faults, hits = 0, 0
    history = []
    
    for page in pages:
        status = "Miss"
        if page in memory:
            status = "Hit"
            hits += 1
        else:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
        
        # FIX: Convert all page numbers to strings to avoid Type Error with '-'
        mem_view = [str(x) for x in memory] + ['-'] * (capacity - len(memory))
        
        history.append({
            "Incoming": str(page), # Convert to string for consistency
            "Memory": mem_view,
            "Status": status
        })
        
    return faults, hits, history

def solve_lru(pages, capacity):
    memory = []
    faults, hits = 0, 0
    history = []
    
    for page in pages:
        status = "Miss"
        if page in memory:
            status = "Hit"
            hits += 1
            memory.remove(page)
            memory.append(page)
        else:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
        
        # FIX: Convert all page numbers to strings
        mem_view = [str(x) for x in memory] + ['-'] * (capacity - len(memory))
        
        history.append({
            "Incoming": str(page),
            "Memory": mem_view,
            "Status": status
        })
    return faults, hits, history

def solve_optimal(pages, capacity):
    memory = []
    faults, hits = 0, 0
    history = []
    
    for i, page in enumerate(pages):
        status = "Miss"
        if page in memory:
            status = "Hit"
            hits += 1
        else:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                future_uses = []
                for mem_page in memory:
                    if mem_page in pages[i+1:]:
                        future_uses.append(pages[i+1:].index(mem_page))
                    else:
                        future_uses.append(9999)
                
                victim_idx = future_uses.index(max(future_uses))
                memory[victim_idx] = page
        
        # FIX: Convert all page numbers to strings
        mem_view = [str(x) for x in memory] + ['-'] * (capacity - len(memory))
        
        history.append({
            "Incoming": str(page),
            "Memory": mem_view,
            "Status": status
        })
    return faults, hits, history