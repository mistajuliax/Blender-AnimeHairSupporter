import bpy

from . import _common


class ahs_maincurve_select(bpy.types.Operator):
    bl_idname = 'object.ahs_maincurve_select'
    bl_label = "Select Hair"
    bl_description = "Select all hair Curves excluding Taper/Bevel Curves"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            for ob in context.visible_objects:
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
        target_objects = []
        for ob in context.visible_objects:
            if ob.type != 'CURVE':
                continue
            if ob.data.taper_object and ob.data.bevel_object:
                target_objects.append(ob)
        if not len(target_objects):
            return {'FINISHED'}

        if context.active_object not in target_objects:
            target_objects.sort(key=lambda ob: ob.name)
            _common.set_active_object(target_objects[0])
        for ob in target_objects:
            _common.select(ob, True)
        return {'FINISHED'}
