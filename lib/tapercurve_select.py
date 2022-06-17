import bpy

from . import _common


class ahs_tapercurve_select(bpy.types.Operator):
    bl_idname = 'object.ahs_tapercurve_select'
    bl_label = "Select"
    bl_description = "Select all Taper/Bevel Curves"
    bl_options = {'REGISTER', 'UNDO'}

    items = [
        ('TAPER', "Taper", "", 'CURVE_NCURVE', 1),
        ('BEVEL', "Bevel", "", 'SURFACE_NCIRCLE', 2),
        ('BOTH', "Both", "", 'ARROW_LEFTRIGHT', 3),
    ]
    mode = bpy.props.EnumProperty(items=items, name="Mode", default='BOTH')

    @classmethod
    def poll(cls, context):
        try:
            taper_and_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object] + [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
            for ob in context.visible_objects:
                if ob in taper_and_bevel_objects:
                    break
            else:
                return False
        except:
            return False
        return True

    def execute(self, context):
        if self.mode == 'BEVEL':
            taper_or_bevel_objects = [c.bevel_object for c in context.blend_data.curves if c.bevel_object]
        elif self.mode == 'TAPER':
            taper_or_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object]
        else:
            taper_or_bevel_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object] + [c.bevel_object for c in context.blend_data.curves if c.bevel_object]

        target_objects = [
            ob for ob in context.visible_objects if ob in taper_or_bevel_objects
        ]

        if not len(target_objects):
            return {'FINISHED'}

        if _common.get_active_object() not in target_objects:
            target_objects.sort(key=lambda ob: ob.name)
            _common.set_active_object(target_objects[0])
        for ob in target_objects:
            _common.select(ob, True)
        return {'FINISHED'}
