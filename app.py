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
with tab1:
    st.subheader("Step-by-Step Page Replacement Visualization")
    algo_choice = st.radio("Algorithm Strategy", ["FIFO", "LRU", "Optimal"], horizontal=True)
    
    if st.button("Run Simulation", type="primary"):
        try:
            # --- THE FIX: Robust Input Parsing ---
            # 1. Replace spaces with nothing (handles "1, 2" vs "1,2")
            # 2. Split by comma
            # 3. Filter out empty strings (handles trailing commas "1,2,")
            # 4. Ensure only digits are processed
            raw_items = [x.strip() for x in ref_string.split(",") if x.strip()]
            pages = [int(x) for x in raw_items if x.isdigit()]
            
            if not pages:
                st.error("Please enter at least one valid number.")
            else:
                # Run the selected algorithm
                if algo_choice == "FIFO": f, h, hist = algorithms.solve_fifo(pages, capacity)
                elif algo_choice == "LRU": f, h, hist = algorithms.solve_lru(pages, capacity)
                else: f, h, hist = algorithms.solve_optimal(pages, capacity)
                
                # Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Page Faults", f, delta_color="inverse")
                c2.metric("Total Hits", h)
                c3.metric("Hit Ratio", f"{h/len(pages)*100:.1f}%")
                
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
    st.subheader("Algorithm Efficiency Benchmark")
    if st.button("Run Benchmark Test"):
        pages = [int(x.strip()) for x in ref_string.split(",")]
        f_fifo, _, _ = algorithms.solve_fifo(pages, capacity)
        f_lru, _, _ = algorithms.solve_lru(pages, capacity)
        f_opt, _, _ = algorithms.solve_optimal(pages, capacity)
        
        data = {"FIFO": f_fifo, "LRU": f_lru, "Optimal": f_opt}
        fig, ax = plt.subplots(figsize=(6,3))
        bars = ax.bar(data.keys(), data.values(), color=['#FF9999', '#66B2FF', '#99FF99'])
        ax.set_ylabel("Page Faults")
        st.pyplot(fig)
        st.info(f"🏆 Winner: {min(data, key=data.get)} with {min(data.values())} faults.")

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