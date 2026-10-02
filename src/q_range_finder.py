"""
Q-RANGE CALIBRATION SWEEP

Workflow:
OpenFOAM -> cylinder clip -> box clip -> Gradient(Q) -> X-normal slice
-> tip/hub spatial mask -> Q-range screenshot sweep.

Confirmed final selected ranges:
tip  = 50-600
hub  = 50-1200
both = 50-1100
"""

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
import os

TASK = "both"  # "tip", "hub", or "both"
CASE_PATH = "/path/to/your/openfoam/case/result.foam"
OUTPUT_DIR = "./output/q_range_calibration/"

# Report-confirmed Q_MIN candidates.
Q_MIN_LIST = [0, 50, 100, 150, 200]

# Exact original Q_MAX sweep list: Not confirmed from the uploaded files.
# These are reconstructed candidate values around the documented final ranges.
Q_MAX_LIST = {
    "tip":  [400, 500, 600, 700, 800],
    "hub":  [800, 1000, 1200, 1400, 1600],
    "both": [700, 900, 1100, 1300, 1500],
}

ALL_PATCHES = [
    "patch/blatt1", "patch/blatt2", "patch/blatt3", "patch/blatt4",
    "patch/nabe", "patch/getriebe", "patch/propellermutter"
]

TASK_SETTINGS = {
    "tip":  (0.00, -0.2, 0.17,
             ["patch/blatt1", "patch/blatt2", "patch/blatt3", "patch/blatt4"]),
    "hub":  (0.18, -0.2, 0.50,
             ["patch/nabe", "patch/getriebe", "patch/propellermutter"]),
    "both": (0.15, -0.2, 0.22, ALL_PATCHES),
}
if TASK not in TASK_SETTINGS:
    raise ValueError("TASK must be 'tip', 'hub', or 'both'.")

HUB_Z, HUB_Y_UPPER, TIP_Z, ACTIVE_PATCHES = TASK_SETTINGS[TASK]
os.makedirs(OUTPUT_DIR, exist_ok=True)

reader = OpenFOAMReader(FileName=CASE_PATH)
reader.CellArrays = ["Q", "U", "p", "vorticity"]
reader.MeshRegions = ["internalMesh"] + ALL_PATCHES

scene = GetAnimationScene()
scene.UpdateAnimationUsingDataTimeSteps()
times = list(reader.TimestepValues)
if not times:
    raise RuntimeError("No CFD time steps found.")
t = times[0]
scene.AnimationTime = t
UpdatePipeline(t, reader)

view = GetActiveViewOrCreate("RenderView")

reader.MeshRegions = ACTIVE_PATCHES
geo = Show(reader, view, "GeometryRepresentation")
geo.Representation = "Surface"
geo.ColorArrayName = ["POINTS", ""]
reader.MeshRegions = ["internalMesh"] + ALL_PATCHES

clip1 = Clip(Input=reader)
clip1.ClipType = "Cylinder"
clip1.ClipType.Center = [0.0, 0.0, 0.0]
clip1.ClipType.Axis = [0.0, 1.0, 0.0]
clip1.ClipType.Radius = 0.38
clip1.Invert = 1

clip2 = Clip(Input=clip1)
clip2.ClipType = "Box"
clip2.ClipType.Position = [-0.38, -1.0, -0.38]
clip2.ClipType.Length = [0.76, 1.4, 0.76]
clip2.Invert = 1

gradient = Gradient(Input=clip2)
gradient.ScalarArray = ["POINTS", "U"]
gradient.ComputeQCriterion = 1

slc = Slice(Input=gradient)
slc.SliceType = "Plane"
slc.SliceType.Origin = [0.0, 0.0, 0.0]
slc.SliceType.Normal = [1.0, 0.0, 0.0]

mask = ProgrammableFilter(Input=slc)
mask.Script = f"""
import numpy as np
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from vtk.util import numpy_support

wrapped = dsa.WrapDataObject(inputs[0])
Z = wrapped.Points[:, 2]
Y = wrapped.Points[:, 1]

hub_band = (np.abs(Z) < {HUB_Z}) & (Y < {HUB_Y_UPPER})
tip_band = (np.abs(Z) > {TIP_Z})
keep_mask = hub_band | tip_band

q = wrapped.PointData['Q Criterion']
q_masked = np.where(keep_mask, q, 0.0)
vtk_array = numpy_support.numpy_to_vtk(q_masked)
vtk_array.SetName('Q Criterion')

output.ShallowCopy(inputs[0].VTKObject)
output.GetPointData().RemoveArray('Q Criterion')
output.GetPointData().AddArray(vtk_array)
"""

display = Show(mask, view, "GeometryRepresentation")
display.Representation = "Surface"
ColorBy(display, ("POINTS", "Q Criterion"))
display.SetScalarBarVisibility(view, True)

view.CameraPosition = [5.0, 0.0, 0.0]
view.CameraFocalPoint = [0.0, 0.0, 0.0]
view.CameraViewUp = [0.0, 0.0, 1.0]
view.CameraParallelScale = 0.8
view.UseFXAA = 1

lut = GetColorTransferFunction("QCriterion")
lut.ApplyPreset("Rainbow Uniform", True)
lut.AutomaticRescaleRangeMode = "Never"
display.LookupTable = lut
pwf = GetOpacityTransferFunction("QCriterion")

for q_min in Q_MIN_LIST:
    for q_max in Q_MAX_LIST[TASK]:
        if q_max <= q_min:
            continue
        lut.RescaleTransferFunction(q_min, q_max)
        pwf.RescaleTransferFunction(q_min, q_max)
        Render()
        filename = f"{TASK}_Qmin{q_min}_Qmax{q_max}_t{t:.4f}.png"
        SaveScreenshot(os.path.join(OUTPUT_DIR, filename), view,
                       ImageResolution=[1920, 1080])
        print("Saved:", filename)

print("Calibration sweep complete.")
