import bpy

from . import _common


class VIEW3D_PT_tools_anime_hair_supporter(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = _common.region()
    bl_category = 'HairTools'
    bl_context = 'objectmode'
    bl_label = "AnimeHairSupport"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        props = context.scene.ahs_props

        # コンバーターズ
        column = self.layout.column(align=True)
        row = column.row(align=True)
        row.operator('object.ahs_convert_edgemesh_to_curve', icon='IPO_EASE_IN_OUT')
        row.enabled = bool(len([o for o in context.selected_objects if o.type == 'MESH']))
        row = column.row(align=True)
        row.operator('object.ahs_convert_curve_to_edgemesh', icon='IPO_CONSTANT')
        row.enabled = bool(len([o for o in context.selected_objects if o.type == 'CURVE']))

        # メインカーブ
        box = self.layout.box()
        row = box.row(align=True)
        row.prop(props, 'maincurve_expand', text="Hair Curve", icon='MOD_CURVE', emboss=False)
        row.operator('object.ahs_maincurve_activate', text="", icon='ZOOM_SELECTED')
        row.label(text="", icon='BLANK1')

        if props.maincurve_expand:
            # 肉付け関係
            row = box.row(align=True)
            row.operator('object.ahs_maincurve_volume_up', icon='MESH_CAPSULE')
            row.operator('object.ahs_maincurve_volume_down', text="", icon='X')

            column = box.column(align=True)
            # 余剰変形
            column.operator('object.ahs_maincurve_extra_deform', icon='PARTICLE_PATH')
            # グラデーションひねり
            column.operator('object.ahs_maincurve_gradation_tilt', icon='FORCE_MAGNETIC')

            # サブツール
            column = box.column(align=True)
            row = column.row(align=True)
            row.operator('object.ahs_maincurve_select', icon='RESTRICT_SELECT_OFF')
            row.operator('object.ahs_maincurve_hide', text="Show", icon='NONE').is_hide = False
            row.operator('object.ahs_maincurve_hide', text="Hide", icon='NONE').is_hide = True

            # 解像度
            row = column.row(align=True)

            # if context.active_object.data.taper_object and context.active_object.data.bevel_object and context.active_object.data.splines.active:
            #     is_successed = True
            # else:
            #     is_successed = False

            try:
                is_successed = context.active_object.data.taper_object and context.active_object.data.bevel_object and context.active_object.data.splines.active
            except:
                is_successed = False

            if is_successed:
                row.prop(context.active_object.data.splines.active, 'resolution_u', text="Resolution")
            else:
                row.label(text="Resolution:")

            row.operator('object.ahs_maincurve_set_resolution', text="", icon='PREFERENCES')

            # 次数
            row = column.row(align=True)

            # if context.active_object.data.taper_object and context.active_object.data.bevel_object and context.active_object.data.splines.active:
            #     is_successed = True
            # else:
            #     is_successed = False

            try:
                is_successed = context.active_object.data.taper_object and context.active_object.data.bevel_object and context.active_object.data.splines.active
            except:
                is_successed = False

            if is_successed:
                row.prop(context.active_object.data.splines.active, 'order_u', text="Order")
            else:
                row.label(text="Order:")

            row.operator('object.ahs_maincurve_set_order', text="", icon='PREFERENCES')

        # テーパーカーブ
        box = self.layout.box()
        row = box.row(align=True)
        row.prop(props, 'tapercurve_expand', text="Taper Curve", icon='CURVE_NCURVE', emboss=False)
        row.operator('object.ahs_tapercurve_activate', text="", icon='ZOOM_SELECTED').mode = 'TAPER'
        row.operator('object.ahs_tapercurve_id_singlize', text="", icon='COPY_ID')

        if props.tapercurve_expand:

            # 種類を変更とか
            row = _common.box_split(box, 0.6, False)
            op = row.operator('object.ahs_tapercurve_change_type', icon='HAND')
            op.is_taper, op.is_bevel = True, False
            op = row.operator('object.ahs_tapercurve_mirror', icon='MOD_MIRROR')
            op.mode, op.is_mirror_x, op.is_mirror_y = 'TAPER', False, True

            # 位置を再設定とか
            row = box.row(align=False)
            row.operator('object.ahs_tapercurve_relocation', icon='PARTICLE_TIP').mode = 'BOTH'
            row.operator('object.ahs_tapercurve_remove_alones', icon='X').mode = 'BOTH'

            # サブツール
            column = box.column(align=True)
            row = column.row(align=True)
            row.operator('object.ahs_tapercurve_select', icon='RESTRICT_SELECT_OFF').mode = 'TAPER'
            op = row.operator('object.ahs_tapercurve_hide', text="Show", icon='NONE')
            op.mode, op.is_hide = 'TAPER', False
            op = row.operator('object.ahs_tapercurve_hide', text="Hide", icon='NONE')
            op.mode, op.is_hide = 'TAPER', True

            # 解像度
            row = column.row(align=True)

            # if context.active_object in bpy.data.objects:
            #     if context.active_object.data.taper_object in bpy.data.objects:
            #         row.prop(context.active_object.data.taper_object.data.splines.active, 'resolution_u', text="Resolution")
            #         is_successed = True
            #     else:
            #         is_successed = False
            # else:
            #     is_successed = False

            try:
                row.prop(context.active_object.data.taper_object.data.splines.active, 'resolution_u', text="Resolution")
                is_successed = True
            except:
                is_successed = False

            if not is_successed:
                taper_objects = [c.taper_object for c in context.blend_data.curves if c.taper_object]

                # if context.active_objects in taper_objects:
                #     row.prop(context.active_object.data.splines.active, 'resolution_u', text="Resolution")
                #     is_successed = True
                # else:
                #     is_successed = False

                try:
                    if context.active_object in taper_objects:
                        row.prop(context.active_object.data.splines.active, 'resolution_u', text="Resolution")
                        is_successed = True
                except:
                    is_successed = False

            if not is_successed:
                row.label(text="Resolution:")
            row.operator('object.ahs_maincurve_set_resolution', text="", icon='PREFERENCES')

        # ベベルカーブ
        box = self.layout.box()
        row = box.row(align=True)
        row.prop(props, 'bevelcurve_expand', text="Bevel Curve", icon='SURFACE_NCIRCLE', emboss=False)
        row.operator('object.ahs_tapercurve_activate', text="", icon='ZOOM_SELECTED').mode = 'BEVEL'
        row.operator('object.ahs_tapercurve_id_singlize', text="", icon='COPY_ID')

        if props.bevelcurve_expand:

            # 種類を変更とか
            row = _common.box_split(box, 0.6, False)
            op = row.operator('object.ahs_tapercurve_change_type', icon='HAND')
            op.is_taper, op.is_bevel = False, True
            op = row.operator('object.ahs_tapercurve_mirror', icon='MOD_MIRROR')
            op.mode, op.is_mirror_x, op.is_mirror_y = 'BEVEL', True, False

            # 位置を再設定とか
            row = box.row(align=False)
            row.operator('object.ahs_tapercurve_relocation', icon='PARTICLE_TIP').mode = 'BOTH'
            row.operator('object.ahs_tapercurve_remove_alones', icon='X').mode = 'BOTH'

            # サブツール
            column = box.column(align=True)
            row = column.row(align=True)
            row.operator('object.ahs_tapercurve_select', icon='RESTRICT_SELECT_OFF').mode = 'BEVEL'
            op = row.operator('object.ahs_tapercurve_hide', text="Show", icon='NONE')
            op.mode, op.is_hide = 'BEVEL', False
            op = row.operator('object.ahs_tapercurve_hide', text="Hide", icon='NONE')
            op.mode, op.is_hide = 'BEVEL', True

            # 解像度
            row = column.row(align=True)

            # if context.active_object in bpy.data.objects:
            #     if context.active_object.data.bevel_object in bpy.data.objects:
            #         row.prop(context.active_object.data.bevel_object.data.splines.active, 'resolution_u', text="Resolution")
            #         is_successed = True
            #     else:
            #         is_successed = False
            # else:
            #     is_successed = False

            try:
                row.prop(context.active_object.data.bevel_object.data.splines.active, 'resolution_u', text="Resolution")
                is_successed = True
            except:
                is_successed = False

            if not is_successed:
                bevel_objects = [c.bevel_object for c in context.blend_data.curves if c.bevel_object]

                # if context.active_objects in bevel_objects:
                #         row.prop(context.active_object.data.splines.active, 'resolution_u', text="Resolution")
                #         is_successed = True
                # else:
                #     is_successed = False

                try:
                    if context.active_object in bevel_objects:
                        row.prop(context.active_object.data.splines.active, 'resolution_u', text="Resolution")
                        is_successed = True
                except:
                    is_successed = False

            if not is_successed:
                row.label(text="Resolution:")
            row.operator('object.ahs_maincurve_set_resolution', text="", icon='PREFERENCES')

        # コンバーターズ
        row = self.layout.row(align=True)
        row.operator('object.ahs_convert_curve_to_armature', icon='ARMATURE_DATA')
        row.enabled = bool(len([o for o in context.selected_objects if o.type == 'CURVE']))

        row = self.layout.row(align=True)
        row.operator('object.ahs_convert_curve_to_mesh', icon='MESH_UVSPHERE')

        for ob in context.selected_objects:
            if ob.type != 'CURVE':
                continue
            if ob.data.taper_object and ob.data.bevel_object:
                row.enabled = True
                break
        else:
            row.enabled = False
