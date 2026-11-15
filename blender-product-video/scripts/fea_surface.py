# Turns a text-to-cad FEA result.vtu into the outer surface Blender needs (fea_to_blend.py).
# usage: cad run --with meshio fea_surface.py <result.vtu> <out.npz>
import sys, numpy as np, meshio
src, out = sys.argv[1:3]
m = meshio.read(src)
tet = np.vstack([c.data[:, :4] for c in m.cells if c.type.startswith('tetra')])
faces = np.vstack([tet[:, [0, 2, 1]], tet[:, [0, 1, 3]], tet[:, [1, 2, 3]], tet[:, [0, 3, 2]]])
key = np.sort(faces, axis=1)
_, idx, cnt = np.unique(key, axis=0, return_index=True, return_counts=True)
surf = faces[idx[cnt == 1]]  # a face only one tetra owns is on the outside
used = np.unique(surf)
remap = np.full(len(m.points), -1); remap[used] = np.arange(len(used))
np.savez(out, points=m.points[used], faces=remap[surf], von_mises=m.point_data['von_mises'][used],
         displacement=m.point_data['displacement'][used])
print(f"SURFACE {len(used)} vertici, {len(surf)} triangoli, picco {m.point_data['von_mises'].max():.1f} MPa")
