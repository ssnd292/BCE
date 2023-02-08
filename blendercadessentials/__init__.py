bl_info = {
    "name" : "Blender CAD Essentials",
    "author" : "Sebastian Schneider",
    "description" : "Collection of often needed tools when working with imported CAD Data.",
    "blender" : (3, 1, 0),
    'version': (0, 1, 9 ,3),
    "location" : "View3D",
    "warning" : "",
    "category" : "View3D"
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
                       
from math import radians


hopsInstalled = False

for addon in bpy.context.preferences.addons:
    if addon.module == "HOps":
        hopsInstalled = True
        print("HOps is installed.")

class BCEProperties(PropertyGroup):
    boolUseMirrorHelper: BoolProperty(
        name="MirrorHelper",
        description="Uses MirrorHelper for Mirroring",
        default = True
        )

    boolMirrorMoveUV: BoolProperty(
        name="Move UV?",
        description="Moves UV one Grid to the right",
        default = False
        )

    stringUVMapName: StringProperty(
        name="Name:",
        description="Name of Renamed UVMap",
        default="UVMap",
        maxlen=1024
        )

    floatSmoothing: FloatProperty(
        name = "",
        description = "HardOps Smoothing Angle",
        default = radians(60),
        min = radians(0.0),
        max = radians(180.0),
        subtype="ANGLE",
        )

    maxObjectNumber: IntProperty(
        name = "",
        description = "Number of Maximum Objects",
        default = 0,
        min = 0,
        max = 10000,
        )

    commonDenominatorInt: IntProperty(
        name = "",
        description = "Number of Linked Groups Wanted",
        default = 2,
        min = 0,
        max = 10000,
        )
    
    maxRandomRotate: FloatProperty(
        name = "",
        description = "Maximum Random Rotation",
        default = radians(180.0),
        min = radians(0.0),
        max = radians(180.0),
        subtype="ANGLE",
        )
    
    axisRandomRotate: EnumProperty(
        name="Axis",
        description="Rotation Axis",
        items=[ ('X', "X", ""),
                ('Y', "Y", ""),
                ('Z', "Z", ""),
               ]
        )

    uvMapEnum: EnumProperty(
    name="UV",
    description="UV Selector",
    items=[ ('0', "UV00", ""),
            ('1', "UV01", ""),
            ('2', "UV02", ""),
            ('3', "UV03", ""),
            ('4', "UV04", ""),
            ('5', "UV05", ""),
            ('6', "UV06", ""),
            ('7', "UV07", ""),
            ]
    )


class BCE_PT_MainUI(bpy.types.Panel):
    bl_idname = "BCE_PT_MainUI"
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

        layout.separator()
        row = layout.row(align=True)
        row.prop(bceprops, "maxObjectNumber")
        row.prop(bceprops, "commonDenominatorInt")
        row = layout.row(align=True)
        layout.separator()
        row.operator('mesh.bce_resetnumbercounter' ,text="Reset Number")
        row.operator('mesh.bce_changenumberoflinkedobjects' ,text="Relink Objects")        

        if hopsInstalled == True:            
            row = layout.row(align=True)
            row.prop(bceprops, "floatSmoothing") 
            row.operator('mesh.bce_addsmoothing' ,text="HardOps Sharpen")  
            layout.separator()      

        row = layout.row(align=True)
        row.prop(bceprops, "axisRandomRotate") 
        row.prop(bceprops, "maxRandomRotate")
        row = layout.row(align=True)
        row.operator('mesh.bce_localrandomrotate' ,text="Random Local Rotate")
        
        layout.separator()
        layout.label(text="Modifier:")       
        row = layout.row(align=True)
        row.operator('mesh.bce_addfwnmodifier' ,text="Add FWVN Modifier")   
        row = layout.row(align=True)
        row.operator('mesh.bce_addtrimodifier' ,text="Triangulate")        
     

        row = layout.row(align=True)
        row.prop(bceprops, "boolUseMirrorHelper")
        row.prop(bceprops, "boolMirrorMoveUV")
        row = layout.row(align=True)
        row.operator('mesh.bce_addmirror' ,text="Add Mirror Modifier")
        ##
        layout.separator()
        ##
        layout.label(text="Unwrapping Functions:")

        row = layout.row(align=True)
        row.prop(bceprops, "uvMapEnum") 
        row.operator('mesh.bce_selectuvmap' ,text="Select UV")
        row = layout.row(align=True)
        row.operator('mesh.bce_addanotheruv' ,text="Add UVMap")
        row.operator('mesh.bce_removeselecteduvmap' ,text="Remove UVMap")

        row = layout.row(align=True)
        row.operator('mesh.bce_hardedgestoseams' ,text="Convert Edge to Seams")  

        layout.separator()
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
        row.operator('mesh.bce_deletelinkedobjects' ,text="Delete Linked Objects")


# Classes
from . import bce_classes 

classes = (
    BCEProperties,
    BCE_PT_MainUI,
    bce_classes.BCE_OT_ClearCustomNormals,
    bce_classes.BCE_OT_MakeTrisToQuads,
    bce_classes.BCE_OT_MakeSingleUserObjectData,
    bce_classes.BCE_OT_ResetScaleForLinkedObjects,
    bce_classes.BCE_OT_ChangedNumberOfLinkedObjects,
    bce_classes.BCE_OT_ResetNumberCounter,
    bce_classes.BCE_OT_ConvertHardEdgesToSeams,
    bce_classes.BCE_OT_SelectUVMap,
    bce_classes.BCE_OT_RenameUVMaps,
    bce_classes.BCE_OT_AddFWNModifier,
    bce_classes.BCE_OT_AddTriModifier,
    bce_classes.BCE_OT_AddMirror,
    bce_classes.BCE_OT_SetHOPsSharpness,
    bce_classes.BCE_OT_AddSmoothing,    
    bce_classes.BCE_OT_DeleteLinkedObjects,
    bce_classes.BCE_OT_TransferUVMaps,
    bce_classes.BCE_OT_AddUVMap,
    bce_classes.BCE_OT_RemoveSelectedUVMap,
    bce_classes.BCE_OT_LocalRandomRotate,
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