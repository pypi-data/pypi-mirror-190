import io
import typing

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import networkx as nx


def show_clustermap(connectivity_matrix: np.ndarray,
                    k_clusters: typing.Sequence[int],
                    subplots: typing.Optional[typing.Tuple[int, int]] = None,
                    title: str = "Consensus clustering",
                    title_subplot: typing.Optional[typing.Sequence[str]] = None,
                    subplot_size: float = 5.):
    """
    Create and show the clustermap from the consensus clustering results.

    :param connectivity_matrix: calculated connectivity matrix
    :param k_clusters: list of investigated clusters
    :param subplots: a tuple with two positive ints for number of rows and columns of the Axes grid.
                     For instance, use (2,3) to show 5 clusters in 2 rows and 3 columns.
                     If absent, the subplots will be arranged in one row.
    :param title: title of plot
    :param title_subplot: list of titles of each seperate clustermap or None if no titles should be set
    :param subplot_size: approximate width and height for Axes to show a consensus matrix for given *k*
    :return: a tuple with figure and an array of figure Axes for each *k*
    """
    # Calculate figure size
    if subplots is None:
        subplots = (1, len(k_clusters))  # Put everything in one row
    elif len(subplots) != 2 or _is_not_positive_int(subplots[0] or _is_not_positive_int(subplots[1])):
        raise ValueError(f'Subplots must be a tuple with two positive ints: {subplots}')

    # Check subplot titles
    if title_subplot is not None and len(k_clusters) != len(title_subplot):
        raise ValueError(
            f'Number of subplot titles ({len(title_subplot)}) must be the same as the number of clusters ({len(k_clusters)})')

    # Check subplot size
    if subplot_size <= 0.:
        raise ValueError('Subplot size must be positive')

    figsize = (subplots[1] * subplot_size, subplots[0] * subplot_size)  # !
    fig, axs = plt.subplots(subplots[0], subplots[1], figsize=figsize, dpi=120)

    # Draw clusters
    axs = axs.flatten()
    for i in range(len(k_clusters)):
        g = sns.clustermap(connectivity_matrix[i, :, :], cmap='Blues', figsize=(5, 5), cbar_kws={"shrink": 0.1},
                           vmin=0., vmax=1.)
        plt.close()
        if title_subplot:
            g.ax_col_dendrogram.set_title(title_subplot[i], fontsize=14)

        g = g.fig
        g.tight_layout()

        with io.BytesIO() as buf:
            g.savefig(buf)
            buf.seek(0)
            axs[i].imshow(plt.imread(buf))

    for ax in axs:
        ax.axis('off')

    fig.suptitle(title)
    return fig, axs


def _is_not_positive_int(param) -> bool:
    return not (isinstance(param, int) and param > 0)


def show_important_features(sig_features: list, prevalence_sig_features: list,
                            hpo_graph: nx.DiGraph, max_plots_per_row: int = 4):
    """
    Create and show visualisation for the difference in features between clusters

    :param sig_features: list of the phenotypic features that are significantly different between clusters
    :param prevalence_sig_features: the corresponding contingency matrices of the listed features in sig_features
    :param hpo_graph: the HPO graph with labels
    :param max_plots_per_row: number of max subplots per row
    """
    k_clusters = prevalence_sig_features[0].shape[1]
    ratio_sig_features = np.zeros((len(prevalence_sig_features), k_clusters), dtype=int)
    hpo_labels = []
    for sig_feat in sig_features:
        hpo_labels.append(hpo_graph.nodes()[sig_feat.term_id.value]['label'])

    for i, arr in enumerate(prevalence_sig_features):
        # calculate prevalence as a ratio/percentage
        ratio_sig_features[i, :] = np.round(arr[0, :] / (arr[0, :]+arr[1, :]) * 100)

    num_rows = int(np.ceil(k_clusters / max_plots_per_row))
    if k_clusters <= max_plots_per_row:
        num_cols = k_clusters
    else:
        num_cols = max_plots_per_row

    sns.set_style("darkgrid")
    fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols)
    axs = axs.flatten()
    color_palette = sns.color_palette("Paired")
    for i, ax in enumerate(axs):
        sns.barplot(x=ratio_sig_features[:, i], y=hpo_labels, ax=ax, color=color_palette[i])
        if i % num_cols != 0:
            ax.set(yticklabels=[])
        ax.set_xlim([0, 100])
        ax.set_xticks([0, 50, 100])
        ax.set_xlabel('Prevalence (%)')
        ax.set_title('Cluster :' + str(i+1))
    [tick.label.set_fontsize(8) for tick in axs[0].yaxis.get_major_ticks()]
    plt.suptitle('Prevalence in HPO terms between clusters')
    plt.autoscale()
    plt.show()
    return
