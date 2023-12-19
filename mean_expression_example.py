from pathlib import Path
import tifffile as tff
from ome_types import from_tiff
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops

# The location of the cytokit sprm pipeline outputs (from globus)
pipeline_output_location = Path("/data/cytokit_sprm_pipeline_outputs")
celltype_prediction_location = Path.home() / "outputs"
dataset = "HBM233.GTZN.466-b38730b2633e0b088619f9bcd514ba13"

mask_fname = pipeline_output_location / dataset / "ometiff-pyramids/pipeline_output/mask/reg001_mask.ome.tif"
mask_metadata = from_tiff(mask_fname)
#mask_metadata.images[0].pixels.channels

# Load the cytokit masks from pipeline outputs
masks = tff.imread(mask_fname)
mask = masks[0]


predictions_fname = celltype_prediction_location / dataset / "deepcelltypes_predictions.csv"

# Load predictions
pred_dtype = np.dtype([("idx", int), ("x", float), ("y", float), ("celltype", "<U18")])
predictions = np.loadtxt(predictions_fname, delimiter=",", dtype=pred_dtype)

# Extract individual cells from mask
props = regionprops(mask)
assert len(props) == mask.max()


img_fname = pipeline_output_location / dataset / "ometiff-pyramids/pipeline_output/expr/reg001_expr.ome.tif"
img = tff.imread(img_fname)
img_metadata = from_tiff(img_fname)
data_chnames = [ch.name for ch in img_metadata.images[0].pixels.channels]

# Comptue mean channel expressions for each cell
mean_channel_expressions = np.array([
    img[..., p.slice[0], p.slice[1]][..., p.image].sum(axis=1) / p.area
    for p in props
])

celltypes = predictions["celltype"]
#np.unique(celltypes, return_counts=True)

# Example: extracting mean_channel_expressions for a single cell type
bcell_expressions = mean_channel_expressions[celltypes == "BCELL"]

# Take the mean channel expression by cell type, for all cell types
mean_channel_expressions_by_celltype = np.array([
    mean_channel_expressions[celltypes == ct].mean(axis=0)
    for ct in sorted(np.unique(celltypes))
])

# Visualize
fig, ax = plt.subplots(figsize=(12, 3))
ax.imshow(mean_channel_expressions_by_celltype);
ax.set_xticks(
    np.arange(mean_channel_expressions_by_celltype.shape[-1]),
    data_chnames,
);
ax.set_yticks(
    np.arange(mean_channel_expressions_by_celltype.shape[0]),
    sorted(np.unique(celltypes)),
);
fig.autofmt_xdate()
fig.tight_layout()
plt.show()
