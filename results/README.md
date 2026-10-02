# CFD Post-Processing Results

This folder contains the main animation results from the automated post-processing workflow developed for an existing OpenFOAM bow-thruster CFD simulation.

The workflow uses Python and ParaView to automate Q-criterion vortex visualization and total-pressure field analysis.

## 1. Transient Q-Criterion Visualization

The combined blade-tip and hub/junction Q-criterion workflow was applied across the available transient CFD time steps.

The visualization configuration was kept consistent throughout the animation to support qualitative comparison between time steps.

### Visualization Settings

- Q-criterion display range: **50–1100**
- Visualization-suppression threshold: **Q = 550**
- Slice normal: **[1, 0, 0]**
- Slice plane: **Y-Z**
- Camera direction: along the X-axis
- Fixed camera and colour range across the transient sequence

The animation shows how the visible Q-criterion structures change with CFD time while the post-processing geometry remains fixed.

> **Important:** Q = 550 is used as a visualization-suppression threshold for visual clarity. It should not be interpreted as a universal physical vortex boundary or as a numerically validated noise threshold.

### Animation

`transient_q_criterion.mp4`

Representative frames from this animation are available in the [`images`](../images/) directory.

---

## 2. Moving Total-Pressure Slice

A second automated workflow was developed to visualize the total-pressure field using a moving cross-sectional slice.

Total pressure was calculated as:

**p_total = p + 0.5 ρ |U|²**

using a seawater density of:

**ρ = 1025 kg/m³**

### Visualization Settings

- Total-pressure display range: **70–140 kPa**
- Slice normal: **[0, 1, 0]**
- Slice plane: **X-Z**
- Start position: **Y = +0.3 m**
- End position: **Y = -1.5 m**
- Flow direction: **-Y**
- Camera direction: along the Y-axis

### Animation

`moving_total_pressure_slice.mp4`

The slice position changes while the CFD solution time also advances. Therefore, the animation contains both spatial and temporal variation.

It should be interpreted as an automated visualization and sampling sweep through the CFD domain rather than as a wake-tracking algorithm.

Representative frames from the moving-slice workflow are available in the [`images`](../images/) directory.

---

## Result Summary

The automated post-processing workflow demonstrates:

- systematic Q-criterion visualization;
- transient comparison using consistent visualization settings;
- automated blade-tip and hub/junction vortex visualization;
- total-pressure calculation from pressure and velocity fields;
- automated moving-slice visualization;
- consistent camera and colour-range control; and
- reproducible CFD post-processing using Python and ParaView.

The underlying OpenFOAM simulation is not included in this repository. This project focuses on post-processing, automation, and scientific visualization of the supplied CFD results.

For the complete methodology and selected figures, see the [main project README](../README.md).
