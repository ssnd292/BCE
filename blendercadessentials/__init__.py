bl_info = {
    "name" : "Blender CAD Essentials",
    "author" : "Sebastian Schneider",
    "description" : "Collection of often needed tools when working with imported CAD Data",
    "blender" : (2, 93, 0),
    'version': (0, 1, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.utils import register_class, unregister_class

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

class BCEProperties(PropertyGroup):
    boolUseMirrorHelper: BoolProperty(
        name="Use MirrorHelper",
        description="Uses MirrorHelper for Mirroring",
        default = True
        )

    stringUVMapName: StringProperty(
        name="Name:",
        description="Name of Renamed UVMap",
        default="UVmap",
        maxlen=1024
        )

    floatSmoothing: FloatProperty(
        name = "Smotthing Angle °",
        description = "HardOps Smoothing Angle",
        default = 60,
        min = 0.0,
        max = 180.0
        )

class BCE_PT_MainUI(bpy.types.Panel):
    bl_idname = "Essentials"
    bl_label = "Blender CAD Essentials"
    bl_category = "Item"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        bceprops = context.scene.bceprops
        layout = self.layout

        layout.label(text="Modelling:")
        row = layout.row(align=True)
        row.operator('mesh.bce_clearnormals' ,text="Reset Custom Normals")

        row = layout.row(align=True)
        row.operator('mesh.bce_tristoquads' ,text="Tris to Quads")

        row = layout.row(align=True)
        row.operator('mesh.bce_makesingleuser' ,text="Make Single User")

        row = layout.row(align=True)
        row.operator('mesh.bce_resetscale' ,text="Reset Scale of Links")

        row = layout.row(align=True)
        row.operator('mesh.bce_addtrimodifier' ,text="Add Triangulate Modifier")
        
        row = layout.row(align=True)
        row.operator('mesh.bce_addmirror' ,text="Mirror w/ MirrorHelper")
        row = layout.row(align=True) 
        row.prop(bceprops, "boolUseMirrorHelper")

        row = layout.row(align=True)        
        row.operator('mesh.bce_addsmoothing' ,text="HardOps Sharpen")

        row = layout.row(align=True) 
        row.prop(bceprops, "floatSmoothing")

        ##
        layout.separator()
        ##
        layout.label(text="Unwrapping Functions:")

        row = layout.row(align=True)
        row.operator('mesh.bce_hardedgestoseams' ,text="Convert to Seams")  

        row = layout.row(align=True)
        row.operator('mesh.bce_addfwnmodifier' ,text="Add FWVN Modifier")

        row = layout.row(align=True)
        row.operator('mesh.bce_renameuvmaps' ,text="Rename UV Maps")

        row = layout.row(align=True)
        row.prop(bceprops, "stringUVMapName")

        row = layout.row(align=True)
        row.operator('mesh.bce_transferuvmaps' ,text="Transfer UV Maps")

        ##
        layout.separator()
        ##

        layout.label(text="Miscellanous Functions:")
        row = layout.row(align=True)
        row.operator('mesh.bce_deletelinkedobjects' ,text="Delete Linked")


# Classes
from . import bce_classes 

classes = (
    BCEProperties,
    BCE_PT_MainUI,
    bce_classes.MESH_OT_ClearCustomNormals,
    bce_classes.MESH_OT_MakeTrisToQuads,
    bce_classes.MESH_OT_MakeSingleUserObjectData,
    bce_classes.MESH_OT_ResetScaleForLinkedObjects,
    bce_classes.MESH_OT_ConvertHardEdgesToSeams,
    bce_classes.MESH_OT_RenameUVMaps,
    bce_classes.MESH_OT_AddFWNModifier,
    bce_classes.MESH_OT_AddTriModifier,
    bce_classes.MESH_OT_AddMirror,
    bce_classes.MESH_OT_AddSmoothing,
    bce_classes.MESH_OT_DeleteLinkedObjects,
    bce_classes.MESH_OT_TransferUVMaps,
    bce_classes.MESH_OT_AddSecondUV,
)

def register():
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.bceprops = PointerProperty(type=BCEProperties)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.bceprops

if __name__ == "__main__":
    register()