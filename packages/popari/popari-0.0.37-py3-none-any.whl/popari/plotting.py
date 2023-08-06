from typing import Optional, Sequence
from functools import partial

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap

import numpy as np
import scanpy as sc

from popari.model import Popari
from popari._dataset_utils import _preprocess_embeddings, _plot_metagene_embedding, _cluster, _pca, _plot_in_situ, \
                                  _plot_umap, _multireplicate_heatmap, _multigroup_heatmap, _compute_empirical_correlations, \
                                  _broadcast_operator, _compute_ari_score, _compute_silhouette_score, _plot_all_metagenes, \
                                  _evaluate_classification_task, _compute_confusion_matrix, _compute_columnwise_autocorrelation, \
                                  _plot_confusion_matrix, _compute_spatial_correlation

def confusion_matrix(trained_model: Popari, labels: str, confusion_matrix_key: str = "confusion_matrix"):
    datasets = trained_model.datasets

    _broadcast_operator(datasets, partial(_plot_confusion_matrix, labels=labels, confusion_matrix_key=confusion_matrix_key))

def multigroup_heatmap(trained_model: Popari,
    title_font_size: Optional[int] = None,
    group_type: str = "metagene",
    axes: Optional[Sequence[Axes]] = None,
    key: Optional[str] = None,
    **heatmap_kwargs
  ):
    r"""Plot 2D heatmap data across all datasets.

    Wrapper function to enable plotting of continuous 2D data across multiple replicates. Only
    one of ``obsm``, ``obsp`` or ``uns`` should be used.

    Args:
        trained_model: the trained Popari model.
        axes: A predefined set of matplotlib axes to plot on.
        obsm: the key in the ``.obsm`` dataframe to plot.
        obsp: the key in the ``.obsp`` dataframe to plot.
        uns: the key in the ``.uns`` dataframe to plot. Unstructured data must be 2D in shape.
        **heatmap_kwargs: arguments to pass to the `ax.imshow` call for each dataset
    """
    datasets = trained_model.datasets
    groups = trained_model.metagene_groups if group_type == "metagene" else trained_model.spatial_affinity_groups
    _multigroup_heatmap(datasets, title_font_size=title_font_size, groups=groups, axes=axes, key=key, **heatmap_kwargs)

def umap(trained_model: Popari, color="leiden", axes = None, **kwargs):
    r"""Plot a categorical label across all datasets in-situ.

    Extends AnnData's ``sc.pl.spatial`` function to plot labels/values across multiple replicates.

    Args:
        trained_model: the trained Popari model.
        color: the key in the ``.obs`` dataframe to plot.
        axes: A predefined set of matplotlib axes to plot on.
    """
    datasets = trained_model.datasets

    _plot_umap(datasets, color=color, axes=axes, **kwargs)

def multireplicate_heatmap(trained_model: Popari,
    title_font_size: Optional[int] = None,
    axes: Optional[Sequence[Axes]] = None,
    obsm: Optional[str] = None,
    obsp: Optional[str] = None,
    uns: Optional[str] = None,
    nested: bool = True,
    **heatmap_kwargs
  ):
    r"""Plot 2D heatmap data across all datasets.

    Wrapper function to enable plotting of continuous 2D data across multiple replicates. Only
    one of ``obsm``, ``obsp`` or ``uns`` should be used.

    Args:
        trained_model: the trained Popari model.
        axes: A predefined set of matplotlib axes to plot on.
        obsm: the key in the ``.obsm`` dataframe to plot.
        obsp: the key in the ``.obsp`` dataframe to plot.
        uns: the key in the ``.uns`` dataframe to plot. Unstructured data must be 2D in shape.
        **heatmap_kwargs: arguments to pass to the `ax.imshow` call for each dataset
    """
    datasets = trained_model.datasets
    
    _multireplicate_heatmap(datasets, title_font_size=title_font_size, axes=axes,
                            obsm=obsm, obsp=obsp, uns=uns, nested=nested, **heatmap_kwargs)
