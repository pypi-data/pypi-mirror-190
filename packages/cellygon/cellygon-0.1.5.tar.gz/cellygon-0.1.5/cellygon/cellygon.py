#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:56:01 2019

@author: henrik
"""

import warnings

import mahotas as mh
import networkx as nx
import numpy as np
import pyvista as pv
import vtk
from imgmisc import (
    compute_neighbours,
    flatten,
    get_layers,
    merge,
    validate_connectivity,
    validate_inputs,
)
from scipy.spatial import KDTree


def unit_vec(vector):
    """Compute the L2 norm unit vector"""
    return vector / np.linalg.norm(vector)


def angle(v1, v2, v3):
    """Compute the angle defined by the vectors v1-v2 and v3-v2"""
    u = unit_vec(np.array(v1) - np.array(v2))
    v = unit_vec(np.array(v3) - np.array(v2))
    angle = np.arccos(np.clip(np.dot(u, v), -1, 1)) / (2 * np.pi) * 360
    return angle


def vertex_cycles(mesh):
    """
    Find all the simple vertex cycles in the mesh. The function uses the mesh
    edges to identify if two vertices are connected or not.

    Parameters:
        mesh : pyvista.PolyData mesh object

    Returns:
        cycles : a list of lists containing the ordered vertex indices for each
            cycle in the mesh

    """
    neighs = get_connected_vertices_all(mesh, include_self=True)
    pairs = []
    for ii in range(mesh.n_points):
        for pp in neighs[ii]:
            pairs.append((ii, pp))
    net = nx.Graph(pairs)
    cycles = nx.cycle_basis(net)
    cycles.sort(key=lambda x: len(x), reverse=True)
    return cycles


def consolidate_disjoint_cells(
    j_indices, j_neighs, edges=None, background=0, allow_triangles=True
):
    """
    Get cell polygons and remove entries that don't make up complete cells
    """
    # Get cell polygons and remove entries in j_neighs that don't make up complete cells
    if edges is not None:
        warnings.warn(
            "NotImplementedWarning::`edges variable supplied, but using supplied edges not implemented. The function will proceed by computing edges from the supplied indices and neighbourhoods."
        )

    iteration = 0
    while True:
        iteration += 1

        n_before = len(j_indices)
        labels, label_counts = np.unique(flatten(j_neighs), return_counts=True)
        labels = labels[labels != background]

        to_merge = []
        for label in labels:

            # Find which junctions belong to a given cell label
            label_in = np.where([label in nn for nn in j_neighs])[0]
            cell_edges = find_edges(j_indices[label_in], j_neighs[label_in])

            # Compute the cycles from the given cell edges. If
            # there are more than one cycle,
            net = nx.Graph()
            net.add_edges_from(cell_edges)
            cycles = nx.cycle_basis(net)
            breaking = False
            if len(cycles) > 1:
                for cc1, cyc1 in enumerate(cycles):
                    if breaking:
                        break
                    for cc2, cyc2 in enumerate(cycles):
                        if cc2 <= cc1:
                            continue
                        # if the cells have no overlap, or only connect by a single
                        # vertex (e.g. due to cell overhang), compress the cell
                        if np.intersect1d(cyc1, cyc2).shape[0] < 2:
                            to_merge.append(
                                list(label_in[np.array(cyc1)])
                                if len(cyc1) < len(cyc2)
                                else list(label_in[np.array(cyc2)])
                            )
                            breaking = True
                            break

            # Collate the junctions which are bound to be merged and identify
            # the ones which are to be removed.
            to_merge = merge(to_merge)
            to_remove = []
            for group in to_merge:
                group = np.asarray(list(group))
                j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
                j_indices[group[0]] = np.mean(j_indices[group], 0)
                to_remove.extend(list(group[1:]))
        to_keep = np.logical_not(np.isin(np.arange(j_indices.shape[0]), to_remove))
        j_indices = j_indices[to_keep]
        j_neighs = j_neighs[to_keep]

        if len(j_indices) == n_before:
            break

    return j_indices, j_neighs


def get_connected_vertices(mesh, index, include_self=True):
    """
    For a given vertex in a mesh, return the list of vertex indices which
    this is connected to (as defined by edge connectivity).

    mesh: a pyvista.PolyData mesh object
    index: the index of the vertex in the mesh
    include_self: bool, default=True. Whether to include its own index

    Returns:
        connected_vertices: a numpy.array of the connected vertices
    """
    connected_vertices = []
    if include_self:
        connected_vertices.append(index)

    cell_id_list = vtk.vtkIdList()
    mesh.GetPointCells(index, cell_id_list)

    # Loop through each cell using the seed point
    for ii in range(cell_id_list.GetNumberOfIds()):
        cell = mesh.GetCell(cell_id_list.GetId(ii))

        if cell.GetCellType() == 3:
            point_id_list = cell.GetPointIds()

            # add the point which isn't the seed
            to_add = (
                point_id_list.GetId(1)
                if point_id_list.GetId(0) == index
                else point_id_list.GetId(0)
            )
            connected_vertices.append(to_add)
        else:
            # Loop through the edges of the point and add all points on these.
            for jj in range(cell.GetNumberOfEdges()):
                point_id_list = cell.GetEdge(jj).GetPointIds()

                # add the point which isn't the seed
                to_add = (
                    point_id_list.GetId(1)
                    if point_id_list.GetId(0) == index
                    else point_id_list.GetId(0)
                )
                connected_vertices.append(to_add)

    connected_vertices = np.unique(connected_vertices)

    return connected_vertices


def get_connected_vertices_all(mesh, include_self=True):
    """
    For each vertex in a given mesh, return the list of vertex indices which
    this is connected to (as defined by edge connectivity).

    mesh: a pyvista.PolyData mesh object
    include_self: bool, default=True. Whether to include its own index

    Returns:
        connectivites: a numpy.array containing of length N where N is the number
        of vertices in the mesh. Each element is a list of the connected vertices
        for that corresponding vertex.
    """

    connectivities = [[]] * mesh.n_points
    for ii in range(mesh.n_points):
        connectivities[ii] = get_connected_vertices(mesh, ii, include_self)

    connectivities = np.array(connectivities)

    return connectivities


def boundary_edges(mesh):
    """Return the boundary edges of a mesh"""
    boundary = mesh.extract_feature_edges(
        boundary_edges=1,
        feature_edges=0,
        feature_angle=0,
        manifold_edges=0,
        non_manifold_edges=0,
    )
    return boundary


def consolidate_holes(tripoly, j_neighs, background=0, mode="all"):
    """
    Consolidate holes in a triangulated polygonised mesh.

    This function takes three arguments:

        tripoly: a triangulated polygon mesh.
        j_neighs: a list of N arrays, where each array contains the labels of the
            neighboring cells of the corresponding junction in tripoly.
        background: an integer specifying the cell id of the background. (default: 0)
        mode: a string specifying the consolidation mode. It can be 'all' to consolidate
            all holes, or 'largest' to only consolidate the largest hole. (default: 'all')

    The function extracts the boundary of tripoly and then uses the vertex_cycles function
    to find all cycles in the boundary. For each cycle, it finds the cell id with the
    highest number of neighbors among all cells in the neighborhood of the junctions
    forming the cycle. If mode is set to 'largest' or (if mode is 'all' and the highest
    count is equal to the length of the cycle), then the function consolidates the
    cycle by adding a point in the center of the cycle and updating the cell id of
    all junctions in the cycle to be the cell id with the highest count. The function
    returns the updated tripoly.

    NB: This can create large, unrealistic cells.
    """
    tripoly = tripoly.copy()
    prev_ids = tripoly["cell_id"].copy()

    # Identify the mesh boundary and the cycles therein (i.e. the holes)
    boundary = boundary_edges(tripoly)
    bdpts = boundary.points
    cycles = vertex_cycles(boundary)
    cycles = [c for c in cycles if len(c) > 1]
    cycles = [[tripoly.FindPoint(bdpts[ii]) for ii in cyc] for cyc in cycles]

    # Go through the cycles and identify the junctions to define a new cell
    # based on the merging criterion
    added = 0
    new_pts = []
    new_faces = []
    new_cids = []
    for cyc in cycles[1:]:
        cyc_j_neighs = np.asarray(flatten(j_neighs[np.array(cyc)]))
        labs, cts = np.unique(
            cyc_j_neighs[
                ~np.isin(cyc_j_neighs, np.append(tripoly["cell_id"], background))
            ],
            return_counts=True,
        )
        maxlab = labs[np.argmax(cts)]
        if mode == "largest" or (mode == "all" and max(cts) == len(cyc)):
            # Add the new cell
            new_faces.extend(
                np.ravel(
                    [
                        [3, cyc[cc - 1], cyc[cc], tripoly.n_points + added]
                        for cc in range(len(cyc))
                    ]
                )
            )
            new_pts.append(np.mean(tripoly.points[cyc], 0))
            new_cids.extend([maxlab] * len(cyc))
            added += 1

    # Update the mesh
    tripoly.points = np.vstack([tripoly.points, new_pts])
    tripoly.faces = np.hstack([tripoly.faces, np.hstack(new_faces)])
    tripoly["cell_id"] = np.hstack([prev_ids, new_cids])

    return tripoly


#


def merge_junctions_euclidean(j_indices, j_neighs, r):
    """
    Merge junctions by Euclidean distance.

    This function takes three arguments:

        j_indices: a numpy array of shape (N, 3) containing the xyz coordinates of N junctions.
        j_neighs: a list of N arrays, where each array contains the list of cell labels which a junction belongs to.
        r: a float specifying the maximum Euclidean distance between two junctions to be merged.

    The function uses scipy's KDTree to identify pairs of junctions that are within r distance of each other,
    and then merges them using a merge function. The merged junctions have their coordinates updated to be
    the mean of the merged junctions' coordinates. The function returns the updated j_indices and j_neighs
    after the merging process.
    """

    tree = KDTree(j_indices)
    matches = tree.query_ball_tree(tree, r=r)
    to_merge = merge(matches)
    to_remove = []
    # j_neighs = np.array([vv for vv in j_neighs])
    j_neighs = list(j_neighs)
    for group in to_merge:
        group = np.asarray(list(group))
        j_neighs[group[0]] = np.unique(np.hstack([j_neighs[gg] for gg in group]))
        j_indices[group[0]] = np.mean(j_indices[group], 0)
        to_remove.extend(list(group[1:]))

    to_keep = np.logical_not(np.isin(np.arange(j_indices.shape[0]), to_remove))
    j_indices = j_indices[to_keep]
    j_neighs = np.array(j_neighs)[to_keep]
    return j_indices, j_neighs


def find_junctions(
    image,
    background=0,
    threshold=3,
    merge_adjacent=True,
    resolution=None,
    include_set="l1",
):
    """
    Find junction points in a labelled (segmented) image.

    This function takes in a label image, where each label represents a different
    object, and finds the points in the image where more than one structure intersects.
    These points are referred to as junctions. The function returns the coordinates
    of these junctions and the labels of the structures that intersect at each junction.

    Parameters:
        image (ndarray): A 3D label image where each label represents a different
            object.
        background (int, optional): Value used to represent background in the image,
            with a default of 0.
        threshold (int, optional): Minimum number of different labels that must
            intersect at a point for it to be considered a junction, with a default
            of 3.
        merge_adjacent (bool, optional): Whether to merge voxel-adjacent junctions
            into a single junction, with a default of True.
        resolution (list or tuple, optional): The voxel size of the image in the
            form [z_res, y_res, x_res]. If not provided, a default value of [1, 1, 1]
            is used.
        include_set (str, optional): Collection of labels to include for junction
            detection. Currently, only 'l1' is supported.

    Returns:
        j_indices (ndarray): The coordinates of the junction points in the image.
        j_neighs (ndarray): The labels of the objects that intersect at each junction.
    """

    connectivity = 3
    image, mask, resolution = validate_inputs(image, mask=None, resolution=resolution)
    connectivity, offset = validate_connectivity(image.ndim, connectivity, offset=None)
    mask = mh.borders(image, connectivity)

    if include_set == "l1":
        include = get_layers(image, background=background, depth=1)[0]
    elif isinstance(include, list(np.array)):
        include = include_set
    else:
        raise Exception("Inclusion set uncompatible.")

    # get the distances to the neighbours
    neighbours = connectivity.copy()
    neighbours[tuple(offset)] = False
    neighbours = np.array(np.where(neighbours)).T
    neighbours = np.multiply(neighbours, resolution)
    neighbours = np.subtract(neighbours, offset)

    # pad the image, and mask so that we can use the mask to keep from running
    # off the edges
    pad_width = [(p, p) for p in offset]
    image = image.astype(float)  # to allow -1 padding
    image = np.pad(image, pad_width, mode="constant", constant_values=-1)
    mask = np.pad(mask, pad_width, mode="constant", constant_values=0)

    # get flattened versions of everything
    flat_neighbourhood = compute_neighbours(image, connectivity, offset)
    image_raveled = image.ravel()
    indices = np.where(mask.ravel())[0]

    point_neighbours = np.array(list(map(lambda x: x + flat_neighbourhood, indices)))
    neighs = image_raveled[point_neighbours]

    # Identify all voxels that neighbour at least 3 different cell ids and neighbour the background
    # TODO include option to include vertices that border both -1 and background
    # TODO generalise to not be restricted to epidermis
    # - TODO change hard-coding for L1 to other collections of labels as well
    junctions = []
    to_keep = include
    for row in neighs:
        r = np.unique(row)
        if background not in r:
            junctions.append(False)
        else:
            r = r[np.isin(r, to_keep)]
            junctions.append(len(r) >= threshold)

    # Extract the vertex coordinates and information about what cells junctions belong to
    j_indices_raveled = indices[junctions]
    j_indices = np.asarray(np.unravel_index(j_indices_raveled, image.shape)).T
    j_neighs = np.asarray([np.unique(row) for row in neighs[junctions]])

    # Consolidate junctions that are neighbours with one another
    if merge_adjacent:
        to_merge = []
        for ii, pt in enumerate(point_neighbours[junctions]):
            for jj, nb in enumerate(pt):
                if nb in j_indices_raveled:
                    to_merge.append([ii, np.where(j_indices_raveled == nb)[0][0]])
        to_merge = merge(to_merge)
        to_remove = []
        new_coords = []
        for group in to_merge:
            group = np.asarray(list(group))
            j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
            new_coords.append(j_indices_raveled[group])
            to_remove.extend(list(group[1:]))

        keep_indices = np.logical_not(np.isin(np.arange(len(j_neighs)), to_remove))
        j_indices_raveled = j_indices_raveled[keep_indices]
        j_indices = np.asarray(np.unravel_index(j_indices_raveled, image.shape)).T
        j_neighs = j_neighs[keep_indices]

        # Update the coordinates and vertex cell neighbours
        merged_coords = np.asarray(
            [
                np.mean(np.asarray(np.unravel_index(nc, image.shape)).T, 0)
                for nc in new_coords
            ]
        )
        for ii, orig_coords in enumerate(
            [np.asarray(np.unravel_index(nc[0], image.shape)).T for nc in new_coords]
        ):
            j_indices[
                np.where(np.all(j_indices == orig_coords, 1))[0][0]
            ] = merged_coords[ii]

    return j_indices, j_neighs


def center_triangulation(
    j_indices, j_neighs, background=0, allow_triangles=True, return_ids=True
):
    """
    Perform a center triangulation of the cells.

    Parameters
    ----------
    j_indices : np.array of shape (N, 3)
        Coordinates in 3d space.
    j_neighs : np.array of lists
        The neighbouring cell labels for each vertex.
    background : int
        The background label (default: 0).
    allow_triangles : bool, optional
        Whether to allow triangular cells. The default is True.
    return_ids : bool, optional
        Whether to return the cell ids for labelling the mesh. The default is True.

    Returns
    -------
    The coordinates, faces (and vertex cell ids)

    """
    cpolys = polygon_cycles(
        j_indices,
        j_neighs,
        edges=None,
        background=background,
        allow_triangles=allow_triangles,
    )
    cycles = np.asarray(list(cpolys.values()))
    centers = np.asarray(
        [np.mean(j_indices[cycles[ii]], 0) for ii in range(len(cycles))]
    )

    faces = []
    for ii, cyc in enumerate(cycles):
        for jj in range(len(cyc)):
            faces.append([cyc[jj - 1], cyc[jj], j_indices.shape[0] + ii])
    faces = np.asarray(faces)
    j_coords = np.vstack([j_indices, centers])

    if return_ids:
        cell_ids = flatten(
            [[list(cpolys.keys())[ii]] * (len(cycles[ii])) for ii in range(len(cycles))]
        )
        return j_coords, faces, cell_ids
    return j_coords, faces


def merge_identical_junctions(j_indices, j_neighs):
    """
    Merge junctions with the same cell neighbours
    """
    to_merge = []
    for ii, jneighs1 in enumerate(j_neighs):
        for jj, jneighs2 in enumerate(j_neighs):
            if jj <= ii:
                continue
            else:
                # overlap = np.intersect1d(jneighs1, jneighs2).shape[0]
                if len(jneighs1) == len(jneighs2) and np.all(
                    np.sort(jneighs2) == np.sort(jneighs1)
                ):
                    to_merge.append([ii, jj])
    to_merge = merge(to_merge)
    to_remove = []
    for group in to_merge:
        group = np.asarray(list(group))
        j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
        to_remove.extend(list(group[1:]))

    keep_indices = np.logical_not(np.isin(np.arange(len(j_neighs)), to_remove))
    # j_indices_raveled = j_indices_raveled[keep_indices]
    j_indices = j_indices[keep_indices]
    j_neighs = j_neighs[keep_indices]
    return j_indices, j_neighs


def merge_similar_junctions(j_indices, j_neighs, threshold=4):
    """
    Merge junctions with sufficiently many similar cell neighbours
    """
    iteration = 0
    while True:
        print(iteration)
        iteration += 1
        n_before = j_indices.shape[0]
        to_merge = []
        for ii, jneighs1 in enumerate(j_neighs):
            for jj, jneighs2 in enumerate(j_neighs):
                if jj <= ii:
                    continue
                else:
                    overlap = np.intersect1d(jneighs1, jneighs2).shape[0]
                    if overlap >= threshold:
                        to_merge.append([ii, jj])
        to_merge = merge(to_merge)
        to_remove = []
        for group in to_merge:
            group = np.asarray(list(group))
            j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
            to_remove.extend(list(group[1:]))

        keep_indices = np.logical_not(np.isin(np.arange(len(j_neighs)), to_remove))
        j_indices = j_indices[keep_indices]
        j_neighs = j_neighs[keep_indices]

        if j_indices.shape[0] == n_before:
            break

    return j_indices, j_neighs


def find_edges(j_indices, j_neighs, threshold=3):
    """Compute the edges from a list of junction cell neighbours"""
    edges = []
    for ii, jneighs1 in enumerate(j_neighs):
        for jj, jneighs2 in enumerate(j_neighs):
            if jj <= ii:
                continue
            else:
                overlap = np.intersect1d(jneighs1, jneighs2).shape[0]
                if (
                    overlap >= threshold
                    and [ii, jj] not in edges
                    and [jj, ii] not in edges
                ):
                    edges.append([ii, jj])

    # Remove edges to vertices that are only connected with one edge
    indices, counts = np.unique(edges, return_counts=True)
    to_keep = indices[counts > 1]
    edges = [edge for edge in edges if np.all(np.isin(edge, to_keep))]

    return edges


def triangle_area(verts):
    """Compute the area of a triangle defined by the input vertices"""
    if verts.ndim < 2:
        verts = np.expand_dims(verts, 0)
    v1 = verts[:, 0, :] - verts[:, 1, :]
    v2 = verts[:, 0, :] - verts[:, 2, :]
    del verts

    # Area of a triangle in 3D is 1/2 * norm of the cross product
    area = ((np.cross(v1, v2) ** 2).sum(axis=1) ** 0.5) / 2.0
    return area


def clean(j_indices, j_neighs, return_edges=True):
    """Remove duplicate vertices"""
    while True:
        n_before = j_indices.shape[0]
        edges = find_edges(j_indices, j_neighs)

        junctions = np.arange(len(j_indices))
        in_edges, counts = np.unique(edges, return_counts=True)
        to_keep = np.isin(junctions, in_edges)

        j_indices = j_indices[to_keep]
        j_neighs = j_neighs[to_keep]

        j_indices = j_indices[counts > 1]
        j_neighs = j_neighs[counts > 1]

        if j_indices.shape[0] == n_before:
            break

    if not return_edges:
        return j_indices, j_neighs
    else:
        edges = find_edges(j_indices, j_neighs)
        return j_indices, j_neighs, edges


def create_polydata(j_indices, faces, resolution=[1, 1, 1]):
    """Generate a polydata object from coordinates and faces."""
    poly = pv.PolyData(
        j_indices * resolution, np.ravel(np.c_[[len(ff) for ff in faces], faces])
    )
    return poly


def polygon_cycles(j_indices, j_neighs, edges=None, background=0, allow_triangles=True):
    """
    Generate the cycle polygons for each well-defined cell label.

    Parameters
    ----------
    j_indices : np.array of shape (N, 3)
        Coordinates in 3d space.
    j_neighs : np.array of lists
        The neighbouring cell labels for each vertex.
    background : int
        The background label (default: 0).
    allow_triangles : bool, optional
        Whether to allow triangular cells. The default is True.
    return_ids : bool, optional
        Whether to return the cell ids for labelling the mesh. The default is True.

    Returns
    -------
    cells: a dict with the key being the cell label, and the value being the list
        of vertices defining the cell cycle (in order).

    """

    # Get cell polygons and remove entries in j_neighs that don't make up complete cells
    labels, label_counts = np.unique(flatten(j_neighs), return_counts=True)
    labels = labels[label_counts > (2 if allow_triangles else 3)]
    labels = labels[labels != background]
    cells = {}
    for ii in labels:
        ii_in = np.where([ii in nn for nn in j_neighs])[0]
        if edges is None:
            cell_edges = find_edges(j_indices[ii_in], j_neighs[ii_in])
        else:
            # TODO - make this work with provided edges
            pass
        net = nx.Graph()
        net.add_edges_from(cell_edges)
        cycles = nx.cycle_basis(net)
        if len(cycles) == 1:
            cycle = ii_in[cycles[0]]
            cells[ii] = cycle
    return cells


# def find_junctions_all(image, background=0, threshold=3, merge_adjacent=True, resolution=None, include_set='l1'):
#     connectivity = 3

#     image, mask, resolution = validate_inputs(
#         image, mask=None, resolution=resolution)
#     connectivity, offset = validate_connectivity(image.ndim, connectivity,
#                                                  offset=None)
#     mask = mh.borders(image, connectivity)

#     # get the distances to the neighbours
#     neighbours = connectivity.copy()
#     neighbours[tuple(offset)] = False
#     neighbours = np.array(np.where(neighbours)).T
#     neighbours = np.multiply(neighbours, resolution)
#     neighbours = np.subtract(neighbours, offset)

#     # pad the image, and mask so that we can use the mask to keep from running
#     # off the edges
#     pad_width = [(p, p) for p in offset]
#     image = image.astype(float)  # to allow -1 padding
#     image = np.pad(image, pad_width, mode='constant', constant_values=-1)
#     mask = np.pad(mask, pad_width, mode='constant', constant_values=background)

#     # get flattened versions of everything
#     flat_neighbourhood = compute_neighbours(image, connectivity, offset)
#     image_raveled = image.ravel()
#     indices = np.where(mask.ravel())[0]

#     point_neighbours = np.array(
#         list(map(lambda x: x + flat_neighbourhood, indices)))
#     neighs = image_raveled[point_neighbours]

#     # Identify all voxels that neighbour at least 3 different cell ids and neighbour the background
#     # TODO include option to include vertices that border both -1 and background
#     # TODO generalise to not be restricted to epidermis
#     # - TODO change hard-coding for L1 to other collections of labels as well
#     junctions = []
#     # to_keep = include
#     for row in neighs:
#         r = np.unique(row)
#         junctions.append(len(r) >= threshold)

#     # Extract the vertex coordinates and information about what cells junctions belong to
#     j_indices_raveled = indices[junctions]
#     j_indices = np.asarray(np.unravel_index(j_indices_raveled, image.shape)).T
#     j_neighs = np.asarray([np.unique(row) for row in neighs[junctions]])

#     # Consolidate junctions that are neighbours with one another
#     if merge_adjacent:
#         to_merge = []
#         for ii, pt in enumerate(point_neighbours[junctions]):
#             for jj, nb in enumerate(pt):
#                 if nb in j_indices_raveled:
#                     to_merge.append(
#                         [ii, np.where(j_indices_raveled == nb)[0][0]])
#         to_merge = merge(to_merge)
#         to_remove = []
#         new_coords = []
#         for group in to_merge:
#             group = np.asarray(list(group))
#             j_neighs[group[0]] = np.unique(np.hstack(j_neighs[group]))
#             new_coords.append(j_indices_raveled[group])
#             to_remove.extend(list(group[1:]))

#         keep_indices = np.logical_not(
#             np.isin(np.arange(len(j_neighs)), to_remove))
#         j_indices_raveled = j_indices_raveled[keep_indices]
#         j_indices = np.asarray(np.unravel_index(
#             j_indices_raveled, image.shape)).T
#         j_neighs = j_neighs[keep_indices]

#         merged_coords = np.asarray(
#             [np.mean(np.asarray(np.unravel_index(nc, image.shape)).T, 0) for nc in new_coords])
#         for ii, orig_coords in enumerate([np.asarray(np.unravel_index(nc[0], image.shape)).T for nc in new_coords]):
#             j_indices[np.where(np.all(j_indices == orig_coords, 1))[
#                 0][0]] = merged_coords[ii]

#     return j_indices, j_neighs


# def remove_duplicated_vertices(j_indices, j_neighs):
#     keep = []
#     for ii, jn1 in enumerate(j_neighs):
#         duplicated = False
#         for jj, jn2 in enumerate(j_neighs):
#             if jj > ii and np.all(jn1 == jn2):
#                 duplicated = True
#                 break
#         keep.append(not duplicated)
#     keep = np.asarray(keep)
#     j_indices = j_indices[keep]
#     j_neighs = j_neighs[keep]
#     return j_indices, j_neighs

# def problematic_vertices(j_indices, j_neighs, edges=None, background=0, threshold=4):
#     # Identify all vertices that has more than two connections to the same cell id
#     if edges is None:
#         edges = find_edges(j_indices, j_neighs)
#     poly = create_polydata(j_indices, edges)
#     neighs = get_connected_vertices_all(poly, True)
#     problematic = []
#     for ii, ji in enumerate(j_indices):
#         nneighs = np.hstack(j_neighs[neighs[ii]])
#         nneighs = nneighs[nneighs != background]
#         vals, counts = np.unique(nneighs, return_counts=True)
#         if any(counts >= threshold):
#             problematic.append(ii)
#     problematic = np.asarray(problematic)
#     return problematic


# def proj_to_plane(point, v1, v2, v3):
#     """Project a point onto the plane defined by the three vertices v1, v2, v3"""
#     # Project point onto the plane defined by v1, v2, v3
#     new_i = unit_vec(np.array(v1) - np.array(v2))
#     new_j = unit_vec(np.array(v3) - np.array(v2))
#     new_k = np.cross(new_i, new_j)
#     change_of_basis = np.array([new_i, new_j, new_k]).transpose()
#     point = np.array(
#         [[point[0] - v2[0]], [point[1] - v2[1]], [point[2] - v2[2]]])
#     point_in_new_basis = np.dot(np.linalg.inv(change_of_basis), point)
#     proj_in_new_basis = np.copy(point_in_new_basis)
#     proj_in_new_basis[2, 0] = 0
#     proj = ((np.dot(change_of_basis, proj_in_new_basis) +
#              np.array([[v2[0]], [v2[1]], [v2[2]]]))).flatten().tolist()
#     return proj


# def internal_angles_mesh(cellygon_mesh, background=0, mode='project'):
#     neighs = get_connected_vertices_all(cellygon_mesh, include_self=False)
#     cells = np.unique(cellygon_mesh['cell_id'])

#     points = cellygon_mesh.points
#     faces = cellygon_mesh.faces.reshape((-1, 4))[:, 1:]
#     faces_cell_ids = np.c_[cellygon_mesh['cell_id'],
#                            cellygon_mesh['cell_id'],
#                            cellygon_mesh['cell_id']]

#     all_angles = []
#     for cell in cells:
#         cell_faces = faces[np.all(faces_cell_ids == cell, 1)]
#         vids, cts = np.unique(cell_faces, return_counts=True)

#         # TODO remove indices that are in all, rather than max
#         vids = np.delete(vids, np.argmax(cts))  # don't consider center

#         for vid in vids:
#             v_neighs = points[neighs[vid][np.isin(neighs[vid], vids)]]
#             phi = angle(v_neighs[0], points[vid], v_neighs[1])
#             all_angles.append([cell, vid, phi])
#     all_angles = np.array(all_angles)
#     return all_angles

# def internal_angles(j_indices, j_neighs, edges, cells=None, background=0, mode='project'):
#     poly = create_polydata(j_indices, edges)
#     neighs = get_connected_vertices_all(poly, include_self=False)

#     if cells is None:
#         # TODO: write convenience function for this
#         _, _, cells = center_triangulation(j_indices, j_neighs, background)
#         cells = np.unique(cells)

#     output = []
#     for ii, cell in enumerate(np.unique(cells)):
#         for jj in np.where(np.array([any(jn == cell) for jn in j_neighs]))[0]:
#             v_neighs = [nn for nn in neighs[jj]]
#             v_neighs_in_cell = [vv for vv in v_neighs if cell in j_neighs[vv]]
#             n_neighs, n_neighs_in_cell = len(v_neighs), len(v_neighs_in_cell)

#             if n_neighs_in_cell != 2:
#                 print(
#                     'Warning: vertex {ii} has too many neighbours in the same cell. Ignoring...')
#                 continue
#             v1 = j_indices[v_neighs_in_cell[0]] - j_indices[jj]
#             v1 = v1 / np.linalg.norm(v1)
#             v2 = j_indices[v_neighs_in_cell[1]] - j_indices[jj]
#             v2 = v2 / np.linalg.norm(v2)
#             phi = np.arccos(np.dot(v1, v2)) / (2 * np.pi) * 360
#             output.append(
#                 (cell, jj, v_neighs_in_cell[0], v_neighs_in_cell[1], phi, n_neighs))
#     output = np.asarray(output)
#     return output


# def merge_triangles(j_indices, j_neighs, threshold=None):
#     iteration = 0
#     while True:
#         print(iteration)
#         iteration += 1

#         init_len = j_indices.shape[0]
#         edges = find_edges(j_indices, j_neighs)

#         G = nx.Graph()
#         G.add_edges_from(edges)
#         cliques = nx.find_cliques(G)
#         cliques = np.asarray([qq for qq in cliques if len(qq) == 3])

#         areas = triangle_area(j_indices[cliques])
#         to_remove = []
#         for ii, qq in enumerate(cliques):
#             if threshold is not None and areas[ii] < threshold:
#                 continue
#             j_indices[qq[0]] = np.mean(j_indices[qq], 0)
#             j_neighs[qq[0]] = np.unique(np.hstack(j_neighs[qq]))
#             to_remove.extend(list(qq[1:]))
#         j_indices = j_indices[np.logical_not(
#             np.isin(np.arange(j_indices.shape[0]), to_remove))]
#         j_neighs = j_neighs[np.logical_not(
#             np.isin(np.arange(j_neighs.shape[0]), to_remove))]
#         j_indices, j_neighs = merge_similar_junctions(j_indices, j_neighs)

#         if init_len == j_indices.shape[0]:
#             break

#     return j_indices, j_neighs, edges
