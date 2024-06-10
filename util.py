import pandas as pd
import trimesh


def extract_domain_from_heart_geometry(torso_pts, torso_uvc, biv_elem):
    TRI_COL = ['a', 'b', 'c']
    # extract surface
    faces = pd.DataFrame({
        'a': pd.concat([biv_elem.a, biv_elem.a, biv_elem.a, biv_elem.b], ignore_index=True),
        'b': pd.concat([biv_elem.b, biv_elem.b, biv_elem.c, biv_elem.c], ignore_index=True),
        'c': pd.concat([biv_elem.c, biv_elem.d, biv_elem.d, biv_elem.d], ignore_index=True),
        'tag': pd.concat([biv_elem.tag, biv_elem.tag, biv_elem.tag, biv_elem.tag], ignore_index=True)
    })
    arr = faces[TRI_COL].values
    arr.sort(axis=1)
    faces[TRI_COL] = arr
    row_counts = faces.groupby(TRI_COL).size().reset_index(name='Frequency')
    single_faces = row_counts[row_counts.Frequency == 1].drop(['Frequency'], axis=1)
    faces = single_faces.join(faces.set_index(TRI_COL), on=TRI_COL, how='inner')
    mesh = trimesh.Trimesh(vertices=torso_pts.values, faces=faces[TRI_COL].values, process=False)
    mesh.fix_normals()
    faces[TRI_COL] = mesh.faces
    # assign scar tag of tetrahedron to pts by majority vote
    tag_counts = {i: {0: 0, 1400: 0, 1401: 0} for i in torso_pts.index}
    for _, tetra in biv_elem.iterrows():
        a, b, c, d, tag = tetra
        tag = int(tag)
        tag_counts[a][tag] += 1
        tag_counts[b][tag] += 1
        tag_counts[c][tag] += 1
        tag_counts[d][tag] += 1
    torso_pts['tag'] = [max(tag_counts[i], key=tag_counts[i].get) for i in torso_pts.index]
    # assign uvc to face
    a = pd.merge(torso_uvc, faces, how='inner', left_index=True, right_on=['a'])
    b = pd.merge(torso_uvc, faces, how='inner', left_index=True, right_on=['b'])
    c = pd.merge(torso_uvc, faces, how='inner', left_index=True, right_on=['c'])

    index = (a.transventricular + b.transventricular + c.transventricular) < 0
    faces.loc[index, 'transventricular'] = -1
    faces.loc[~index, 'transventricular'] = 1

    faces['transmural'] = (a.transmural + b.transmural + c.transmural) / 3
    faces['apicobasal'] = (a.apicobasal + b.apicobasal + c.apicobasal) / 3
    # filter indices based on lvendo
    lv = faces[faces.transventricular == -1]
    lvendo = lv[(lv.transmural < 0.1)]
    # filter out the scar core
    pace_surface = lvendo[lvendo.tag != 1400]
    heart_domain = pd.concat([pace_surface.a, pace_surface.b, pace_surface.c], axis=0).unique()
    heart_domain = [int(index) for index in heart_domain]

    return heart_domain
