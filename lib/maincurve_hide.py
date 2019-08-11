import bpy

from . import _common


class ahs_maincurve_hide(bpy.types.Operator):
    bl_idname = 'object.ahs_maincurve_hide'
    bl_label = "Hide"
    bl_description = "Hide/Show all hair Curves"
    bl_options = {'REGISTER', 'UNDO'}

    is_hide = bpy.props.BoolProperty(name="Hide")

    @classmethod
    def poll(cls, context):
        try:
            for ob in context.blend_data.objects:
                if ob.type != 'CURVE':
                    continue
                if ob.data.taper_object and ob.data.bevel_object:
                    break
            else:
                return False
        except:
            return False
        return True

    def execute(self, context):
        for ob in context.blend_data.objects:
            if ob.type != 'CURVE':
                continue
            if ob.data.taper_object and ob.data.bevel_object:
                _common.set_hide(ob, self.is_hide)
        return {'FINISHED'}
