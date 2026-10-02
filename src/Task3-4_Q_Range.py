"""
TASK 3 & 4 — FINAL SINGLE-TIME-STEP Q-CRITERION RENDER
========================================================
Purpose: produce ONE clean, final render per task configuration
('tip', 'hub', or 'both'), using the fixed Q-criterion display
range already selected by the calibration sweep
(Task3-4_range_finder.py):

    tip  -> 50-600
    hub  -> 50-1200
    both -> 50-1100

This script does NOT loop over Q_MIN_LIST / Q_MAX_LIST. It is the
"final render" step that Task3-4_range_finder.py's own header
comment refers to, filling the gap noted in the project report's
issues section (no such single-range script existed among the
original project files).

Clip geometry: this script uses the two-stage Cylinder-then-Box
clip (radius 0.38 m about the tunnel's Y-axis, then a box trim),
matching Task3-4_range_finder.py and the transient pipeline
(tip_hub_pipeline_final.py), rather than the single-box clip used
in the original Task3-4.py sweep script. This keeps the clip
geometry consistent across the single-time-step and transient
Q-criterion pipelines. If the calibration images were in fact
produced with the single-box clip instead, switch CLIP_MODE below
to 'box'.
"""

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
import os

# ════════════════════════════════════════════════════════
# CHANGE THESE SETTINGS AS NEEDED
# ════════════════════════════════════════════════════════

TASK = 'tip'   # 'tip', 'hub', 'both'

CASE_PATH  = 'path/to/your/OpenFOAM/case/result.foam'
OUTPUT_DIR = 'output/'

# Clip geometry: 'cylinder' (cylinder+box, matches range_finder / transient
# pipeline) or 'box' (single box, matches the original Task3-4.py sweep script)
CLIP_MODE = 'cylinder'

BOX_POSITION = [-0.4, -1.5, -0.5]
BOX_LENGTH   = [0.8,   1.8,  1.0]

CYL_CENTER = [0.0, 0.0, 0.0]
CYL_AXIS   = [0.0, 1.0, 0.0]
CYL_RADIUS = 0.38
CYL_BOX_POSITION = [-0.38, -1.0, -0.38]
CYL_BOX_LENGTH   = [0.76,  1.4,  0.76]

# Calibrated Q-criterion display ranges (from Task3-4_range_finder.py)
Q_RANGES = {
    'tip':  (50, 600),
    'hub':  (50, 1200),
    'both': (50, 1100),
}

# ════════════════════════════════════════════════════════

ALL_PATCHES = [
    'patch/blatt1', 'patch/blatt2',
    'patch/blatt3', 'patch/blatt4',
    'patch/nabe',   'patch/getriebe',
    'patch/propellermutter'
]

# ── Task settings ────────────────────────────────────────
if TASK == 'tip':
    HUB_Z          = 0.00
    HUB_Y_UPPER    = -0.2
    TIP_Z          = 0.17
    ACTIVE_PATCHES = [
        'patch/blatt1', 'patch/blatt2',
        'patch/blatt3', 'patch/blatt4'
    ]
    TASK_LABEL = 'tip_vortex'
    print("Task: TIP VORTEX")

elif TASK == 'hub':
    HUB_Z          = 0.18
    HUB_Y_UPPER    = -0.2
    TIP_Z          = 0.5
    ACTIVE_PATCHES = [
        'patch/nabe', 'patch/getriebe',
        'patch/propellermutter'
    ]
    TASK_LABEL = 'hub_vortex'
    print("Task: HUB VORTEX")

elif TASK == 'both':
    HUB_Z          = 0.15
    HUB_Y_UPPER    = -0.2
    TIP_Z          = 0.22
    ACTIVE_PATCHES = ALL_PATCHES
    TASK_LABEL     = 'both_vortex'
    print("Task: BOTH")

else:
    raise ValueError(f"Unknown TASK '{TASK}'. Use 'tip', 'hub', or 'both'.")

Q_MIN, Q_MAX = Q_RANGES[TASK]
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load case ────────────────────────────────────────────
print("\nLoading case...")
resultfoam = OpenFOAMReader(FileName=CASE_PATH)
resultfoam.CellArrays = ['Q', 'U', 'p', 'vorticity']

animationScene1 = GetAnimationScene()
animationScene1.UpdateAnimationUsingDataTimeSteps()
available_times = resultfoam.TimestepValues
print(f"Available time steps: {available_times}")

t = available_times[0]
print(f"Using first time step: {t}")
animationScene1.AnimationTime = t

renderView1 = GetActiveViewOrCreate('RenderView')

# ── Load mesh regions ─────────────────────────────────────
resultfoam.MeshRegions = ['internalMesh'] + ALL_PATCHES
UpdatePipeline(t, resultfoam)

