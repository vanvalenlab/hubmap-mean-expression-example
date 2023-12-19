# Example: Mean marker expression by cell type

This repo contains a minimal example demonstrating how to compute a simple
metric (in this case, mean marker expression) by cell type using the
published results from the CODEX cytokit+sprm pipeline from the HubMAP
data portal.

The analysis requires three inputs:

1. The multiplexed image from the CODEX Cytokit+SPRM pipeline (from globus)
2. The corresponding mask produced by the CODEX Cytokit+SPRM pipeline (also from globus)
3. The cell type predictions

The celltype predictions are not currently publicly available as the model is still
under development.
However, a module has been provided which integrates with the Cytokit+SPRM pipeline
to directly produce celltype predictions. This is availble to consortium members
at <https://github.com/hubmapconsortium/deepcelltypes-hubmap>.

The CWL workflow referenced above adds one more output to the CODEX Cytokit+SPRM
pipeline: a .csv file called `deepcelltypes_predictions.csv` containing the cell type
predictions with the following structure:

```
mask_index,centroid_x,centroid_y,predicted_celltype
```

## Running

First, create a virtual envrionment and install the dependencies with
`pip install -r requirements.txt`

Next, make sure you have all of the necessary CODEX Cytokit+SPRM data
downloaded from globus for the dataset you are working with.

Finally, make sure you have the celltype predictions. These are computed either
by running the Cytokit+SPRM pipeline with the additional prediction CWL
workflow referenced above, or by unpacking the predictions that I've shared
with consortium members from the preliminary model development.

Modify the `pipeline_output_location`, `celltype_prediction_location`,
and `dataset` values in `mean_expression_example.py` to match the locations
on your system.

Then:

```bash
python mean_expression_example.py
```
