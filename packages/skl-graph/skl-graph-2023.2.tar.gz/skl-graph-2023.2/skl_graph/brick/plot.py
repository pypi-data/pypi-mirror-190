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

from enum import Enum as enum_t
from typing import Dict
from typing import NamedTuple as named_tuple_t
from typing import Tuple, Union

import matplotlib.pyplot as pypl


axes_t = pypl.Axes
figure_t = pypl.Figure


class plot_mode_e(enum_t):
    Networkx = 0
    SKL = 1
    SKL_Polyline = 2
    SKL_Curve = 3
    Graphviz = 4


class plot_style_t(named_tuple_t):
    type: str  # E.g., "." for nodes and "-" for edges
    size: int  # "markersize" for nodes, "linewidth" for edges
    color: str  # E.g., "b"


class direction_style_t(named_tuple_t):
    show: bool
    size: int  # "linewidth"
    color: str  # "k"


class label_style_t(named_tuple_t):
    show: bool
    size: float  # "fontsize"
    color: str  # "k"


node_style_h = plot_style_t
node_styles_h = Dict[Union[int, None], node_style_h]
node_style_unstructured_h = Tuple[str, int, str]  # type, size, color
node_styles_unstructured_h = Dict[Union[int, None], node_style_unstructured_h]

edge_style_h = plot_style_t
edge_styles_h = Tuple[edge_style_h, edge_style_h]  # regular edges, self-loops
edge_style_unstructured_h = node_style_unstructured_h
edge_styles_unstructured_h = Tuple[edge_style_unstructured_h, edge_style_unstructured_h]

direction_style_unstructured_h = Tuple[bool, int, str]  # show, size, color

label_styles_h = Tuple[label_style_t, label_style_t]  # nodes, edges
label_style_unstructured_h = Tuple[bool, float, str]  # show, size, color
label_styles_unstructured_h = Tuple[label_style_unstructured_h, label_style_unstructured_h]
