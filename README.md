Live App Demo: [Visualizing Fractal Snowflakes](https://visualize-fractals-realtime.streamlit.app/)

# Visualizing Fractal Snowflakes in Real Time

This applied science project turns mathematical theory into clean, highly efficient functional software. Starting with fractals invented in my PhD research, this project builds an interactive tool that visualizes these objects and runs empirical complexity benchmarks on the underlying code.  

**Main Idea**: Uses computationally expensive objects called snowflake fractals to demonstrate the efficiency gains achieved through NumPy vectorization vs pure Python loops. Vectorized code is used to deploy the app. 

**Main steps of this project:**

1. **Algorithmize**: Convert a mathematical construction into a clean python algorithm. 
2. **Vectorize**: The code is vectorized while keeping the underlying logic intact.
3. **Empirical Complexity Analysis**: A deep run time analysis  is performed to see how much faster the vectorized code is.
4. **Deploy**: [fractal.py](./fractal.py) contains the deployment code for the web app. 

[Interactive web app](): Displays real-time rendering with parameter manipulation and runtime benchmarks.

**Dictionary:**

1. Fractal: For our purpose, a fractal is simply a shape with intricate geometry that "looks" the same upon zooming into the shape. 
2. Koch Snowflake: This phrase always refers to Koch's original construction of his namesake fractal.
3. Modified Snowflakes: This is an infinite family of snowflake like curves of which Koch is a special case.

Here an abridged version of my dissertation if you're curious about the math behind this project: [see section 2.2](https://scholarspace.manoa.hawaii.edu/server/api/core/bitstreams/31ac5794-df3a-4efa-b2cf-27ec43a9976a/content).