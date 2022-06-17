import re

import bpy
import mathutils

from . import _common


class ahs_convert_curve_to_edgemesh(bpy.types.Operator):
    bl_idname = 'object.ahs_convert_curve_to_edgemesh'
    bl_label = "Curve > Edge Mesh"
    bl_description = "Convert NURBS curve to Edge Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            for ob in context.selected_objects:
                if ob.type != 'CURVE':
                    continue
                for spline in ob.data.splines:
                    if spline.type == 'NURBS':
                        return True
        except:
            return False
        return True

    def execute(self, context):
        name = _common.get_active_object().name
        if re_result := re.search(r'^(.+):HairCurve', name):
            name = re_result[1]

        new_verts, new_edges = [], []
        for ob in context.selected_objects[:]:
            _common.select(ob, False)
            if ob.type != 'CURVE':
                continue
            curve = ob.data

            splines = [
                s
                for s in curve.splines
                if s.type == 'NURBS' and len(s.points) >= 2
            ]

            if not len(splines):
                continue

            # テーパー/ベベルを完全削除
            if curve.taper_object:
                temp_ob = curve.taper_object
                context.blend_data.curves.remove(temp_ob.data, do_unlink=True)
            if curve.bevel_object:
                temp_ob = curve.bevel_object
                context.blend_data.curves.remove(temp_ob.data, do_unlink=True)

            # 頂点/辺情報を格納
            for spline in splines:
                for index, point in enumerate(spline.points):
                    if index >= 1:
                        new_edges.append((len(new_verts) - 1, len(new_verts)))
                    new_verts.append(_common.mul(ob.matrix_world, mathutils.Vector(point.co[:3])))

            context.blend_data.curves.remove(ob.data, do_unlink=True)

        me = context.blend_data.meshes.new(name)
        me.from_pydata(new_verts, new_edges, [])

        ob = context.blend_data.objects.new(name, me)
        _common.link_to_scene(ob)
        _common.select(ob, True)
        _common.set_active_object(ob)

        return {'FINISHED'}
