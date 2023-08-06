#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:08:33 2020

@author: henrikahl
"""

import argparse
import os
import re
import sys
from multiprocessing import Pool, cpu_count

import mahotas as mh
import numpy as np
import pandas as pd
import pyvista as pv
import tifffile as tiff
from imgmisc import (
    autocrop,
    circular_mask,
    find_neighbors,
    flatten,
    get_l1,
    get_l1_from_above,
    get_resolution,
    listdir,
    merge,
    mkdir,
    rand_cmap,
)
from scipy.ndimage import center_of_mass

import cellygon as cg

bname = lambda x: os.path.basename(os.path.splitext(x)[0])

parser = argparse.ArgumentParser(description="")

# Required positional argument
parser.add_argument("input", type=str, nargs="+", help="Input files or directory")
parser.add_argument(
    "--output", type=str, help="Output directory", default=f"{os.path.curdir}"
)

# Optional argument
parser.add_argument("--radius", type=float, default=None)
parser.add_argument("--center", type=float, nargs=3, default=None)

parser.add_argument("--background", type=int, default=0)
parser.add_argument("--delete", type=int, nargs="+", default=None)
parser.add_argument("--resolution", type=float, nargs=3, default=None)
parser.add_argument("--suffix", type=str, default="-refined")
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--skip_done", action="store_true")
parser.add_argument("--parallel_workers", type=int, default=1)

args = parser.parse_args()

if len(args.input) == 1 and os.path.isdir(os.path.abspath(args.input[0])):
    files = listdir(
        args.input[0], sorting="natural", include=[".tif", ".tiff", ".lsm", ".czi"]
    )
else:
    files = args.input
mkdir(args.output)


fname = files[0]


def run(fname):
    # Read in info
    infostr = (
        re.findall("(\d+)-(\S+)-(\S+)-plant_(\d+)-(\d+)h", fname)[0]
        if args.time
        else re.findall("(\d+)-(\S+)-(\S+)-plant_(\d+)", fname)[0]
    )
    if args.time:
        dataset, genotype, reporter, plant, time = infostr
        dataset, plant, time = int(dataset), int(plant), int(time)
    else:
        dataset, genotype, reporter, plant = infostr
        dataset, plant = int(dataset), int(plant)
    seg_img = tiff.imread(fname)
    resolution = np.asarray(get_resolution(fname))

    # Reduce the cells to look at
    if args.radius is not None:
        center = (
            args.center
            if not args.center is None
            else center_of_mass(seg_img != args.background)[1:]
        )

        mask1 = circular_mask(
            seg_img.shape[1],
            seg_img.shape[2],
            center=np.round(center / resolution)[1:][::-1].astype(int),
            radius=args.radius,
        )
        mask2 = circular_mask(
            seg_img.shape[1],
            seg_img.shape[2],
            center=np.round(center / resolution)[1:][::-1].astype(int),
            radius=args.radius - 1,
        )
        mask3 = np.logical_xor(mask1, mask2)
        border_cells = np.unique(seg_img[:, mask3])
        seg_img[:, ~mask1] = 0
        seg_img = autocrop(seg_img, 0, n=1, offset=1)
        l1 = get_l1_from_above(seg_img)
        l1 = [ll for ll in l1 if ll not in border_cells]
    else:
        l1 = get_l1(seg_img, background=args.background)

    # Generate meshes
    j_indices, j_neighs = cg.find_junctions(
        seg_img,
        background=args.background,
        merge_adjacent=False,
        resolution=args.resolution,
        threshold=3,
        include_set=l1,
    )
    j_indices, j_neighs = cg.merge_junctions_euclidean(
        j_indices, j_neighs, r=np.sqrt(3)
    )

    jbak, jnbak = j_indices.copy(), j_neighs.copy()
    j_indices, j_neighs = jbak, jnbak
    j_indices, j_neighs = cg.merge_similar_junctions(j_indices, j_neighs, threshold=4)
    j_indices, j_neighs, edges = cg.clean(j_indices, j_neighs)

    tri_j_indices, tri_faces, tri_face_cell_ids = cg.center_triangulation(
        j_indices, j_neighs, args.background
    )

    # TODO
    tripoly = cg.create_polydata(tri_j_indices, tri_faces, args.resolution)
    tripoly["cell_id"] = tri_face_cell_ids
    areas = np.asarray(
        [
            pv.PolyData(
                tripoly.extract_cells(tripoly["cell_id"] == lab).points,
                tripoly.extract_cells(tripoly["cell_id"] == lab).cells,
            ).area
            for lab in np.unique(tripoly["cell_id"])
        ]
    )
    tripoly["cell_area"] = np.zeros(tripoly.n_cells)
    for ii, cid in enumerate(np.unique(tripoly["cell_id"])):
        tripoly["cell_area"][tripoly["cell_id"] == cid] = areas[ii]

    if args.plot_result:
        p = pv.Plotter()
        p.add_mesh(tripoly, cmap="glasbey")
        p.show()

    tripoly.save(f"{args.output}/{bname(fname)}{args.suffix}.vtk")


if len(sys.argv) < 2:
    n_cores = cpu_count() - 1
else:
    n_cores = int(sys.argv[1])

# n_cores = 1
p = Pool(n_cores)
p.map(run, files)
p.close()
p.join()
