# Create a 3D visualization for distributed fiber optic sensing data for microseismic events.
# Author: Kailey Dougherty
# Date created: 24-FEB-2025
# Date last modified: 12-MAR-2025

# Import needed libraries
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go


class DataViewer:
	
	def __init__(self, plot_objects):
		self.plot_objects = plot_objects
	
	def	draw(self):
		fig = go.Figure()

		for b in self.plot_objects:
			# Check if the object is a list
			if isinstance(b, list):
				for c in b:
					if isinstance(c, go.Scatter3d):  #If yes, add as trace
						fig.add_trace(c)
					else:  #Otherwise, print error message
						print(f"Invalid object: {c}")
			else:			
				# Check if the object is valid
				if isinstance(b, go.Scatter3d):  #If yes, add as trace
					fig.add_trace(b)
				else:  #Otherwise, print error message
					print(f"Invalid object: {b}")

	
		fig.update_layout()
		
		return fig.show()