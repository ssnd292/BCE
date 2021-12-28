import bpy

class MESH_OT_ClearCustomNormals(bpy.types.Operator):
    bl_idname = "mesh.bce_clearnormals"
    bl_label = "Clear Custom Normals"
    bl_description = "Clears Custome Normals of Selected Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def reset_normals(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            bpy.context.view_layer.objects.active = o
            if o.type  in ['MESH']:
                bpy.ops.mesh.customdata_custom_splitnormals_clear()

    def execute(self, context):
        self.reset_normals(context)
        return{'FINISHED'}

class MESH_OT_MakeTrisToQuads(bpy.types.Operator):
    bl_idname = "mesh.bce_tristoquads"
    bl_label = "Tris To Quads"
    bl_description = "Removes Triangulation"
    bl_options = {'REGISTER', 'UNDO'}

    def tristoquads(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type  in ['MESH']:
                bpy.ops.object.mode_set(mode='EDIT', toggle=False)
                bpy.ops.mesh.select_all(action='SELECT')
                selection = bpy.context.selected_objects
                bpy.ops.mesh.tris_convert_to_quads(uvs=True)
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    def execute(self, context):
        self.tristoquads(context)
        return{'FINISHED'}

class MESH_OT_MakeSingleUserObjectData(bpy.types.Operator):
    bl_idname = "mesh.bce_makesingleuser"
    bl_label = "Make Single User"
    bl_description = "Makes Object and Data Single User"
    bl_options = {'REGISTER', 'UNDO'}

    def makesingleuser(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
    def execute(self, context):
        self.makesingleuser(context)
        return{'FINISHED'}

class MESH_OT_ResetScaleForLinkedObjects(bpy.types.Operator):
    bl_idname = "mesh.bce_resetscale"
    bl_label = "Reset Scale for Linked Objects"
    bl_description = "Resets Data Links and Scale and Relinks Data"
    bl_options = {'REGISTER', 'UNDO'}

    def resetscalandrelink(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                bpy.ops.object.select_linked(type='OBDATA')
                bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                bpy.ops.object.make_links_data(type='OBDATA')
    def execute(self, context):
        self.resetscalandrelink(context)
        return{'FINISHED'}


class MESH_OT_ConvertHardEdgesToSeams(bpy.types.Operator):
    bl_idname = "mesh.bce_hardedgestoseams"
    bl_label = "Create Seams"
    bl_description = "Create Seams from Selected Hard Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def hardedgestoseams(self, context):
        bpy.ops.mesh.select_similar(type='SHARP', threshold=0.01)
        bpy.ops.mesh.mark_seam(clear=False)
    def execute(self, context):
        self.hardedgestoseams(context)
        return{'FINISHED'}

class MESH_OT_AddFWNModifier(bpy.types.Operator):
    bl_idname = "mesh.bce_addfwnmodifier"
    bl_label = "Adds FWVN Modifier"
    bl_description = "Addes Weighted Vertex Modifier with preset Settings"
    bl_options = {'REGISTER', 'UNDO'}

    def addfwnmodifier(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
                bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True
                bpy.context.object.modifiers["WeightedNormal"].weight = 100

    def execute(self, context):
        self.addfwnmodifier(context)
        return{'FINISHED'}

class MESH_OT_AddTriModifier(bpy.types.Operator):
    bl_idname = "mesh.bce_addtrimodifier"
    bl_label = "Adds Triangulate Modifier"
    bl_description = "Triangulates Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def addtrimodifier(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.ml_modifier_add(modifier_type="TRIANGULATE")
                bpy.context.object.modifiers["Triangulate"].keep_custom_normals = True

    def execute(self, context):
        self.addtrimodifier(context)
        return{'FINISHED'}

class MESH_OT_AddMirror(bpy.types.Operator):
    bl_idname = "mesh.bce_addmirror"
    bl_label = "Adds Mirror Modifier"
    bl_description = "Mirrors Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def addmirror(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                
                bpy.ops.object.ml_modifier_add(modifier_type="MIRROR")
                mirrorHelper = bpy.context.scene.objects.get("MirrorHelper")
                if mirrorHelper:
                    bpy.context.object.modifiers["Mirror"].mirror_object = bpy.data.objects["MirrorHelper"]
                else:
                    tempSelectedObject = bpy.context.view_layer.objects.active
                    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                    for obj in bpy.context.selected_objects:
                         obj.name = "MirrorHelper"
                    bpy.context.view_layer.objects.active = tempSelectedObject
                    bpy.context.object.modifiers["Mirror"].mirror_object = bpy.data.objects["MirrorHelper"]


    def execute(self, context):
        self.addmirror(context)
        return{'FINISHED'}

class MESH_OT_AddSmoothing(bpy.types.Operator):
    bl_idname = "mesh.bce_addsmoothing"
    bl_label = "Adds FWVN Modifier"
    bl_description = "Adds Weighted Vertex Modifier with preset Settings"
    bl_options = {'REGISTER', 'UNDO'}

    def addsmoothing(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.shade_smooth()
                bpy.ops.hops.soft_sharpen(auto_smooth_angle=2.0944, is_global=True)
    def execute(self, context):
        self.addsmoothing(context)
        return{'FINISHED'}

class MESH_OT_DeleteLinkedObjects(bpy.types.Operator):
    bl_idname = "mesh.bce_deletelinkedobjects"
    bl_label = "Deleted Linked Objects but Active"
    bl_description = "Deleted Linked Objects but Active"
    bl_options = {'REGISTER', 'UNDO'}

    def deletelinkedobjects(self, context):
        bpy.ops.object.select_linked(type='OBDATA')
        bpy.context.active_object.select_set(False)
        bpy.ops.object.delete(use_global=False, confirm=False)

    def execute(self, context):
        self.deletelinkedobjects(context)
        return{'FINISHED'}

class MESH_OT_RenameUVMaps(bpy.types.Operator):
    bl_idname = "mesh.bce_renameuvmaps"
    bl_label = "Renames UV Maps of Selected Objects"
    bl_description = "Renames UV Maps to UVMap of all Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def renameuvmaps(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                if bpy.context.object.data.uv_layers:
                    bpy.context.view_layer.objects.active.data.uv_layers[0].name = "UVMap"
                else:
                    bpy.ops.mesh.uv_texture_add()

    def execute(self, context):
        self.renameuvmaps(context)
        return{'FINISHED'}


class MESH_OT_TransferUVMaps(bpy.types.Operator):
    bl_idname = "mesh.bce_transferuvmaps"
    bl_label = "Transfers UVMaps"
    bl_description = "Transfers UVMap from Active to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def transferuvmaps(self, context):
        bpy.ops.object.data_transfer(data_type='UV', use_create=True, loop_mapping='POLYINTERP_LNORPROJ', poly_mapping='NORMAL', use_object_transform=True, ray_radius=0.01, islands_precision=0.5)
            
    def execute(self, context):
        self.transferuvmaps(context)
        return{'FINISHED'}

class MESH_OT_AddSecondUV(bpy.types.Operator):
    bl_idname = "mesh.bce_addseconduv"
    bl_label = "Adds Second UVMap"
    bl_description = "Add Second UVMap to all Selected Objects if they only have one"
    bl_options = {'REGISTER', 'UNDO'}

    def addseconduv(self, context):
        selection = bpy.context.selected_objects
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH'] and len(bpy.context.object.data.uv_layers) == 1:
                bpy.ops.mesh.uv_texture_add()
            
    def addseconduv(self, context):
        self.transferuvmaps(context)
        return{'FINISHED'}