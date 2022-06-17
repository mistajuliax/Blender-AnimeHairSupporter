import bpy

from . import _common


class ahs_maincurve_set_order(bpy.types.Operator):
    bl_idname = 'object.ahs_maincurve_set_order'
    bl_label = "Change order"
    bl_description = "? Set the order (granuality) of selected curves all at once"
    bl_options = {'REGISTER', 'UNDO'}

    value = bpy.props.IntProperty(name="値", default=3, min=-6, max=6, soft_min=-6, soft_max=6)

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
            self.value = _common.get_active_object().data.splines.active.order_u
        except:
            pass
        return self.execute(context)

    def execute(self, context):
        for ob in context.selected_objects:
            if ob.type != 'CURVE':
                continue
            for spline in ob.data.splines:
                if self.mode == 'ABSOLUTE':
                    spline.order_u = self.value
                elif self.mode == 'RELATIVE':
                    spline.order_u += self.value
        return {'FINISHED'}
