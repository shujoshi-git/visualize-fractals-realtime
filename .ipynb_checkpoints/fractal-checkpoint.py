import numpy as np
import matplotlib.pyplot as plt
import time
import streamlit as st


# Unvectorized and vectorized function takem as-it-is from snowflakes.ipynb.

# (Unvectorized) function to generate a modified snowflake curve.

# Parameters:
#    points: The starting segment. i.e., the zeroth generation of the fractal. 
#    k: The starting step counter. Cannot be initialized inside the function body since the function calls itself within its body.
#    max_gen: number of iterations we wish to perform.
#    a: A fixed number between 1/4 and 1/3 that determines the shape of the fractal. 
#    side_length : the side length of the starting equilateral triangle.

def modified_snowflake(max_gen, a, side_length = 1.0):
    
    def modified_koch_curve(points, k, max_gen, a):
        # Stop recursion when max generation is reached.
        if k > max_gen:
            return points
            
        new_points = []
    
        # Compute base length for current generation k.
        r = (a) ** k  
    
        # Process each segment sequentially.
        for i in range(len(points) - 1):
            A = np.array(points[i])
            B = np.array(points[i + 1])
            AB = B - A
            L = np.linalg.norm(AB)
    
            # Determine unit direction and perpendicular normal vector.
            unit_AB = AB / L
            normal = np.array([-unit_AB[1], unit_AB[0]])  
    
            # Calculate base length of new triangles and margins along current segment.
            base_length = r 
            margin = (L - base_length) / 2
    
            # Locate base end-points P1 and P2, and midpoint M.
            P1 = A + unit_AB * margin          
            P2 = A + unit_AB * (margin + base_length)  
            M = (P1 + P2) / 2                   
    
            # Calculate the peak vertex of the new triangle.
            height = (np.sqrt(3) / 2) * base_length
            P3 = M + normal * height        
    
            # Append transformed sequence of 4 points replacing segment AB.
            new_points += [tuple(A), tuple(P1), tuple(P3), tuple(P2)]
    
        # Re-attach final endpoint to complete the segment.
        new_points.append(tuple(points[-1]))  
    
        # Iterate/recurse to next generation with updated point list.
        return modified_koch_curve(new_points, k + 1, max_gen,a)

    # Define the 3 vertices of an equilateral triangle.
    p1 = (0.0, 0.0)
    p2 = (side_length, 0.0)
    p3 = (side_length / 2.0, (np.sqrt(3) / 2.0) * side_length)
    
    # Define the initial closed loop (0th generation).
    initial_triangle = [p1, p3, p2, p1]
    
    # Generate the fractal curve across all 3 sides simultaneously.
    return modified_koch_curve(initial_triangle, k = 1, max_gen = max_gen, a = a)




# (Vectorized) function to generate a modified snowflake curve.

def vectorized_snowflake(max_gen, a, side_length = 1.0):

    def vectorized_modified_koch(points, k, max_gen, a):
        if k > max_gen:
            return points
    
        pts = np.asarray(points, dtype = float)
        r = (a) ** k  
    
        A = pts[:-1]
        B = pts[1:]
        AB = B - A
        L = np.linalg.norm(AB, axis = 1, keepdims = True)
    
        unit_AB = AB / L
        normal = np.column_stack((-unit_AB[:, 1], unit_AB[:, 0]))
    
        base_length = r 
        margin = (L - base_length) / 2
    
        P1 = A + unit_AB * margin
        P2 = A + unit_AB * (margin + base_length)
        M = (P1 + P2) / 2
    
        height = (np.sqrt(3) / 2) * base_length
        P3 = M + normal * height
    
        num_segments = len(A)
        new_points = np.empty((num_segments * 4 + 1, 2), dtype=float)
        new_points[0:-1:4] = A
        new_points[1:-1:4] = P1
        new_points[2:-1:4] = P3
        new_points[3:-1:4] = P2
    
        new_points[-1] = pts[-1]
    
        return vectorized_modified_koch(new_points, k + 1, max_gen, a)
    
    p1 = (0.0, 0.0)
    p2 = (side_length, 0.0)
    p3 = (side_length / 2.0, (np.sqrt(3) / 2.0) * side_length)

    initial_triangle = np.array([p1, p3, p2, p1], dtype = float)

    return vectorized_modified_koch(initial_triangle, k = 1, max_gen = max_gen, a = a)

    

#-----------------------------



#  Streamlit Layout

st.set_page_config(page_title = "Visualizing Fractals In Real Time", layout = "wide")

# Keep slider limits always visible. 

st.markdown("""
    <style>
    /* Force every text element and tick inside any slider container to stay visible */
    div[data-testid="stSlider"] * {opacity: 1 !important; visibility: visible !important;}
    
    /* Ensure the slider track container doesn't obscure text overflow */
    div[data-testid="stSlider"] {padding-bottom: 10px;}
    </style>
""", unsafe_allow_html = True)



# Sidebar


with st.sidebar:
    st.markdown("<h1 style = 'text-align: center;'>About This Visualizer</h1>", unsafe_allow_html = True)
    st.markdown("""
    <div style = "text-align: justify;">
    <i> This applied science project utilizes computationally expensive objects called snowflake fractals to demonstrate the efficiency gains achieved through <b>NumPy vectorization</b> vs <b>pure Python loops</b>. These fractals were introduced by me to disprove a mathematical conjecture as part of my PhD research. For more information on the mathematics and algorithms of this project, click <a href="https://github.com/shujoshi-git/fractals-research-code/blob/main/snowflakes.ipynb" target="_blank" style="color: #66c0f4; text-decoration: underline; font-weight: bold;">here</a>.</i>
    </div>
    
    """, unsafe_allow_html = True)

    st.write("---")
    
