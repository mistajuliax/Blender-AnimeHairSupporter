import bmesh
import bpy
import mathutils

from . import _common


class ahs_convert_edgemesh_to_curve(bpy.types.Operator):
    bl_idname = 'object.ahs_convert_edgemesh_to_curve'
    bl_label = "Edge Mesh > Curve"
    bl_description = "Convert selected edges to NURBS curve"
    bl_options = {'REGISTER', 'UNDO'}

    order_u = bpy.props.IntProperty(name="Degree", default=3, min=3, max=6, soft_min=3, soft_max=6)
    extra_deform_multi = bpy.props.IntProperty(name="Extra deformation", default=0, min=-100, max=200, soft_min=-100, soft_max=200, subtype='PERCENTAGE')
    is_remove_mesh = bpy.props.BoolProperty(name="Delete original Mesh", default=True)

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        self.layout.prop(self, 'order_u', slider=True)
        self.layout.prop(self, 'extra_deform_multi', slider=True)
        self.layout.prop(self, 'is_remove_mesh', icon='X', toggle=True)

    def execute(self, context):
        new_objects = []
        for ob in context.selected_objects[:]:
            _common.select(ob, False)
            if ob.type != 'MESH':
                continue
            if len(ob.data.vertices) < 2 or len(ob.data.edges) < 1 or len(ob.data.polygons):
                continue

            bm = bmesh.new()
            bm.from_mesh(ob.data)

            separated_verts = []
            already_edges = []
            for _ in range(len(bm.verts) * 2):
                # まだ拾ってない開始頂点/辺を検索
                current_vert, current_edge = None, None
                for vert in bm.verts:
                    # 繋がってる辺が2つは開始地点として不適切
                    if len(vert.link_edges) == 2:
                        continue
                    # まだ拾ってない辺を検索
                    for edge in vert.link_edges:
                        if edge in already_edges:
                            continue
                        # 変数に確保して離脱
                        current_vert, current_edge = vert, edge
                        break
                    if current_edge:
                        break
                # 離脱
                else:
                    break
                if not current_edge:
                    break

                # 辿っていく
                local_verts = [current_vert]
                for j in range(len(bm.verts) * 2):
                    # すでに拾ったもとと登録
                    already_edges.append(current_edge)
                    # 次の頂点を現在頂点に
                    current_vert = current_edge.other_vert(current_vert)
                    # ローカル結果にアペンド
                    local_verts.append(current_vert)
                    # 離脱
                    if len(current_vert.link_edges) != 2:
                        break
                    # 2つある辺の次にあたるのを現在辺に
                    for edge in current_vert.link_edges:
                        if edge != current_edge:
                            current_edge = edge
                            break
                # 離脱
                else:
                    break
                # 結果をアペンド
                separated_verts.append(local_verts)

            for local_verts in separated_verts:
                local_points = [_common.mul(ob.matrix_world, v.co) for v in local_verts]

                # グローバルZ軸が上の頂点を開始地点とする
                begin_co = local_points[0]
                end_co = local_points[-1]
                if begin_co.z < end_co.z:
                    local_verts.reverse(), local_points.reverse()

                # カーブとオブジェクトを新規作成してリンク
                name = f"{ob.name}:HairCurve"
                curve = context.blend_data.curves.new(name, 'CURVE')
                curve_ob = context.blend_data.objects.new(name, curve)
                curve_ob.matrix_world = mathutils.Matrix.Translation(local_points[0])
                _common.link_to_scene(curve_ob)
                new_objects.append(curve_ob)

                # カーブの設定
                curve.dimensions = '3D'

                # スプライン＆ポイントを作成
                spline = curve.splines.new('NURBS')
                spline.points.add(len(local_points) - 1)
                for index, (point, co) in enumerate(zip(spline.points, local_points)):
                    if index != 0 and len(local_points) - 1 != index:
                        prev_line = co - local_points[index - 1]
                        next_line = co - local_points[index + 1]
                        co += prev_line.lerp(next_line, 0.5) * (self.extra_deform_multi * 0.01)
                    point.co = list(_common.mul(curve_ob.matrix_world.inverted(), co)) + [1.0]

                # スプラインの設定
                spline.order_u = self.order_u
                spline.use_endpoint_u = True

            bm.free()

            if self.is_remove_mesh:
                context.blend_data.meshes.remove(ob.data, do_unlink=True)

        # 新規オブジェクトをアクティブ＆選択
        if len(new_objects):
            _common.set_active_object(new_objects[0])
        for new_object in new_objects:
            _common.select(new_object, True)

        return {'FINISHED'}
