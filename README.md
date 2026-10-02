# Bow-Thruster CFD Post-Processing using Python and ParaView

Python and ParaView automation for vortex visualization and total-pressure post-processing of an existing OpenFOAM bow-thruster CFD simulation.

## Overview

This project develops a reproducible CFD post-processing workflow using Python and ParaView.

The work focuses on automating the visualization and analysis of an existing OpenFOAM bow-thruster simulation, with particular emphasis on:

- Q-criterion vortex identification
- Tip-vortex visualization
- Hub and junction vortex visualization
- Transient vortex-field visualization
- Total-pressure calculation
- Moving-slice pressure-field visualization
- Consistent camera and colour settings
- Reproducible extraction of CFD visualizations

The objective was to reduce repetitive manual post-processing and create a consistent workflow for analyzing transient CFD results.

## Tools and Technologies

- Python
- ParaView
- OpenFOAM
- CFD post-processing
- Q-criterion
- Scientific visualization
- Engineering automation

## Workflow

The project follows the general workflow:

OpenFOAM simulation results  
↓  
ParaView processing pipeline  
↓  
Q-criterion calculation  
↓  
Q-range calibration  
↓  
Vortex visualization  
↓  
Transient visualization automation  

and, for pressure analysis:

OpenFOAM simulation results  
↓  
Velocity and pressure fields  
↓  
Total-pressure calculation  
↓  
Moving X-Z slice  
↓  
Automated pressure-field visualization

## Q-Criterion Visualization

Q-criterion was used to identify vortical structures around the bow-thruster assembly.

A dedicated calibration workflow was used to compare visualization ranges before selecting the final settings.

The selected display ranges were:

| Analysis | Q Range |
|---|---:|
| Tip vortex | 50–600 |
| Hub / junction vortex | 50–1200 |
| Combined visualization | 50–1100 |

For the transient combined vortex visualization, a visualization-suppression threshold of:

`Q = 550`

was used.

This separates the calibration of the display range from the threshold used to suppress weaker structures in the transient visualization.

## Total-Pressure Analysis

Total pressure was calculated using:

`p_total = p + 0.5 * rho * |U|^2`

with:

`rho = 1025 kg/m³`

The pressure field was visualized using a Y-normal X-Z slice.

The slice was moved from:

`Y = +0.3 m`

to:

`Y = -1.5 m`

to examine changes in the total-pressure field at different positions.

## Automation

Python was used with ParaView to make the post-processing workflow reproducible.

The automation addressed tasks such as:

- creation and configuration of visualization pipelines
- consistent visualization settings
- Q-criterion range calibration
- transient visualization
- moving-slice pressure analysis
- extraction of representative result frames

This approach reduces repetitive manual interaction when processing multiple CFD states or visualization positions.

## Repository Structure

```text
.
├── src/
│   └── Python / ParaView automation scripts
├── images/
│   └── Selected CFD visualizations
├── results/
│   └── Selected post-processing outputs
├── docs/
│   └── Supporting project documentation
├── .gitignore
└── README.md
