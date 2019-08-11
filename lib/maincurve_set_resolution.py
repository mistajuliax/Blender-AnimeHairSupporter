import bpy

from . import _common


class ahs_maincurve_set_resolution(bpy.types.Operator):
    bl_idname = 'object.ahs_maincurve_set_resolution'
    bl_label = "Change Resolution"
    bl_description = "Set the number of subdivisions of the Curve"
    bl_options = {'REGISTER', 'UNDO'}

    value = bpy.props.IntProperty(name="value", default=12, min=-64, max=64, soft_min=-64, soft_max=64)

    items = [
        ('ABSOLUTE', "Absolute", "", 'PREFERENCES', 1),
        ('RELATIVE', "Relative", "", 'ZOOMIN', 2),
    ]
    mode = bpy.props.EnumProperty(items=items, name="Mode", default='ABSOLUTE')

    @classmethod
    def poll(cls, context):
        try:
            for ob in context.selected_objects:
                if ob.type != 'CURVE':
                    continue
                break
            else:
                return False
        except:
            return False
        return True

    def invoke(self, context, event):
        try:
            self.value = _common.get_active_object().data.splines.active.resolution_u
        except:
            pass
        return self.execute(context)

    def execute(self, context):
        for ob in context.selected_objects:
            if ob.type != 'CURVE':
                continue
            for spline in ob.data.splines:
                if self.mode == 'ABSOLUTE':
                    spline.resolution_u = self.value
                if self.mode == 'RELATIVE':
                    spline.resolution_u += self.value
        return {'FINISHED'}
