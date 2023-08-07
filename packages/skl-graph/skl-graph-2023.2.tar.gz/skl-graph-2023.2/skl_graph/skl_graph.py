# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
Base Skeleton Graph.

Simple example usage:
>>> import matplotlib.pyplot as pyplot
>>> import numpy
>>> import skimage.data as data
>>> import skimage.util as util
>>> object_map = util.invert(data.horse())
>>> # --- SKL Map
>>> from skl_graph.skl_map import SKLMapFromObjectMap
>>> skl_map = SKLMapFromObjectMap(object_map)
>>> # --- SKL Graph
>>> from skl_graph.skl_graph import skl_graph_t
>>> skl_graph = skl_graph_t.FromSKLMap(skl_map)
>>> # --- End of SKLGraph-based sections
>>> _, axes = pyplot.subplots(ncols=3)
>>> axes[0].matshow(object_map, cmap="gray")
>>> axes[1].matshow(skl_map, cmap="gray")
>>> skl_graph.Plot(axes=axes[2], should_block=False)
>>> for ax, title in zip(axes, ("Object", "Skeleton", "Graph")):
>>>     ax.set_title(title)
>>>     ax.set_axis_off()
>>> pyplot.tight_layout()
>>> pyplot.show()
"""

from __future__ import annotations

from typing import Callable, ClassVar, Dict, List, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as pl_
import networkx as nx_
import numpy as np_
import scipy.ndimage as im_
import skimage.draw as dw_
from mpl_toolkits import mplot3d as m3_

import skl_graph.brick.edge as dg_
import skl_graph.brick.node as nd_
import skl_graph.brick.topology_map as bymp
from skl_graph.brick.constants import UNTESTED_VALIDITY
from skl_graph.brick.plot import (
    axes_t,
    direction_style_t,
    direction_style_unstructured_h,
    edge_style_unstructured_h,
    edge_styles_h,
    edge_styles_unstructured_h,
    figure_t,
    label_style_t,
    label_style_unstructured_h,
    label_styles_h,
    label_styles_unstructured_h,
    node_style_unstructured_h,
    node_styles_h,
    node_styles_unstructured_h,
    plot_mode_e,
    plot_style_t,
)


array_t = np_.ndarray


class skl_graph_t(nx_.MultiGraph):
    """
    s_node: Singleton node
    e_node: End node
    b_node: Branch node
    """

    __slots__ = (
        "dim",
        "domain_lengths",
        "n_components",
        "n_s_nodes",
        "n_e_nodes",
        "n_b_nodes",
        "has_widths",
        "invalidities",
        "node_styles",
        "edge_styles",
        "direction_style",
        "label_styles",
    )

    # TODO: use styles instead
    # TODO: use styles in all functions, not just plotexplicity (partially done for networkx)
    colormap: ClassVar[Dict[int, str]] = {0: "b", 1: "r", 2: "g"}

    dim: int
    domain_lengths: Tuple[int, ...]
    n_components: int
    n_s_nodes: int
    n_e_nodes: int
    n_b_nodes: int
    has_widths: bool
    invalidities: List[str]  # Use brick.constants.UNTESTED_VALIDITY as initial value
    node_styles: node_styles_h  # One style per degree + one default style
    edge_styles: edge_styles_h  # One style for "regular" edges, one for self-loops
    direction_style: direction_style_t
    label_styles: label_styles_h  # For nodes and edges, in that order

    def __init__(self):
        #
        super().__init__()
        for slot in self.__class__.__slots__:
            setattr(self, slot, None)
        self.invalidities = UNTESTED_VALIDITY

    @classmethod
    def FromSKLMap(cls, skl_map: array_t, width_map: array_t = None) -> skl_graph_t:
        """

        Parameters
        ----------
        skl_map : numpy.ndarray
        width_map : numpy.ndarray, optional

        Returns
        -------
        skl_graph_t
            Graph of the skeleton as an extended networkx.MultiGraph instance
        """
        instance = cls()

        instance.domain_lengths = skl_map.shape
        instance.dim = instance.domain_lengths.__len__()
        instance.has_widths = width_map is not None
        instance.n_s_nodes = 0
        instance.n_e_nodes = 0
        instance.n_b_nodes = 0

        tmap, background_label = bymp.TopologyMapOfMap(skl_map, return_bg_label=True)
        cc_map, n_components = bymp.LABELING_FCT_FOR_DIM[skl_map.ndim](skl_map)

        instance.n_components = n_components

        # Process skl_map/tmap per connected component (*)
        for cmp_label in range(1, n_components + 1):
            if n_components > 1:
                cmp_map = cc_map == cmp_label
                single_tmap = np_.full_like(tmap, background_label)
                single_tmap[cmp_map] = tmap[cmp_map]
            else:
                cmp_map = skl_map
                single_tmap = tmap

            if instance._DealsWithSpecialCases(
                single_tmap, background_label, width_map=width_map
            ):
                pass
            else:
                e_nodes, e_node_lmap = nd_.EndNodes(single_tmap, width_map=width_map)
                b_nodes, b_node_lmap = nd_.BranchNodes(single_tmap, width_map=width_map)
                raw_edges, edge_lmap = dg_.RawEdges(cmp_map, b_node_lmap)
                edges, node_uids_per_edge = dg_.EdgesFromRawEdges(
                    raw_edges,
                    e_nodes,
                    b_nodes,
                    edge_lmap,
                    e_node_lmap,
                    b_node_lmap,
                    width_map=width_map,
                )

                instance.add_nodes_from(
                    (node.uid, dict(as_node_t=node)) for node in e_nodes
                )
                instance.add_nodes_from(
                    (node.uid, dict(as_node_t=node)) for node in b_nodes
                )
                for edge, adjacent_node_uids in zip(edges, node_uids_per_edge):
                    instance._AddEdge(edge, adjacent_node_uids)

                instance.n_e_nodes += e_nodes.__len__()
                instance.n_b_nodes += b_nodes.__len__()

        instance.node_styles = {
            None: plot_style_t(type=".", size=6, color="g"),
            1: plot_style_t(type=".", size=6, color="r"),
        }
        instance.edge_styles = (
            plot_style_t(type="-", size=2, color="k"),
            plot_style_t(type=":", size=2, color="k"),
        )
        instance.direction_style = direction_style_t(show=False, size=0, color="k")
        instance.label_styles = (
            label_style_t(show=True, size=6.0, color="k"),
            label_style_t(show=False, size=6.0, color="k"),
        )

        return instance

    def _DealsWithSpecialCases(
        self, tmap: array_t, background_label: int, width_map: array_t = None
    ) -> bool:
        """Creates and adds nodes and edges of cases such as a singleton node, self loops...

        Parameters
        ----------
        tmap : numpy.ndarray
            Topological map of the skeleton; Must contain a unique connected component.
        background_label
        width_map

        Returns
        -------

        """
        singleton = np_.where(tmap == 0)
        if singleton[0].size > 0:
            # Can only be 1 since tmap is processed per connected components (*)
            singleton = np_.array(singleton, dtype=np_.int64).squeeze()
            end_node = nd_.end_node_t.WithPosition(singleton, width_map=width_map)
            self.add_node(end_node.uid, as_node_t=end_node)

            self.n_s_nodes += 1

            return True
        #
        elif (tmap[tmap != background_label] == 2).all():
            # The tmap represents a self loop
            loop_slc = np_.nonzero(tmap == 2)

            # Takes the first pixel to serve as a node, and the rest for the self-loop edge
            #
            # 0:1 makes sites elements array_t's (instead of numpy numbers), which is necessary for
            # nd_.branch_node_t.WithCentroidAndSites, but requires to squeeze the centroid.
            sites = tuple(per_dim[0:1] for per_dim in loop_slc)
            centroid = np_.array(sites, dtype=np_.float64).squeeze()
            node = nd_.branch_node_t.WithCentroidAndSites(
                centroid, sites=sites, width_map=width_map
            )
            self.add_node(node.uid, as_node_t=node)

            n_unique_sites = loop_slc[0].__len__()
            sites = tuple(
                per_dim[list(range(n_unique_sites)) + [0]] for per_dim in loop_slc
            )
            adjacent_node_uids = (node.uid, node.uid)
            edge = dg_.edge_t.NewWithDetails(
                # sites, adjacent_node_uids, node.uid, width_map=width_map
                sites,
                adjacent_node_uids,
                width_map=width_map,
            )
            self._AddEdge(edge, adjacent_node_uids)

            self.n_b_nodes += 1

            return True

        return False

    def _AddEdge(self, edge: dg_.edge_t, adjacent_node_uids: Sequence[str]) -> None:
        #
        edge_uid = edge.uid
        version_number = 1
        uid_w_vn = edge_uid
        while self.has_edge(*adjacent_node_uids, key=uid_w_vn):
            version_number += 1
            uid_w_vn = edge_uid + "+" + version_number.__str__()

        self.add_edge(*adjacent_node_uids, key=uid_w_vn, as_edge_t=edge)

    @property
    def n_nodes(self) -> int:
        return self.number_of_nodes()

    @property
    def n_edges(self) -> int:
        return self.number_of_edges()

    @property
    def is_valid(self) -> bool:
        """"""
        output = True
        self.invalidities = []

        n_components = nx_.number_connected_components(self)
        if n_components != self.n_components:
            output = False
            self.invalidities.append(
                f"Actual and stored number of connected components differ: "
                f"{n_components}!={self.n_components}"
            )
        n_s_nodes = sum(degree == 0 for _, degree in self.degree)
        if n_s_nodes != self.n_s_nodes:
            output = False
            self.invalidities.append(
                f"Actual and stored number of singleton nodes differ: "
                f"{n_s_nodes}!={self.n_s_nodes}"
            )
        n_e_nodes = sum(degree == 1 for _, degree in self.degree)
        if n_e_nodes != self.n_e_nodes:
            output = False
            self.invalidities.append(
                f"Actual and stored number of end nodes differ: "
                f"{n_e_nodes}!={self.n_e_nodes}"
            )
        n_b_nodes = sum(degree > 1 for _, degree in self.degree)
        if n_b_nodes != self.n_b_nodes:
            output = False
            self.invalidities.append(
                f"Actual and stored number of end nodes differ: "
                f"{n_b_nodes}!={self.n_b_nodes}"
            )

        nodes_are_valid = all(
            _node.is_valid for _, _node in self.nodes.data("as_node_t")
        )
        if not nodes_are_valid:
            output = False
            self.invalidities.append("Some nodes are invalid")

        some_edges_are_invalid = False
        for origin, destination, edge in self.edges.data("as_edge_t"):
            if not edge.is_probably_valid:
                output = False
                some_edges_are_invalid = True

            nodes = (self.nodes[_uid]["as_node_t"] for _uid in (origin, destination))
            if not edge.HasValidEndSites(*nodes):
                output = False
                some_edges_are_invalid = True
                edge.invalidities.append(f"Invalid sites end points")
        if some_edges_are_invalid:
            self.invalidities.append("Some edges are invalid")

        return output

    def ShowInvalidities(self) -> None:
        """"""
        if self.invalidities == UNTESTED_VALIDITY:
            _ = self.is_valid

        if self.invalidities.__len__() == 0:
            print(f"{self}\n---> Valid")
            return

        invalidities = "\n    ".join(self.invalidities)
        print(f"{self}\n---> Invalidities:\n    {invalidities}")

        for name, elements in zip(("node", "edge"), (self.nodes, self.edges)):
            print(f"    --- Invalid {name}s")
            for *_, element in elements.data(f"as_{name}_t"):
                # Since the graph has been checked, then element.invalidities != UNTESTED_VALIDITY
                if element.invalidities.__len__() > 0:
                    invalidities = "\n    ".join(element.invalidities)
                    print(f"    {element}\n    /!\\\n    {invalidities}")

    def Correctness(self, skl_map: array_t) -> Tuple[bool, bool]:
        """"""
        rebuilt_skl_map = self.RebuiltSkeletonMap()

        topological_map = bymp.TopologyMapOfMap(skl_map)
        # Keep next line before its next one
        topological_map[topological_map == bymp.TMapBackgroundLabel(skl_map)] = 0
        topological_map[topological_map > 3] = 3

        binary_correctness = np_.array_equal(rebuilt_skl_map > 0, skl_map)
        topology_correctness = np_.array_equal(rebuilt_skl_map, topological_map)

        return binary_correctness, topology_correctness

    def RebuiltSkeletonMap(self, with_width: bool = False) -> array_t:
        #
        if (not self.has_widths) and with_width:
            with_width = False
        if with_width:
            dtype = np_.float64
        else:
            # Not uint to allow for subtraction
            dtype = np_.int8

        output = np_.zeros(self.domain_lengths, dtype=dtype)

        for ___, ___, edge in self.edges.data("as_edge_t"):
            if with_width:
                output[edge.sites] = edge.widths
            else:
                output[edge.sites] = 2

        for ___, node in self.nodes.data("as_node_t"):
            if isinstance(node, nd_.branch_node_t):
                if with_width:
                    output[node.sites] = node.diameters
                else:
                    output[node.sites] = 3
            else:
                if with_width:
                    output[tuple(node.position)] = node.diameter
                else:
                    output[tuple(node.position)] = 1

        return output

    def RebuiltObjectMap(self) -> array_t:
        #
        if not self.has_widths:
            raise ValueError("Requires an SKL graph with widths")

        # Not uint to allow for subtraction
        output = np_.zeros(self.domain_lengths, dtype=np_.int8)

        if self.dim == 2:
            NewBall = dw_.disk
        else:
            NewBall = _Ball3D

        for ___, node in self.nodes.data("as_node_t"):
            if isinstance(node, nd_.branch_node_t):
                for *sites, radius in zip(
                    *node.sites,
                    np_.around(0.5 * (node.diameters - 1.0)).astype(np_.int64),
                ):
                    output[NewBall(sites, radius, shape=output.shape)] = 1
            else:
                output[
                    NewBall(
                        node.position,
                        np_.around(0.5 * (node.diameter - 1.0))
                        .astype(np_.int64)
                        .item(),
                        shape=output.shape,
                    )
                ] = 1

        for ___, ___, edge in self.edges.data("as_edge_t"):
            for *sites, radius in zip(
                *edge.sites, np_.around(0.5 * (edge.widths - 1.0)).astype(np_.int64)
            ):
                output[NewBall(sites, radius, shape=output.shape)] = 1

        return output

    def SetPlotStyles(
        self,
        /,
        *,
        node: Union[node_style_unstructured_h, node_styles_unstructured_h] = None,
        edge: edge_style_unstructured_h = None,
        regular_edge: edge_style_unstructured_h = None,
        self_loop: edge_style_unstructured_h = None,
        edges: edge_styles_unstructured_h = None,
        direction: direction_style_unstructured_h = None,
        label: label_style_unstructured_h = None,
        label_node: label_style_unstructured_h = None,
        label_edge: label_style_unstructured_h = None,
        labels: label_styles_unstructured_h = None,
    ) -> None:
        """
        edge: common style for both regulars and self-loops
        edges: styles for regulars and self-loops, in that order
        label: common style for both nodes and edges
        labels: styles for nodes and edges, in that order
        """
        if node is not None:
            if isinstance(node, tuple):  # node_style_unstructured_h
                self.node_styles = {
                    None: plot_style_t(type=node[0], size=node[1], color=node[2])
                }
            else:
                styles = {
                    _dgr: plot_style_t(type=_stl[0], size=_stl[1], color=_stl[2])
                    for _dgr, _stl in node.items()
                }
                self.node_styles.update(styles)
            if None not in self.node_styles:
                # Should never happen, but just in case...
                raise ValueError(
                    f"{self.node_styles}: Node styles without default style. "
                    f'Expected: style dictionary with a "None" entry.'
                )

        if edge is not None:
            style = plot_style_t(type=edge[0], size=edge[1], color=edge[2])
            styles = (style, style)
        elif regular_edge is not None:
            style = plot_style_t(
                type=regular_edge[0],
                size=regular_edge[1],
                color=regular_edge[2],
            )
            styles = (style, self.edge_styles[1])
        elif self_loop is not None:
            style = plot_style_t(
                type=self_loop[0],
                size=self_loop[1],
                color=self_loop[2],
            )
            styles = (self.edge_styles[0], style)
        elif edges is not None:
            styles = tuple(
                plot_style_t(
                    type=edges[_idx][0],
                    size=edges[_idx][1],
                    color=edges[_idx][2],
                )
                for _idx in range(2)
            )
        else:
            styles = None
        if styles is not None:
            self.edge_styles = styles

        if direction is not None:
            self.direction_style = direction_style_t(
                show=direction[0], size=direction[1], color=direction[2]
            )

        if label is not None:
            style = label_style_t(show=label[0], size=label[1], color=label[2])
            styles = (style, style)
        elif label_node is not None:
            style = label_style_t(
                show=label_node[0],
                size=label_node[1],
                color=label_node[2],
            )
            styles = (style, self.label_styles[1])
        elif label_edge is not None:
            style = label_style_t(
                show=label_edge[0],
                size=label_edge[1],
                color=label_edge[2],
            )
            styles = (self.label_styles[0], style)
        elif labels is not None:
            styles = tuple(
                label_style_t(
                    show=labels[_idx][0],
                    size=labels[_idx][1],
                    color=labels[_idx][2],
                )
                for _idx in range(2)
            )
        else:
            styles = None
        if styles is not None:
            self.label_styles = styles

    def Plot(
        self,
        figure: pl_.Figure = None,
        axes: pl_.axes.Axes = None,
        mode: plot_mode_e = plot_mode_e.SKL,
        max_distance: float = 1.0,
        colormap: Dict[int, str] = None,
        should_block: bool = True,
        should_return_figure: bool = False,
        should_return_axes: bool = False,
    ) -> Optional[Union[figure_t, axes_t, Tuple[figure_t, axes_t]]]:
        #
        if self.number_of_nodes() < 1:
            print(f"{__name__}.{self.Plot.__name__}: Empty graph")
            return None

        if axes is None:
            if figure is None:
                figure = pl_.figure()
            if self.dim == 2:
                axes = figure.gca()
            else:
                axes = figure.add_subplot(1, 1, 1, projection=m3_.Axes3D.name)
            axes.invert_yaxis()
        else:
            figure = axes.get_figure()

        if axes.yaxis_inverted():
            transformation = lambda y: y
            vector_transf = lambda y: y
        else:
            max_0 = self.domain_lengths[0] - 1
            transformation = lambda y: max_0 - np_.asarray(y)
            vector_transf = lambda y: -np_.asarray(y)

        transform_coords = lambda pos: (pos[1], transformation(pos[0]), *pos[2:])
        positions_as_dict = dict(
            (uid, transform_coords(node.position))
            for uid, node in self.nodes.data("as_node_t")
        )

        if self.dim == 2:
            if mode is plot_mode_e.Networkx:
                self._PlotWithNetworkX(positions_as_dict, axes, colormap)
            #
            elif mode in (
                plot_mode_e.SKL,
                plot_mode_e.SKL_Polyline,
                plot_mode_e.SKL_Curve,
            ):
                self._PlotExplicitly(
                    positions_as_dict,
                    transformation,
                    vector_transf,
                    axes,
                    mode,
                    max_distance,
                )
            #
            elif mode is plot_mode_e.Graphviz:
                self._PlotWithGraphviz(axes)
            #
            else:
                raise ValueError(f"{mode}: Invalid plotting mode")
            #
        else:
            self._PlotExplicitly(
                positions_as_dict,
                transformation,
                vector_transf,
                axes,
                mode,
                max_distance,
            )

        if self.dim == 2:
            # Matplotlib says: NotImplementedError: It is not currently possible to manually set the aspect on 3D axes
            axes.axis("equal")

        if should_block:
            pl_.show()  # Better named as TriggerMatplotlibEventLoop
            return None
        elif should_return_figure:
            if should_return_axes:
                return figure, axes
            else:
                return figure
        elif should_return_axes:
            return axes

        return None

    def _PlotWithNetworkX(
        self,
        positions_as_dict: Dict[str, Tuple[int, ...]],
        axes: pl_.axes.Axes,
        colormap: Optional[Dict[int, str]],
    ) -> None:
        #
        if colormap is None:
            colormap = self.__class__.colormap

        node_degrees = (elm[1] for elm in self.degree)
        node_colors = tuple(
            colormap[degree] if degree < 3 else colormap[2] for degree in node_degrees
        )

        nx_.draw_networkx(
            self,
            ax=axes,
            pos=positions_as_dict,
            node_color=node_colors,
            with_labels=self.label_styles[0].show,
            font_size=int(round(self.label_styles[0].size)),
            width=self.edge_styles[0].size,
        )
        if self.label_styles[1].show:
            nx_.draw_networkx_edge_labels(
                self,
                ax=axes,
                pos=positions_as_dict,
                edge_labels=self._EdgeIDsForPlot(),
                font_size=int(round(self.label_styles[1].size)),
            )

    def _PlotExplicitly(
        self,
        positions_as_dict: Dict[str, Tuple[int, ...]],
        transformation: Callable[[array_t], array_t],
        vector_transf: Callable[[array_t], array_t],
        axes: pl_.axes.Axes,
        mode: plot_mode_e,
        max_distance: float,
    ) -> None:
        #
        if mode == plot_mode_e.SKL:
            mode = "site"
        elif mode == plot_mode_e.SKL_Polyline:
            mode = "polyline"
        else:
            mode = "curve"
        dg_.Plot(
            self.edges.data("as_edge_t"),
            transformation,
            vector_transf,
            axes,
            self.edge_styles,
            self.direction_style,
            self.label_styles[1],
            mode=mode,
            max_distance=max_distance,
        )
        # TODO: there is no distinction between end nodes and isolated nodes
        nd_.PlotEndNodes(
            self.nodes.data("as_node_t"),
            transformation,
            axes,
            self.node_styles.get(1, self.node_styles[None]),
        )

        if self.dim == 2:
            nd_.Plot2DBranchNodes(
                self.nodes.data("as_node_t"),
                self.degree,
                transformation,
                axes,
                self.node_styles,
            )
            if self.label_styles[0].show:
                nx_.draw_networkx_labels(
                    self,
                    ax=axes,
                    pos=positions_as_dict,
                    font_size=int(round(self.label_styles[0].size)),
                    font_color=self.label_styles[0].color,
                )
        else:
            nd_.Plot3DBranchNodes(
                self.nodes.data("as_node_t"),
                self.degree,
                transformation,
                axes,
                self.node_styles,
            )
            if self.label_styles[0].show:
                nd_.Plot3DNodeLabels(self, positions_as_dict, axes, self.label_styles)

    def _PlotWithGraphviz(self, axes: pl_.axes.Axes) -> None:
        #
        try:
            import tempfile as tp_

            import imageio as io_
            import pygraphviz as gp_

            graph = nx_.nx_agraph.to_agraph(self)
            with tp_.NamedTemporaryFile() as tmp_accessor:
                img_name = tmp_accessor.name
                graph.layout()
                graph.draw(img_name, format="png")
                axes.imshow(io_.v3.imread(img_name))
        except Exception as exc:
            axes.text(
                0,
                0,
                f"Unable to plot graph using pygraphviz/imageio.\nPlease check installed modules.\n[{exc}]",
                horizontalalignment="center",
            )

    def _EdgeIDsForPlot(self) -> Dict[str, str]:
        #
        lengths_as_dict = nx_.get_edge_attributes(self, "length")
        w_lengths_as_dict = (
            nx_.get_edge_attributes(self, "w_length") if self.has_widths else None
        )

        w_length_str = ""
        edge_ids = {}
        for key, value in lengths_as_dict.items():
            if w_lengths_as_dict is not None:
                w_length_str = "/" + str(round(w_lengths_as_dict[key]))
            edge_ids[key[0:2]] = key[2] + "\n" + str(round(value)) + w_length_str

        return edge_ids

    def __str__(self) -> str:
        """"""
        output = (
            f"{self.__class__.__name__}:\n"
            f"    Domain lengths={self.domain_lengths}\n"
            f"    Has widths={self.has_widths}\n\n"
            f"    Components={self.n_components}\n"
            f"    Nodes={self.n_nodes}"
            f" = S_{self.n_s_nodes} + E_{self.n_e_nodes} + B_{self.n_b_nodes}\n"
            f"    Edges={self.n_edges}"
        )

        return output


def _Ball3D(center: Sequence[int], radius: int, shape: Tuple[int, int, int]) -> array_t:
    #
    output = np_.zeros(shape, dtype=np_.bool_)
    # dw_.ellipsoid leaves a one pixel margin around the ellipse, hence [1:-1, 1:-1, 1:-1]
    ellipse = dw_.ellipsoid(radius, radius, radius)[1:-1, 1:-1, 1:-1]
    sp_slices = tuple(
        slice(0, min(output.shape[idx_], ellipse.shape[idx_])) for idx_ in (0, 1, 2)
    )
    output[sp_slices] = ellipse[sp_slices]

    row, col, dep = center
    output = im_.shift(
        output, (row - radius, col - radius, dep - radius), order=0, prefilter=False
    )

    return output
