## CFD Visualization Results

The following results demonstrate the automated post-processing workflow developed for the existing OpenFOAM bow-thruster simulation. The visualizations focus on Q-criterion-based vortex identification and total-pressure field analysis.

### Q-Criterion Range Calibration

A systematic Q-range comparison was performed before selecting the final visualization settings. This avoided relying solely on ParaView's automatic colour rescaling and provided consistent ranges for subsequent visualizations.

![Q-Criterion Range Calibration](images/q_range_calibration.png)

### Blade-Tip Vortex Visualization

The blade-tip region was examined using the Q-criterion to identify rotation-dominated structures around the propeller-tip region.

The selected display range was:

**Q = 50–600**

![Blade-Tip Vortex Visualization](images/tip_vortex.png)

### Hub and Junction Vortex Visualization

The hub and junction region was examined separately to visualize rotation-dominated structures around the central region of the bow-thruster assembly.

The selected display range was:

**Q = 50–1200**

![Hub and Junction Vortex Visualization](images/hub_junction_vortex.png)

### Transient Vortex Evolution

For the transient analysis, the combined tip-and-hub visualization used a fixed display range of:

**Q = 50–1100**

A separate visualization-suppression threshold of:

**Q = 550**

was applied to suppress weaker structures in the final visualization.

The slice orientation, camera position, spatial-mask logic, and colour range were kept consistent between frames, enabling direct qualitative comparison of the transient vortex field.

![Transient Q-Criterion Evolution](images/transient_q_frames.png)

> **Important:** Q = 550 is a visualization-suppression threshold used for visual clarity. It should not be interpreted as a universal physical boundary between vortex and non-vortex flow or as a demonstrated numerical-noise threshold.

### Total-Pressure Field Analysis

Total pressure was calculated from the pressure and velocity fields using:

**p_total = p + 0.5 ρ |U|²**

with seawater density:

**ρ = 1025 kg/m³**

This provides a complementary view of the flow field alongside the Q-criterion vortex analysis.

![Total Pressure Field](images/total_pressure.png)

### Moving Total-Pressure Slice

A Y-normal X-Z slice was swept through the CFD domain from:

**Y = +0.3 m to Y = -1.5 m**

The moving slice was used to examine how the total-pressure distribution changes at different positions through the bow-thruster flow field.

![Moving Total-Pressure Slice Stages](images/moving_pressure_slices.png)

### Result Summary

The automated workflow provides a reproducible approach for:

- calibrating Q-criterion visualization ranges;
- examining blade-tip and hub/junction vortex structures;
- comparing transient vortex-field evolution using consistent visualization settings;
- calculating total pressure from OpenFOAM pressure and velocity fields; and
- examining total-pressure variation using an automated moving-slice workflow.

These results demonstrate the use of Python and ParaView for repeatable CFD post-processing and scientific visualization.
