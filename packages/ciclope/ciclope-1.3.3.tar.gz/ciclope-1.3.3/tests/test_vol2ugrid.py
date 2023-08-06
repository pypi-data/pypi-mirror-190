import sys
sys.path.append('/home/gianthk/PycharmProjects/recon_utils')
sys.path.append('/home/gianthk/PycharmProjects/CT2FE')

import recon_utils as ru
from old.pybonemorph import remove_unconnected

vs = 0.0606

input_file = '/home/gianthk/Data/2019.001.coop_TUberlin_simulierte_Mensch.iorig/trabecular_samples/trabecular_sample_mini3/2000L_crop_imgaussfilt_60micron_uint8_0000.tif'
data_3D = ru.read_tiff_stack(input_file)

# data_3D = data_3D[25:28, 25:28, 25:28]
data_3D = data_3D[20:40, 20:40, 20:40]

# apply threshold
BW = data_3D > 140

# detect isolated cluster
BW = remove_unconnected(BW)

# mask the voxel data
data_3D[BW==0] = 0

tmpfile = '/home/gianthk/PycharmProjects/CT2FE/input_templates/tmp_example01_comp_static_bone_matprop.inp'
matprop = {
            "file": ["/home/gianthk/PycharmProjects/CT2FE/material_properties/bone.inp"],
            "range": [[1, 250]]
           }

mesh, refnodes = src.ciclope.voxelFE.vol2ugrid(data_3D, 0.0606, refnodes=True, verbose=True)
src.ciclope.voxelFE.mesh2voxelfe(mesh, tmpfile, "pippo.inp", matprop, keywords=['NSET', 'ELSET', 'PROPERTY'], verbose=True)

# ciclope.voxelFE.vol2voxelfe(data_3D, tmpfile, 'pippo_vol2voxelFE.inp', matprop, ['NSET', 'ELSET', 'PROPERTY'], 0.0606, verbose=True)

#
# import ccx2paraview
# ccx2paraview.Converter('pippo.frd', ['vtk']).run()