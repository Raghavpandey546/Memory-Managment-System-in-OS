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

def solve_lfu(pages, capacity):
    """
    Least Frequently Used: Replaces the page with the fewest visits.
    Tie-breaking: If two pages have the same frequency, use FIFO (replace the older one).
    """
    memory = []
    faults, hits = 0, 0
    history = []
    frequency = {} # Tracks how many times a page is accessed
    
    for page in pages:
        status = "Miss"
        
        # Update frequency for the current page
        frequency[page] = frequency.get(page, 0) + 1
        
        if page in memory:
            status = "Hit"
            hits += 1
            # In LFU, we don't move the page effectively, we just update frequency
        else:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                # Find the page in memory with the minimum frequency
                # min() finds the key with smallest value. 
                # Since 'memory' is a list (ordered), it picks the first one in case of ties (FIFO tie-breaker)
                victim = min(memory, key=lambda x: frequency[x])
                
                memory.remove(victim)
                memory.append(page)
                
                # Optional: Reset frequency of victim? 
                # In standard LFU, we usually remove the victim's count or keep it. 
                # For strictly local replacement, we usually remove it.
                del frequency[victim] 

        # Format for visualization
        mem_view = [str(x) for x in memory] + ['-'] * (capacity - len(memory))
        history.append({
            "Incoming": str(page),
            "Memory": mem_view,
            "Status": status
        })
        
    return faults, hits, history

def solve_mru(pages, capacity):
    """
    Most Recently Used: Replaces the page that was just added/accessed.
    (Opposite of LRU). Good for cyclic scanning.
    """
    memory = []
    faults, hits = 0, 0
    history = []
    
    for page in pages:
        status = "Miss"
        if page in memory:
            status = "Hit"
            hits += 1
            # Move to end (mark as most recently used)
            memory.remove(page)
            memory.append(page)
        else:
            faults += 1
            if len(memory) < capacity:
                memory.append(page)
            else:
                # MRU logic: Remove the LAST element (the most recent one)
                memory.pop() 
                memory.append(page)
        
        mem_view = [str(x) for x in memory] + ['-'] * (capacity - len(memory))
        history.append({
            "Incoming": str(page),
            "Memory": mem_view,
            "Status": status
        })
        
    return faults, hits, history