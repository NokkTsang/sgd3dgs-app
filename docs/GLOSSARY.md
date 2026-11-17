# Gaussian Splatting glossary

## Representation and rendering

**3D Gaussian / splat** — An anisotropic volumetric primitive with position,
orientation, scale/covariance, opacity, and appearance coefficients.

**Mean (`μ`)** — The 3D centre of a Gaussian.

**Covariance (`Σ`)** — The ellipsoid's size and orientation. Implementations
often parameterize it using scale and a quaternion rather than storing a full
matrix.

**Opacity / alpha** — Contribution strength during compositing. Many overlapping
Gaussians blend into each pixel.

**Spherical harmonics (SH)** — Coefficients representing view-dependent colour.
They are one reason rotating a captured object is more complicated than moving a
plain RGB point cloud.

**Rasterizer** — GPU code that projects, sorts, and blends Gaussians into pixels.

**Densification / pruning** — Training operations that add useful Gaussians and
remove low-value ones.

## Cameras and reconstruction

**COLMAP** — A common structure-from-motion system producing calibrated cameras,
poses, and a sparse point cloud from images.

**Extrinsics** — Camera pose relative to the scene.

**Intrinsics** — Camera focal length, principal point, and lens model.

**Novel view** — A viewpoint not directly present in the training images.

## Segmentation

**2D mask** — A per-pixel foreground/background or instance label in one image.

**Lifting** — Combining calibrated 2D evidence into labels on 3D Gaussians.

**Object identity encoding** — A learned feature attached to each Gaussian that
encourages Gaussians belonging to the same object to group together.

**Promptable segmentation** — Segmentation controlled by clicks, boxes, text, or
masks, such as SAM-family models.

**Label leakage** — Background or another object is incorrectly assigned to a
selected object and moves with it.

**Under-segmentation** — Part of the object is left behind.

**Over-segmentation** — Multiple IDs represent parts of one logical object.

## Editing and completion

**SE(3) / rigid transform** — Rotation and translation that preserve shape.

**Pivot** — Point around which an object rotates. A bad pivot makes interaction
feel unnatural even when the transform mathematics is correct.

**OBB** — Oriented bounding box, usually more useful than an axis-aligned box for
object dimensions and pivots.

**Disocclusion** — Background exposed when a foreground object moves away.

**Inpainting** — Filling a missing image or scene region using surrounding
evidence and possibly a generative prior.

**Object completion** — Generating unseen geometry/appearance for an incomplete
object, such as its back or underside.

**Baked lighting** — Shadows, highlights, and reflections captured in appearance
rather than represented as editable physical lighting.

## Project terms

**Source scene** — Immutable Gaussian scene to which labels and edits refer.

**Scene manifest** — Small JSON document binding source, labels, coordinate
system, objects, and provenance.

**Vertical slice** — The thinnest complete path through the system, currently
scene → labels → selection → movement → undo.

**Golden fixture** — Small stable input/output used to detect regressions.

**Spike** — Time-boxed investigation intended to answer a question, not become
production code automatically.
