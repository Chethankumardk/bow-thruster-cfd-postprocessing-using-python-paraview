## CFD Visualization Results

### Q-Criterion Range Calibration

A systematic Q-range comparison was performed before selecting the final visualization settings. This avoided relying only on ParaView's automatic colour rescaling.

![Q-Criterion Range Calibration](images/q_range_calibration.png)

### Blade-Tip Vortex Visualization

The blade-tip region was examined using Q-criterion to identify rotation-dominated structures associated with the propeller tip region.

The selected display range for this visualization was:

**Q = 50–600**

![Blade-Tip Vortex](images/tip_vortex.png)

### Hub and Junction Vortex Visualization

The hub and junction region was examined separately to visualize rotation-dominated structures around the central region of the bow-thruster assembly.

The selected display range was:

**Q = 50–1200**

![Hub and Junction Vortex](images/hub_junction_vortex.png)

### Transient Vortex Evolution

The final transient workflow used a fixed Q display range of:

**Q = 50–1100**

together with a visualization-suppression threshold of:

**Q = 550**

The same slice orientation, camera configuration, spatial-mask logic and colour range were retained between frames to support consistent qualitative comparison.

![Transient Q-Criterion Evolution](images/transient_q_frames.png)

> **Note:** Q = 550 is used as a visualization-suppression threshold. It should not be interpreted as a universal physical vortex boundary or a demonstrated numerical-noise threshold.

### Total-Pressure Field

Total pressure was calculated as:

**p_total = p + 0.5 ρ |U|²**

using seawater density:

**ρ = 1025 kg/m³**

![Total Pressure Field](images/total_pressure.png)

### Moving Total-Pressure Slice

A Y-normal X-Z slice was moved through the CFD domain from:

**Y = +0.3 m to Y = -1.5 m**

to visualize how the total-pressure distribution changes with slice position.

![Moving Total-Pressure Slices](images/moving_pressure_slices.png)
