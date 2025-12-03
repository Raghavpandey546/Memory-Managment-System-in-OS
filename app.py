import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import algorithms, mmu, rag 

st.set_page_config(page_title="MemVisor OS Suite", layout="wide", page_icon="💾")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/dusk/64/000000/server.png", width=50)
    st.title("MemVisor Pro")
    st.info("Operating System Project")
    
    st.markdown("### ⚙️ Simulator Config")
    capacity = st.slider("RAM Frames", 3, 8, 3)
    ref_string = st.text_input("Reference String", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3")
    
    st.markdown("---")
    st.caption("Modules: Algo Sim | MMU | Arena | AI-Docs")

# --- MAIN APP ---
st.title("💾 Advanced Memory Management Suite")
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Algo Simulator", "⚙️ MMU Hardware", "📊 Comparison Arena", "🤖 OS Assistant"])

# === TAB 1: ALGORITHMS ===
# ... inside Tab 1 ...
with tab1:
    st.subheader("Step-by-Step Visualization")
    
    # UPDATE THIS LINE TO INCLUDE LFU AND MRU
    algo_choice = st.radio("Strategy", ["FIFO", "LRU", "Optimal", "LFU", "MRU"], horizontal=True)
    # Ensure this is inside the 'try:' block in Tab 1
    raw_items = [x.strip() for x in ref_string.split(",") if x.strip()]
    pages = [int(x) for x in raw_items if x.isdigit()]
    
    if st.button("Run Simulation", type="primary"):
        try:
            # ... (input parsing code) ...
            
            # UPDATE THIS BLOCK
            if algo_choice == "FIFO": f, h, hist = algorithms.solve_fifo(pages, capacity)
            elif algo_choice == "LRU": f, h, hist = algorithms.solve_lru(pages, capacity)
            elif algo_choice == "LFU": f, h, hist = algorithms.solve_lfu(pages, capacity)
            elif algo_choice == "MRU": f, h, hist = algorithms.solve_mru(pages, capacity)
            else: f, h, hist = algorithms.solve_optimal(pages, capacity)

                # Visualization
            df = pd.DataFrame(hist)
            def highlight(val):
                if val == 'Hit':
                    return 'background-color: #196F3D; color: white' # Dark Green
                elif val == 'Miss':
                    return 'background-color: #943126; color: white' # Dark Red
                return ''
            st.dataframe(df.style.applymap(highlight, subset=['Status']), use_container_width=True)
        except Exception as e:
            st.error(f"Error processing input: {e}")
            
# === TAB 2: MMU HARDWARE ===
with tab2:
    st.subheader("⚙️ Hardware Address Translation (MMU)")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("#### Input")
        v_addr = st.text_input("Virtual Address (Hex)", "0x3A7F")
        p_size = st.selectbox("Page Size", [4, 8])
        st.info(f"Page Size: {p_size}KB\nOffset Bits: {13 if p_size==8 else 12}")
    
    with col2:
        st.markdown("#### Translation Flow")
        res = mmu.translate_address(v_addr, p_size)
        
        if res["valid"]:
            # 1. VISUAL FLOWCHART (The "Detailed Graph")
            # We use Graphviz to draw the translation logic
            graph = f"""
            digraph MMU {{
                rankdir=LR;
                node [shape=box, style=filled, fillcolor="#f9f9f9"];
                
                VA [label="Virtual Addr\\n{v_addr}", fillcolor="#e1f5fe"];
                Split [shape=diamond, label="Split bits"];
                
                Page [label="Page #{res['page_num']}\\n(Binary: {res['binary_page']})", fillcolor="#d4edda"];
                Offset [label="Offset: {res['offset_hex']}\\n(Binary: {res['binary_offset']})", fillcolor="#fff3cd"];
                
                PT [label="Page Table\\nLookup", shape=cylinder];
                Frame [label="Frame #??", fillcolor="#d4edda"];
                
                PA [label="Physical Addr\\n(Frame + Offset)", fillcolor="#ffebee"];
                
                VA -> Split;
                Split -> Page [label="Upper Bits"];
                Split -> Offset [label="Lower {res['offset_bits']} Bits"];
                Page -> PT -> Frame;
                Frame -> PA;
                Offset -> PA;
            }}
            """
            st.graphviz_chart(graph)
            
            # 2. BITWISE BREAKDOWN TABLE
            st.markdown("#### Bitwise Decomposition")
            
            # Create a stylized explanation
            bit_cols = st.columns(3)
            with bit_cols[0]:
                st.metric("1. Virtual Address", v_addr, help=f"Decimal: {int(v_addr, 16)}")
            with bit_cols[1]:
                st.metric("2. Page Number (p)", res['page_num'], delta=f"Bits: 15-{res['offset_bits']}")
            with bit_cols[2]:
                st.metric("3. Offset (d)", res['offset_hex'], delta=f"Bits: {res['offset_bits']-1}-0")
            
            # Visual Binary Split
            st.code(f"""
Binary Analysis:
  {res['binary_full']}  (Total 16 bits)
  |{''.ljust(len(res['binary_page']), '-')}||{''.ljust(len(res['binary_offset']), '-')} |
   Page #   Offset
   {res['binary_page']}      {res['binary_offset']}
            """, language="text")
            
        else:
            st.error("Invalid Hex Address. Try 0x1A2B")

# === TAB 3: COMPARISON ARENA ===
with tab3:
    st.header("📊 Algorithm Efficiency Benchmark")
    
    # 1. INPUT SECTION
    st.caption("Compare how different algorithms handle the same workload.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        # Re-parse input here to ensure it updates live
        raw_items = [x.strip() for x in ref_string.split(",") if x.strip()]
        pages = []
        if raw_items:
            pages = [int(x) for x in raw_items if x.isdigit()]

    if not pages:
        st.warning("Please enter a valid Reference String in the sidebar.")
    else:
        # --- SECTION A: CURRENT CONFIG COMPARISON ---
        st.subheader(f"1. Snapshot Comparison (Frames: {capacity})")
        
        if st.button("Run Snapshot Benchmark"):
            # Run all algorithms
            f1,_,_ = algorithms.solve_fifo(pages, capacity)
            f2,_,_ = algorithms.solve_lru(pages, capacity)
            f3,_,_ = algorithms.solve_optimal(pages, capacity)
            f4,_,_ = algorithms.solve_lfu(pages, capacity)
            f5,_,_ = algorithms.solve_mru(pages, capacity)
            
            # Plot Bar Chart
            fig, ax = plt.subplots(figsize=(8, 3))
            strategies = ["FIFO", "LRU", "OPT", "LFU", "MRU"]
            faults = [f1, f2, f3, f4, f5]
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#D7BDE2']
            
            bars = ax.bar(strategies, faults, color=colors)
            ax.set_ylabel("Page Faults")
            
            # Add labels
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
            
            st.pyplot(fig)
            
            # Smart Insight
            best_algo = strategies[faults.index(min(faults))]
            st.success(f"🏆 Recommendation: Use **{best_algo}** for this specific workload.")

        st.markdown("---")

        # --- SECTION B: SENSITIVITY ANALYSIS (The New Feature) ---
        st.subheader("2. Sensitivity Analysis (Belady's Anomaly Test)")
        st.caption("How does increasing RAM (Frames) affect performance? Does adding more memory always help?")
        
        if st.button("Run Multi-Frame Stress Test"):
            with st.spinner("Simulating hardware variations..."):
                # Data structure to hold results: { "FIFO": [12, 10, 9...], "LRU": ... }
                results = {"FIFO": [], "LRU": [], "OPT": []}
                frame_range = range(3, 8) # Test frame sizes 3 to 7
                
                for f_size in frame_range:
                    f_fifo,_,_ = algorithms.solve_fifo(pages, f_size)
                    f_lru,_,_ = algorithms.solve_lru(pages, f_size)
                    f_opt,_,_ = algorithms.solve_optimal(pages, f_size)
                    
                    results["FIFO"].append(f_fifo)
                    results["LRU"].append(f_lru)
                    results["OPT"].append(f_opt)
                
                # Plot Line Chart
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                ax2.plot(frame_range, results["FIFO"], marker='o', label="FIFO", color='#FF9999', linestyle='--')
                ax2.plot(frame_range, results["LRU"], marker='s', label="LRU", color='#66B2FF')
                ax2.plot(frame_range, results["OPT"], marker='^', label="Optimal", color='#99FF99')
                
                ax2.set_xlabel("Number of Frames (RAM Size)")
                ax2.set_ylabel("Total Page Faults")
                ax2.set_title("Performance vs. Memory Size")
                ax2.legend()
                ax2.grid(True, linestyle=':', alpha=0.6)
                
                st.pyplot(fig2)
                
                # Check for Belady's Anomaly in FIFO
                # (If faults INCREASE as frames INCREASE)
                fifo_faults = results["FIFO"]
                has_belady = False
                for i in range(len(fifo_faults)-1):
                    if fifo_faults[i+1] > fifo_faults[i]:
                        has_belady = True
                        break
                
                if has_belady:
                    st.error("⚠️ **Belady's Anomaly Detected!** Increasing frame size actually hurt FIFO performance.")
                    st.markdown("""
                    **Explanation:** In FIFO, replacing pages without considering usage history can sometimes lead to *more* faults when memory increases. 
                    [cite_start]This is a famous OS paradox[cite: 43].
                    """)
                else:
                    st.info("✅ No anomalies detected. Performance improved or stayed stable as RAM increased.")

# === TAB 4: CHATBOT ===
with tab4:
    st.markdown("## 🤖 AI Knowledge Assistant")
    
    # Load PDF (Keep your existing loading logic here)
    pdf_path = "assets/os_notes.pdf"
    if 'pdf_chunks' not in st.session_state:
        with st.spinner("Processing Knowledge Base..."):
            chunks = rag.process_pdf(pdf_path)
            st.session_state.pdf_chunks = chunks

    # Chat Interface
    user_query = st.chat_input("Ask about Paging, Segmentation, or Deadlocks...")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if user_query:
        if st.session_state.pdf_chunks:
            answer, score = rag.get_answer(user_query, st.session_state.pdf_chunks)
            
            # Store history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            st.session_state.chat_history.append({"role": "assistant", "content": answer, "score": score})
        else:
            st.error("Please add 'os_notes.pdf' to assets folder first.")

    # Display Chat History Beautifully
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                # 1. Show the Text
                st.markdown(f"**Answer:** \n\n{msg['content']}")
                
                # 2. Show the "Confidence Meter" (The Beauty Part)
                if "score" in msg and msg['score'] > 0:
                    score = msg['score']
                    color = "green" if score > 50 else "orange"
                    st.caption(f"Relevance Match: {score}%")
                    st.progress(int(score))