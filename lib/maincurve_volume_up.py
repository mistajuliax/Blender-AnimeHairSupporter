import bpy
import mathutils
import math
import os
from . import _common


class ahs_maincurve_volume_up(bpy.types.Operator):
    bl_idname = 'object.ahs_maincurve_volume_up'
    bl_label = "Increase Volume"
    bl_description = "Increase Taper/Bevel of the Curve""
    bl_options = {'REGISTER', 'UNDO'}

    taper_type = bpy.props.EnumProperty(items=_common.get_taper_enum_items(), name="Taper", default='Tapered')

    bevel_type = bpy.props.EnumProperty(items=_common.get_bevel_enum_items(), name="Bevel", default='Sharp')
    is_bevel_mirror = bpy.props.BoolProperty(name="Flip Bevel Horizontally", default=False)

    scale = bpy.props.FloatProperty(name="Radius", default=0.2, min=0, max=10, soft_min=0, soft_max=10, step=0.1, precision=3)
    scale_y_multi = bpy.props.IntProperty(name="Flatness", default=50, min=0, max=100, soft_min=0, soft_max=100, subtype='PERCENTAGE')

    @classmethod
    def poll(cls, context):
        try:
            for ob in context.selected_objects:
                if ob.type == 'CURVE':
                    break
            else:
                return False
        except:
            return False
        return True

    def draw(self, context):
        self.layout.prop(self, 'taper_type')

        row = self.layout.row(align=True)
        row.prop(self, 'bevel_type')
        row.prop(self, 'is_bevel_mirror', text="", icon='MOD_MIRROR')

        self.layout.prop(self, 'scale')
        self.layout.prop(self, 'scale_y_multi', slider=True)

    def execute(self, context):
        # すでにテーパーかベベルとして指定されているオブジェクトをリスト
        taper_and_bevel_objects = [c.taper_object for c in context.blend_data.curves] + [c.bevel_object for c in context.blend_data.curves]

        blend_path = _common.get_append_data_blend_path()

        for ob in context.selected_objects:
            if ob in taper_and_bevel_objects:
                continue
            if ob.type != 'CURVE':
                continue

            curve = ob.data

            # すでにテーパーかベベルがあって参照が1つの場合は削除
            if curve.taper_object:
                if len([c.taper_object for c in context.blend_data.curves if c.taper_object == curve.taper_object]) == 1:
                    c = curve.taper_object
                    if c:
                        context.blend_data.curves.remove(c, do_unlink=True)
            if curve.bevel_object:
                if len([c.bevel_object for c in context.blend_data.curves if c.bevel_object == curve.bevel_object]) == 1:
                    c = curve.bevel_object
                    if c:
                        context.blend_data.curves.remove(c, do_unlink=True)

            # テーパーオブジェクトをアペンドして割り当て
            with context.blend_data.libraries.load(blend_path) as (data_from, data_to):
                data_to.objects = ["Taper." + self.taper_type]
            taper_curve_ob = data_to.objects[0]
            taper_curve = taper_curve_ob.data
            name = ob.name + ":Taper"
            taper_curve_ob.name, taper_curve.name = name, name
            _common.link_to_scene(taper_curve_ob)
            _common.select(taper_curve_ob, False)
            curve.taper_object = taper_curve_ob

            # ベベルオブジェクトをアペンドして割り当て
            with context.blend_data.libraries.load(blend_path) as (data_from, data_to):
                data_to.objects = ["Bevel." + self.bevel_type]
            bevel_curve_ob = data_to.objects[0]
            bevel_curve = bevel_curve_ob.data
            name = ob.name + ":Bevel"
            bevel_curve_ob.name, bevel_curve.name = name, name
            _common.link_to_scene(bevel_curve_ob)
            _common.select(bevel_curve_ob, False)
            curve.bevel_object = bevel_curve_ob
            # 左右反転処理
            if self.is_bevel_mirror:
                co_list = [list(p.co) for p in bevel_curve.splines[0].points]
                co_list.reverse()
                for point, new_co in zip(bevel_curve.splines[0].points, co_list):
                    new_co[0] = -new_co[0]
                    point.co = new_co

            _common.relocation_taper_and_bevel(ob, taper_curve_ob, True)
            _common.relocation_taper_and_bevel(ob, bevel_curve_ob, False)

            # 拡縮変更
            taper_curve_ob.scale = (self.scale, self.scale, self.scale)
            bevel_curve_ob.scale = (self.scale, self.scale * self.scale_y_multi * 0.01, self.scale)

        return {'FINISHED'}
