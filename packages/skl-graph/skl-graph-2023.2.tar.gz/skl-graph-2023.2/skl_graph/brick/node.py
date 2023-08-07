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

from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Tuple

import matplotlib.pyplot as pl_
import numpy as np_
import scipy.spatial as sp_
import skimage.measure as ms_
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as polygons_3d_t

import skl_graph.brick.elm_id as id_
import skl_graph.brick.topology_map as bymp
from skl_graph.brick.constants import UNTESTED_VALIDITY
from skl_graph.brick.plot import label_style_t, node_style_h, node_styles_h


array_t = np_.ndarray


class node_t:
    #
    __slots__ = ("uid", "position", "invalidities")

    uid: str
    position: array_t
    invalidities: List[str]  # Use brick.constants.UNTESTED_VALIDITY as initial value

    def __init__(self):
        #
        for slot in self.__class__.__slots__:
            setattr(self, slot, None)
        self.invalidities = UNTESTED_VALIDITY

    def _SetUID(self) -> None:
        #
        self.uid = id_.COORDINATE_SEPARATOR.join(
            coord.__str__() for coord in self.position
        )

    @property
    def is_valid(self) -> bool:
        """"""
        output = True
        self.invalidities = []

        if self.uid is None:
            output = False
            self.invalidities.append("Has no UID")

        return output

    def __str__(self) -> str:
        """"""
        return f"{self.__class__.__name__}[{self.uid}]: Pos={self.position}"


class end_node_t(node_t):
    #
    __slots__ = ("diameter",)

    diameter: float

    def __init__(self):
        #
        super().__init__()
        for slot in self.__class__.__slots__:
            setattr(self, slot, None)

    @classmethod
    def WithPosition(cls, position: array_t, width_map: array_t = None) -> end_node_t:
        #
        instance = cls()

        instance.position = position
        if width_map is not None:
            instance.diameter = width_map.item(tuple(position))
        instance._SetUID()

        return instance


class branch_node_t(node_t):
    #
    __slots__ = ("sites", "diameters")

    sites: Tuple[array_t, ...]
    diameters: array_t

    def __init__(self):
        #
        super().__init__()
        for slot in self.__class__.__slots__:
            setattr(self, slot, None)

    @classmethod
    def WithCentroidAndSites(
        cls, centroid: array_t, sites: Tuple[array_t, ...], width_map: array_t = None
    ) -> branch_node_t:
        #
        # TODO: why passing the centroid instead of computing it here from sites?
        # TODO: sites is not optional but seems to be considered as such from at least a calling function (do a search to find out which)
        instance = cls()

        sites_as_array = np_.array(sites)
        centroid = np_.around(centroid).reshape((-1, 1))
        segments = sites_as_array - centroid
        medoid_idx = (segments**2).sum(axis=0).argmin()
        # np_.array(): fresh array instead of a view of sites_as_array
        position = np_.array(sites_as_array[:, medoid_idx].squeeze())

        instance.position = position
        instance.sites = sites
        if width_map is not None:
            instance.diameters = width_map[sites]
        instance._SetUID()

        return instance


def EndNodes(
    part_map: array_t, width_map: array_t = None
) -> Tuple[List[end_node_t], array_t]:
    #
    # Note: End nodes are necessarily single-pixel nodes. Hence, they have no coordinate list.
    #
    # Not uint to allow for subtraction
    e_node_lmap = (part_map == 1).astype(np_.int64)  # Not really an lmsk here
    e_node_coords = np_.where(e_node_lmap)

    e_nodes = e_node_coords[0].__len__() * [end_node_t()]
    for n_idx, position in enumerate(zip(*e_node_coords)):
        end_node = end_node_t.WithPosition(
            np_.array(position, dtype=np_.int64), width_map=width_map
        )
        e_nodes[n_idx] = end_node
        e_node_lmap[position] = n_idx + 1  # Now that's becoming an lmsk

    return e_nodes, e_node_lmap


def BranchNodes(
    part_map: array_t, width_map: array_t = None
) -> Tuple[List[branch_node_t], array_t]:
    #
    # Note: Branch nodes always have a coordinate list (i.e., even if they are single-pixeled)
    #
    b_node_map = np_.logical_and(
        part_map > 2, part_map != bymp.TMapBackgroundLabel(part_map)
    )
    b_node_lmap, n_b_nodes = bymp.LABELING_FCT_FOR_DIM[part_map.ndim](b_node_map)

    b_node_props = ms_.regionprops(b_node_lmap)

    b_nodes = n_b_nodes * [branch_node_t()]
    for n_idx, props in enumerate(b_node_props):
        sites = props.image.nonzero()
        for d_idx in range(part_map.ndim):
            sites[d_idx].__iadd__(props.bbox[d_idx])
        branch_node = branch_node_t.WithCentroidAndSites(
            props.centroid, sites=sites, width_map=width_map
        )
        b_nodes[n_idx] = branch_node

    return b_nodes, b_node_lmap