# ── Show patch geometry ───────────────────────────────────
resultfoam.MeshRegions = ACTIVE_PATCHES
d = Show(resultfoam, renderView1, 'GeometryRepresentation')
d.Representation = 'Surface'
d.ColorArrayName = ['POINTS', '']
resultfoam.MeshRegions = ['internalMesh'] + ALL_PATCHES
Hide(resultfoam, renderView1)

# ── Clip ────────────────────────────────────────────────
if CLIP_MODE == 'cylinder':
    print("\nApplying cylinder clip...")
    clip1 = Clip(Input=resultfoam)
    clip1.ClipType = 'Cylinder'
    clip1.ClipType.Center = CYL_CENTER
    clip1.ClipType.Axis   = CYL_AXIS
    clip1.ClipType.Radius = CYL_RADIUS
    clip1.Invert = 1

    print("Applying box clip...")
    clip_final = Clip(Input=clip1)
    clip_final.ClipType = 'Box'
    clip_final.ClipType.Position = CYL_BOX_POSITION
    clip_final.ClipType.Length   = CYL_BOX_LENGTH
    clip_final.Invert = 1
    print("Clip(s) applied!")
else:
    print("\nApplying box clip...")
    clip_final = Clip(Input=resultfoam)
    clip_final.ClipType          = 'Box'
    clip_final.ClipType.Position = BOX_POSITION
    clip_final.ClipType.Length   = BOX_LENGTH
    clip_final.Invert            = 1
    print("Box clip applied!")

# ── Compute Q-criterion on clipped domain ─────────────────
print("Computing Q-criterion...")
gradient1 = Gradient(Input=clip_final)
gradient1.ScalarArray       = ['POINTS', 'U']
gradient1.ComputeQCriterion = 1
q_source = gradient1
print("Q-criterion computed!")

# ── Slice — X-normal cross section ───────────────────────
slc = Slice(Input=q_source)
slc.SliceType        = 'Plane'
slc.SliceType.Origin = [0.0, 0.0, 0.0]
slc.SliceType.Normal = [1.0, 0.0, 0.0]

# ── Programmable filter — spatial mask ───────────────────
mask = ProgrammableFilter(Input=slc)
mask.Script = f"""
import numpy as np
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from vtk.util import numpy_support

data    = inputs[0]
wrapped = dsa.WrapDataObject(data)

Z = wrapped.Points[:, 2]
Y = wrapped.Points[:, 1]

HUB_Z       = {HUB_Z}
HUB_Y_UPPER = {HUB_Y_UPPER}
TIP_Z       = {TIP_Z}

hub_band  = (np.abs(Z) < HUB_Z) & (Y < HUB_Y_UPPER)
tip_band  = (np.abs(Z) > TIP_Z)
keep_mask = hub_band | tip_band

q_array  = wrapped.PointData['Q Criterion']
q_masked = np.where(keep_mask, q_array, 0.0)

vtk_array = numpy_support.numpy_to_vtk(q_masked)
vtk_array.SetName('Q Criterion')

output.ShallowCopy(inputs[0].VTKObject)
output.GetPointData().RemoveArray('Q Criterion')
output.GetPointData().AddArray(vtk_array)
"""
mask.RequestInformationScript  = ''
mask.RequestUpdateExtentScript = ''

# ── Display + fixed color range (calibrated, set once) ───
sd = Show(mask, renderView1, 'GeometryRepresentation')
sd.Representation = 'Surface'

lut = GetColorTransferFunction('QCriterion')
lut.ApplyPreset('Rainbow Uniform', True)
lut.AutomaticRescaleRangeMode = 'Never'
lut.RescaleTransferFunction(Q_MIN, Q_MAX)

pwf = GetOpacityTransferFunction('QCriterion')
pwf.RescaleTransferFunction(Q_MIN, Q_MAX)

ColorBy(sd, ('POINTS', 'Q Criterion'))
sd.LookupTable = lut
sd.SetScalarBarVisibility(renderView1, True)

Hide(resultfoam, renderView1)
renderView1.UseFXAA = 1

# ── Fixed camera ──────────────────────────────────────────
renderView1.CameraPosition      = [5.0, 0.0, 0.0]
renderView1.CameraFocalPoint    = [0.0, 0.0, 0.0]
renderView1.CameraViewUp        = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.8

Render()

# ── Save the single, final render for this task ──────────
out = os.path.join(OUTPUT_DIR, f"{TASK_LABEL}_final_t{t:.4f}_Q{Q_MIN}-{Q_MAX}.png")
SaveScreenshot(out, renderView1, ImageResolution=[1920, 1080])

print("\nDone.")
print(f"Task: {TASK}  |  Q range used: [{Q_MIN}, {Q_MAX}]  |  Clip mode: {CLIP_MODE}")
print(f"Saved: {out}")