# Centered "About Me" heading.
    st.markdown("<h3 style='text-align: center;'> About Me</h3>", unsafe_allow_html = True)
    st.markdown("""
    <div style = "text-align: justify;">
    <b>Shubham Joshi, Ph.D.</b><br/>
    <i> Applied scientist with expertise in data science and machine learning. In a past life, I was a mathematician who studied beautiful shapes called fractals.</i>
    </div>
    """, unsafe_allow_html = True)
    
# Links.
    st.markdown("""
    <div style = "display: flex; gap: 15px; justify-content: center; margin-top: 15px;">
        <a href = "https://github.com/shujoshi-git" target="_blank" style="text-decoration: none; color: #66c0f4; font-weight: bold;"> GitHub</a>
        <a href = "https://www.linkedin.com/in/shubham-joshi-ph-d-1625b626b/" target="_blank" style="text-decoration: none; color: #66c0f4; font-weight: bold;"> LinkedIn</a>
        <a href = "mailto:shujoshi.work@gmail.com" style="text-decoration: none; color: #66c0f4; font-weight: bold;"> Email</a>
    </div>
    """, unsafe_allow_html = True)

# Header section.
st.title("Visualizing Fractals In Real Time: Run Time Analysis")
st.subheader("Use the sliders to toggle the scaling factor and generation. Check out the run time analysis to see how run time compares for unvectorized code (Python lists) vs vectorized code (NumPy arrays).")



# Configuration.

left_vis_col, right_controls_col = st.columns([1, 1])

with right_controls_col:
    
    with st.container(border=True):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0;'>Configuration</h4>", unsafe_allow_html = True)
        slider_col1, slider_col2 = st.columns(2)

        with slider_col1:
            generations = st.slider("Resolution", min_value = 1, max_value = 8, value = 7)

        with slider_col2:
            scaling_factor = st.slider("Scaling Factor", min_value = 0.20, max_value = 0.35, value = 0.28, step = 0.01, format = "%.2f")

# Compute timings using current slider inputs. Cannot use %timeit. 
t0 = time.perf_counter()
unvec_curve = modified_snowflake(max_gen = generations, a = scaling_factor, side_length = 1.0)
t1 = time.perf_counter()
unvec_time_ms = (t1 - t0) * 1000.0

t2 = time.perf_counter()
vec_curve = vectorized_snowflake(max_gen = generations, a = scaling_factor, side_length = 1.0)
t3 = time.perf_counter()
vec_time_ms = (t3 - t2) * 1000.0

speedup_factor = unvec_time_ms / vec_time_ms if vec_time_ms > 0 else 1.0


# Snowflake visualization.

with left_vis_col:
    fig_vis, ax = plt.subplots(figsize = (5, 4.5))

    # Center coordinates around zero.
    vec_arr = vec_curve - [0.5, 0.3]

    ax.plot(vec_arr[:, 0], vec_arr[:, 1], color = "#1f77b4", linewidth = 1.0) # This color looks "icy blue" :)
    ax.set_title("Snowflake Fractal", fontsize = 11)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout()
    st.pyplot(fig_vis, use_container_width = True)


# Run Time Stats and Sppedup Factor.

with right_controls_col:

    # Bar Chart Container
    with st.container(border = False):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0;'>Live Run Time Stats</h4>", unsafe_allow_html = True)
        
        fig_bar, ax_bar = plt.subplots(figsize = (4.5, 1.8))
        categories = ['Unvectorized', 'Vectorized']
        times = [unvec_time_ms, vec_time_ms]
        colors = ['#ff4d4d', '#1f77b4']

        bars = ax_bar.barh(categories, times, color = colors, height = 0.4)
        ax_bar.set_xlim(0, max(times) * 1.25 if max(times) > 0 else 1.0)
        ax_bar.grid(axis = 'x', linestyle = '-', alpha = 0.3)
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)

        for bar, time_val in zip(bars, times):
            ax_bar.text(
                bar.get_width() + (max(times) * 0.03 if max(times) > 0 else 0.1), bar.get_y() + bar.get_height()/2, 
                f"{time_val:.1f} ms",va = 'center', fontsize = 9)

        plt.tight_layout()
        st.pyplot(fig_bar, use_container_width =True)

# Speedup Factor.
    
    with st.container(border = False):
        st.markdown("<h4 style='text-align: center; margin-bottom: 0;'>Speed Up Factor</h4>", unsafe_allow_html=  True)
        st.markdown(f"<h1 style='text-align: center; color: #2ca02c; margin-top: 0;'>{speedup_factor:.2f}x</h1>", unsafe_allow_html = True)


# Scaling plot.

st.markdown("---")
st.markdown("<h3 style='text-align: center;'>Run Time Scaling with Resolution</h3>", unsafe_allow_html =True)

st.image("plots/runtime_plot.png", use_container_width = True)

st.markdown("""
#### **Key Performance Takeaway**: As computations become more demanding (resolution > 5), vectorized code performs roughly 100x better than its unvectorized counterpart. Vectorizing allows visualizing (rendering) these complex shapes in real time. 
""")