def PlotEndNodes(
    nodes: Iterable[Tuple[str, node_t]],
    transformation: Callable[[array_t], array_t],
    axes: pl_.axes.Axes,
    node_style: node_style_h,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    positions = np_.array(
        tuple(node.position for _, node in nodes if isinstance(node, end_node_t))
    )
    if positions.size == 0:
        return

    plot_style = node_style.color + node_style.type

    if positions.shape[1] == 2:
        axes.plot(
            positions[:, 1],
            transformation(positions[:, 0]),
            plot_style,
            markersize=node_style.size,
        )
    else:
        axes.plot3D(
            positions[:, 1],
            transformation(positions[:, 0]),
            positions[:, 2],
            plot_style,
            markersize=node_style.size,
        )


def Plot2DBranchNodes(
    nodes: Iterable[Tuple[str, node_t]],
    degrees: Iterable[int],
    transformation: Callable[[array_t], array_t],
    axes: pl_.axes.Axes,
    node_styles: node_styles_h,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    positions_0, positions_1, styles, sizes = [], [], [], []
    for (_, node), degree in zip(nodes, degrees):
        degree: Tuple[str, int]
        if isinstance(node, branch_node_t):
            node_style = node_styles.get(degree[1], node_styles[None])

            coords_0 = node.sites[1]
            coords_1 = transformation(node.sites[0])
            if coords_0.size > 2:
                try:
                    hull = sp_.ConvexHull(np_.transpose((coords_0, coords_1)))
                except sp_.QhullError:
                    # TODO: check when this happens, in particular flat convex hull
                    axes.plot(
                        coords_0,
                        coords_1,
                        node_style.color + "-",
                        linewidth=0.3 * node_style.size,
                    )
                else:
                    vertices = hull.vertices
                    axes.fill(coords_0[vertices], coords_1[vertices], node_style.color)
            elif coords_0.size > 1:
                axes.plot(
                    coords_0,
                    coords_1,
                    node_style.color + "-",
                    linewidth=0.3 * node_style.size,
                )

            # Grouping for "better performances"
            positions_0.extend(coords_0)
            positions_1.extend(coords_1)
            styles.extend(coords_0.size * (node_style.color + node_style.type,))
            sizes.extend(coords_0.size * (node_style.size,))

    if positions_0.__len__() > 0:
        # NOTE: axes.plot does not accept one style and one size per node. Hence the "styles[0]" and "sizes[0]".
        axes.plot(positions_0, positions_1, styles[0], markersize=sizes[0])


def Plot3DBranchNodes(
    nodes: Iterable[Tuple[str, node_t]],
    degrees: Iterable[int],
    transformation: Callable[[array_t], array_t],
    axes: pl_.axes.Axes,
    node_styles: node_styles_h,
) -> None:
    """
    nodes: all the nodes of the graph, so that filtering is needed here
    """
    positions_0, positions_1, positions_2, styles, sizes = [], [], [], [], []
    for (_, node), degree in zip(nodes, degrees):
        degree: Tuple[str, int]
        if isinstance(node, branch_node_t):
            node_style = node_styles.get(degree[1], node_styles[None])

            coords_0 = node.sites[1]
            coords_1 = transformation(node.sites[0])
            coords_2 = node.sites[2]
            if coords_0.size > 3:
                try:
                    coords = np_.transpose((coords_0, coords_1, coords_2))
                    hull = sp_.ConvexHull(coords)
                    triangle_lst = []
                    for face in hull.simplices:
                        triangle_lst.append(
                            [coords[v_idx, :].tolist() for v_idx in face]
                        )
                    triangle_lst = polygons_3d_t(
                        triangle_lst,
                        facecolors=node_style.color,
                        edgecolors="b",
                        linewidth=0.6 * node_style.size,
                    )
                    axes.add_collection3d(triangle_lst)
                except:
                    # TODO: better space-filling drawing: to be done
                    axes.plot3D(
                        coords_0,
                        coords_1,
                        coords_2,
                        node_style.color + ".",
                        markersize=node_style.size,
                    )
            elif coords_0.size > 2:
                triangle = list(zip(coords_0, coords_1, coords_2))
                triangle_lst = polygons_3d_t([triangle], facecolors=node_style.color)
                axes.add_collection3d(triangle_lst)
            elif coords_0.size > 1:
                axes.plot3D(
                    coords_0,
                    coords_1,
                    coords_2,
                    node_style.color + "-",
                    linewidth=0.3 * node_style.size,
                )

            # Grouping for "better performances"
            positions_0.extend(coords_0)
            positions_1.extend(coords_1)
            positions_2.extend(coords_2)
            styles.extend(coords_0.size * (node_style.color + node_style.type,))
            sizes.extend(coords_0.size * (node_style.size,))

    if positions_0.__len__() > 0:
        # NOTE: axes.plot3D does not accept one style and one size per node. Hence the "styles[0]" and "sizes[0]".
        axes.plot3D(
            positions_0, positions_1, positions_2, styles[0], markersize=sizes[0]
        )


def Plot3DNodeLabels(
    nodes: Iterable[str],
    positions_as_dict: Dict[str, Tuple[int, ...]],
    axes: pl_.axes.Axes,
    style: label_style_t,
) -> None:
    #
    for node in nodes:
        axes.text(
            *positions_as_dict[node], node, fontsize=style.size, color=style.color
        )
