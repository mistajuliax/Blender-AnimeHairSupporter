import bpy

from . import _common


class ahs_tapercurve_id_singlize(bpy.types.Operator):
    bl_idname = 'object.ahs_tapercurve_id_singlize'
    bl_label = "? Taper / Bevel single user"
    bl_description = "? If there are multiple taper / bevel references, duplicate and assign each "
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            taper_and_bevel_counts = {ob: 0 for ob in context.blend_data.objects}
            for ob in context.blend_data.objects:
                if ob.type != 'CURVE':
                    continue

                if ob.data.taper_object:
                    taper_and_bevel_counts[ob.data.taper_object] += 1
                if ob.data.bevel_object:
                    taper_and_bevel_counts[ob.data.bevel_object] += 1

            for ob in context.selected_objects:
                if taper_and_bevel_counts[ob] >= 2:
                    return True
                if (
                    ob.data.taper_object
                    and taper_and_bevel_counts[ob.data.taper_object] >= 2
                ):
                    return True
                if (
                    ob.data.bevel_object
                    and taper_and_bevel_counts[ob.data.bevel_object] >= 2
                ):
                    return True
            return False
        except:
            return False
        return True

    def execute(self, context):
        targets = {}
        for ob in context.selected_objects:
            if ob.type != 'CURVE':
                continue
            targets[ob] = []
            if ob.data.taper_object:
                targets[ob.data.taper_object] = []
            if ob.data.bevel_object:
                targets[ob.data.bevel_object] = []

        is_tapers = {}
        for ob in context.blend_data.objects:
            if ob.type != 'CURVE':
                continue

            if ob.data.taper_object:
                for key in targets:
                    if ob.data.taper_object == key:
                        targets[key].append(ob)
                        is_tapers[key] = True

            if ob.data.bevel_object:
                for key in targets:
                    if ob.data.bevel_object == key:
                        targets[key].append(ob)
                        is_tapers[key] = False

        for ob, parents in targets.items():
            if len(parents) < 2:
                continue

            for index, parent in enumerate(parents):
                if index == 0:
                    new_ob, new_curve = ob, ob.data
                else:
                    new_ob, new_curve = ob.copy(), ob.data.copy()
                    new_ob.data = new_curve
                    _common.link_to_scene(new_ob)

                if is_tapers[ob]:
                    parent.data.taper_object = new_ob
                else:
                    parent.data.bevel_object = new_ob

                _common.relocation_taper_and_bevel(parent, new_ob, is_tapers[ob])

        return {'FINISHED'}
