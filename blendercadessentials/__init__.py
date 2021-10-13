bl_info = {
    "name" : "Blender CAD Essentials",
    "author" : "Sebastian Schneider",
    "description" : "Collection of often needed tools when working with imported CAD Data",
    "blender" : (2, 93, 0),
    'version': (0, 0, 8),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.utils import register_class, unregister_class


class Blender_CAD_Essentials_Panel(bpy.types.Panel):
    bl_idname = "Essentials"
    bl_label = "Blender CAD Essentials"
    bl_category = "Item"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Pre Modelling:")
        row = layout.row(align=True)
        row.operator('mesh.bce_clearnormals' ,text="Reset Custom Normals")

        row = layout.row(align=True)
        row.operator('mesh.bce_tristoquads' ,text="Tris to Quads")

        row = layout.row(align=True)
        row.operator('mesh.bce_makesingleuser' ,text="Make Single User")

        row = layout.row(align=True)
        row.operator('mesh.bce_resetscale' ,text="Reset Scale of Links")

        ##
        layout.separator()
        ##

        layout.label(text="Smoothing & Unwrapping:")
        #row = layout.row(align=True) 
        #row.prop(get_preferences().property, "sharpness", text="Sharpness")
        row = layout.row(align=True)        
        row.operator('mesh.bce_addsmoothing' ,text="HardOps Sharpen")

        row = layout.row(align=True)
        row.operator('mesh.bce_hardedgestoseams' ,text="Convert to Seams")  

        row = layout.row(align=True)
        row.operator('mesh.bce_addfwnmodifier' ,text="Add FWVN Modifier")

        row = layout.row(align=True)
        row.operator('mesh.bce_addtrimodifier' ,text="Add Triangulate Modifier")
        
        row = layout.row(align=True)
        row.operator('mesh.bce_addmirror' ,text="Mirror w/ MirrorHelper")

        row = layout.row(align=True)
        row.operator('mesh.bce_renameuvmaps' ,text="Rename UV Maps")

        ##
        layout.separator()
        ##
        layout.label(text="Cleanup:")
        row = layout.row(align=True)
        row.operator('mesh.bce_deletelinkedobjects' ,text="Delete Linked")

# Classes
from . import bce_classes 

classes = (
    Blender_CAD_Essentials_Panel,
    bce_classes.ClearCustomNormals,
    bce_classes.MakeTrisToQuads,
    bce_classes.MakeSingleUserObjectData,
    bce_classes.ResetScaleForLinkedObjects,
    bce_classes.ConvertHardEdgesToSeams,
    bce_classes.RenameUVMaps,
    bce_classes.AddFWNModifier,
    bce_classes.AddTriModifier,
    bce_classes.AddMirror,
    bce_classes.AddSmoothing,
    bce_classes.DeleteLinkedObjects,
)

def register():
    for cls in classes:
        register_class(cls)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
