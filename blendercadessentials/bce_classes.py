import bpy
from random import sample
from random import uniform

#########################################
## Modelling
#########################################
uvLengthOld = 0
uvLengthNew = 0

def selectionCheck(self, selectionCount):
    if len(selectionCount) == 0:
        self.report({'INFO'}, 'You have nothing selected to perform this action.')

class BCE_OT_ClearCustomNormals(bpy.types.Operator):
    bl_idname = "mesh.bce_clearnormals"
    bl_label = "Clear Custom Normals"
    bl_description = "Clears Custome Normals of Selected Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    def reset_normals(self, context):        
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)

        for o in selection:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            bpy.context.view_layer.objects.active = o
            if o.type  in ['MESH']:
                bpy.ops.mesh.customdata_custom_splitnormals_clear()

    def execute(self, context):
        self.reset_normals(context)
        return{'FINISHED'}

class BCE_OT_MakeTrisToQuads(bpy.types.Operator):
    bl_idname = "mesh.bce_tristoquads"
    bl_label = "Tris To Quads"
    bl_description = "Removes Triangulation"
    bl_options = {'REGISTER', 'UNDO'}

    def tristoquads(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
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

class BCE_OT_MakeSingleUserObjectData(bpy.types.Operator):
    bl_idname = "mesh.bce_makesingleuser"
    bl_label = "Make Single User"
    bl_description = "Makes Object and Data Single User"
    bl_options = {'REGISTER', 'UNDO'}

    def makesingleuser(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
    def execute(self, context):
        self.makesingleuser(context)
        return{'FINISHED'}

class BCE_OT_ResetScaleForLinkedObjects(bpy.types.Operator):
    bl_idname = "mesh.bce_resetscale"
    bl_label = "Reset Scale for Linked Objects"
    bl_description = "Resets Data Links and Scale and Relinks Data"
    bl_options = {'REGISTER', 'UNDO'}

    def resetscalandrelink(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                bpy.ops.object.select_linked()
                bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                bpy.ops.object.make_links_data()
    def execute(self, context):
        self.resetscalandrelink(context)
        return{'FINISHED'}

class BCE_OT_ChangedNumberOfLinkedObjects(bpy.types.Operator):
    bl_idname = "mesh.bce_changenumberoflinkedobjects"
    bl_label = "Reset Scale for Linked Objects"
    bl_description = "Resets Data Links and Scale and Relinks Data"
    bl_options = {'REGISTER', 'UNDO'}

    def changenumberoflinkedobjects(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        bceprops = context.scene.bceprops
        maxObjNumber = bceprops.maxObjectNumber
        divider = bceprops.commonDenominatorInt
       
        if maxObjNumber == 0:
            maxObjNumber = len(selection)
            bceprops.maxObjectNumber = maxObjNumber
        
        numberOfSelections = maxObjNumber/divider
        print("Number of Objects to Select: "+ str(numberOfSelections))

        if ".0" in str(numberOfSelections):
            newSelection = sample(selection, int(numberOfSelections))
            print("Number of selected Objects: "+ str(len(newSelection)))
            bpy.ops.object.select_all(action='DESELECT')

            for o in newSelection:
                o.select_set(True)

            for o in newSelection:
                bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
                bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)
                bpy.ops.object.make_links_data(type='OBDATA')

        else:
            self.report({'WARNING'}, 'Your Number is not a Denominator of the whole Object Amount!')

    def execute(self, context):
        self.changenumberoflinkedobjects(context)
        return{'FINISHED'}

class BCE_OT_ResetNumberCounter(bpy.types.Operator):
    bl_idname = "mesh.bce_resetnumbercounter"
    bl_label = "Reset Scale for Linked Objects"
    bl_description = "Resets Data Links and Scale and Relinks Data"
    bl_options = {'REGISTER', 'UNDO'}

    def resetnumbercounter(self, context):
        bceprops = context.scene.bceprops
        bceprops.maxObjectNumber = 0
    def execute(self, context):
        self.resetnumbercounter(context)
        return{'FINISHED'}


class BCE_OT_AddFWNModifier(bpy.types.Operator):
    bl_idname = "mesh.bce_addfwnmodifier"
    bl_label = "Adds FWVN Modifier"
    bl_description = "Addes Weighted Vertex Modifier with preset Settings"
    bl_options = {'REGISTER', 'UNDO'}

    def addfwnmodifier(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
                bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True
                bpy.context.object.modifiers["WeightedNormal"].weight = 100

    def execute(self, context):
        self.addfwnmodifier(context)
        return{'FINISHED'}

class BCE_OT_AddTriModifier(bpy.types.Operator):
    bl_idname = "mesh.bce_addtrimodifier"
    bl_label = "Adds Triangulate Modifier"
    bl_description = "Triangulates Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def addtrimodifier(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.ml_modifier_add(modifier_type="TRIANGULATE")
                bpy.context.object.modifiers["Triangulate"].keep_custom_normals = True

    def execute(self, context):
        self.addtrimodifier(context)
        return{'FINISHED'}

class BCE_OT_AddMirror(bpy.types.Operator):
    bl_idname = "mesh.bce_addmirror"
    bl_label = "Adds Mirror Modifier"
    bl_description = "Mirrors Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def addmirror(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        bceprops = context.scene.bceprops
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                
                bpy.ops.object.modifier_add(type='MIRROR')
                latestModifier = len(o.modifiers)-1
                bpy.context.object.modifiers[latestModifier].name = "BCE_Mirror"                

                if bceprops.boolMirrorMoveUV == True:
                    bpy.context.object.modifiers[latestModifier].offset_u = 1
                if bceprops.boolUseMirrorHelper:
                    mirrorHelper = bpy.context.scene.objects.get("MirrorHelper")
                    if mirrorHelper:
                        bpy.context.object.modifiers[latestModifier].mirror_object = bpy.data.objects["MirrorHelper"]
                    else:
                        tempSelectedObject = bpy.context.view_layer.objects.active
                        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        for obj in bpy.context.selected_objects:
                            obj.name = "MirrorHelper"
                        bpy.context.view_layer.objects.active = tempSelectedObject
                        bpy.context.object.modifiers[latestModifier].mirror_object = bpy.data.objects["MirrorHelper"]
                

    def execute(self, context):
        self.addmirror(context)
        return{'FINISHED'}

class BCE_OT_SetHOPsSharpness(bpy.types.Operator):
    bl_idname = "mesh.bce_set_hopssharpness"
    bl_label = "Overrides HardOps Global Sharpness Angle"
    bl_description = "Overrides Hardops Sharpness Angle"

    def execute(self, context):
        angle = context.scene.bceprops.floatSmoothing
        bpy.context.preferences.addons["HOps"].preferences.property.sharpness = angle
        return {"FINISHED"}

class BCE_OT_AddSmoothing(bpy.types.Operator):
    bl_idname = "mesh.bce_addsmoothing"
    bl_label = "Adds HOps SSharpen"
    bl_description = "Uses HOps SSharpen"
    bl_options = {'REGISTER', 'UNDO'}

    def addsmoothing(self, context):        
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        bpy.ops.mesh.bce_set_hopssharpness()
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                bpy.ops.object.shade_smooth()
                bpy.ops.hops.sharpen(behavior='SSHARP', mode='SSHARP', additive_mode=True, auto_smooth_angle=3.14159, is_global=True)


    def execute(self, context):
        self.addsmoothing(context)
        return{'FINISHED'}

class BCE_OT_LocalRandomRotate(bpy.types.Operator):
    bl_idname = "mesh.bce_localrandomrotate"
    bl_label = "Rotates Randomly Locally"
    bl_description = "Randomly Rotates selected objects locally"
    bl_options = {'REGISTER', 'UNDO'}

    def localrandomrotate(self, context):        
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        rotateAngle = context.scene.bceprops.maxRandomRotate
        rotateAxis = context.scene.bceprops.axisRandomRotate

        bpy.ops.mesh.bce_set_hopssharpness()
        print("Returning to Setting HOps Sharpen")
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                actualAngle = uniform(-rotateAngle,rotateAngle)
                o.rotation_euler.rotate_axis(rotateAxis, actualAngle)

    def execute(self, context):
        self.localrandomrotate(context)
        return{'FINISHED'}

#########################################
## Unwrapping
#########################################

class BCE_OT_ConvertHardEdgesToSeams(bpy.types.Operator):
    bl_idname = "mesh.bce_hardedgestoseams"
    bl_label = "Create Seams"
    bl_description = "Create Seams from Selected Hard Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def hardedgestoseams(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)        
        for o in selection:
            current_mode = o.mode
            if current_mode == "EDIT":
                if bpy.context.active_object.data.total_edge_sel == 1:
                    try:
                        bpy.ops.mesh.select_similar(type='SHARP', threshold=0.01)
                        bpy.ops.mesh.mark_seam(clear=False)
                    except:
                        self.report({'ERROR'}, 'You need to select an Edge!')
                else:
                    self.report({'ERROR'}, 'You need to select an Edge!')
            else:
                self.report({'ERROR'}, 'You need to select an Edge!')
    def execute(self, context):
        self.hardedgestoseams(context)
        return{'FINISHED'}

class BCE_OT_SelectUVMap(bpy.types.Operator):
    bl_idname = "mesh.bce_selectuvmap"
    bl_label = "Select UVMap 01"
    bl_description = "Selects First UVMap"
    bl_options = {'REGISTER', 'UNDO'}

    def selectuvmap01(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        selectedUV = context.scene.bceprops.uvMapEnum
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                o.data.uv_layers.active_index =  int(selectedUV)

    def execute(self, context):
        self.selectuvmap01(context)
        return{'FINISHED'}


class BCE_OT_RenameUVMaps(bpy.types.Operator):
    bl_idname = "mesh.bce_renameuvmaps"
    bl_label = "Renames Active UV Maps of Selected Objects"
    bl_description = "Renames Active UV Maps of all Selected Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def renameuvmaps(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        newUVMapName = context.scene.bceprops.stringUVMapName
        for o in selection:
            bpy.context.view_layer.objects.active = o
            if o.type in ['MESH']:
                uvLayers = bpy.context.object.data.uv_layers
                currentUVMap = uvLayers.active_index
                if uvLayers:
                    if uvLayers[currentUVMap].name == newUVMapName:
                        self.report({'ERROR'}, 'A UVMap with that Name already exists.')
                    else:
                        uvLayers[currentUVMap].name = newUVMapName
                else:
                    bpy.ops.mesh.uv_texture_add()
                    if uvLayers[currentUVMap].name == newUVMapName:
                        self.report({'ERROR'}, 'A UVMap with that Name already exists.')
                    else:
                        uvLayers[currentUVMap].name = newUVMapName
                    

    def execute(self, context):
        self.renameuvmaps(context)
        return{'FINISHED'}


class BCE_OT_TransferUVMaps(bpy.types.Operator):
    bl_idname = "mesh.bce_transferuvmaps"
    bl_label = "Transfers UVMaps"
    bl_description = "Transfers UVMap from Active to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def transferuvmaps(self, context):
        selection = bpy.context.selected_objects        
        if len(selection) > 0:
            if len(selection) == 2:
                bpy.ops.object.data_transfer(data_type='UV', use_create=True, loop_mapping='POLYINTERP_LNORPROJ', poly_mapping='NORMAL', use_object_transform=True, ray_radius=0.01, islands_precision=0.5)
            else:
                self.report({'ERROR'}, 'You need to select at least two Objects!')
        else:
            selectionCheck(self,selection)
            
    def execute(self, context):
        self.transferuvmaps(context)
        return{'FINISHED'}

class BCE_OT_AddUVMap(bpy.types.Operator):
    bl_idname = "mesh.bce_adduvmap"
    bl_label = "Adds UVMap"
    bl_description = "Adds another UVMap to all Selected Objects."
    bl_options = {'REGISTER', 'UNDO'}

    def adduvmap(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        for o in selection:
            bpy.context.view_layer.objects.active = o
            uvLengthOld = len(bpy.context.object.data.uv_layers)
            if o.type in ['MESH'] and len(bpy.context.object.data.uv_layers) > 0 and uvLengthNew != uvLengthOld:
                bpy.ops.mesh.uv_texture_add()
                uvLengthNew = len(bpy.context.object.data.uv_layers)
            
    def execute(self, context):
        self.adduvmap(context)
        return{'FINISHED'}

class BCE_OT_RemoveSelectedUVMap(bpy.types.Operator):
    bl_idname = "mesh.bce_removeselecteduvmap"
    bl_label = "Removes Selected UVMap"
    bl_description = "Removes Selected UVMap from all selected objects."
    bl_options = {'REGISTER', 'UNDO'}

    def removeselecteduvmap(self, context):
        selection = bpy.context.selected_objects
        selectionCheck(self,selection)
        for o in selection:
            bpy.context.view_layer.objects.active = o
            uvLengthOld = len(bpy.context.object.data.uv_layers)
            if o.type in ['MESH'] and len(bpy.context.object.data.uv_layers) > 0 and uvLengthNew != uvLengthOld:
                bpy.ops.mesh.uv_texture_remove()
                uvLengthNew = len(bpy.context.object.data.uv_layers)
            
    def execute(self, context):
        self.removeselecteduvmap(context)
        return{'FINISHED'}

#########################################
## Misc
#########################################

class BCE_OT_DeleteLinkedObjects(bpy.types.Operator):
    bl_idname = "mesh.bce_deletelinkedobjects"
    bl_label = "Deleted Linked Objects but Active"
    bl_description = "Deleted Linked Objects but Active"
    bl_options = {'REGISTER', 'UNDO'}

    def deletelinkedobjects(self, context):
        bpy.ops.object.select_linked()
        bpy.context.active_object.select_set(False)
        bpy.ops.object.delete(use_global=False, confirm=False)

    def execute(self, context):
        self.deletelinkedobjects(context)
        return{'FINISHED'}