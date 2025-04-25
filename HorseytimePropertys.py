import bpy
def get_shape_key_items(self, context):
    obj = context.scene.my_object.faceHappy
    items = []

    if obj:
        try:
            if obj and obj.data.shape_keys and obj.data.shape_keys.key_blocks:
                for i, key_block in enumerate(obj.data.shape_keys.key_blocks):
                    items.append((key_block.name, key_block.name, "", i))
        except Exception as e:
            print(e)
    return items or [("NONE", "No Shape Keys", "", 0)]

# def intern_enum_items_strings(items):
#     def intern_string(s):
#         if isinstance(s, str):
#             ENUM_STRING_CACHE.setdefault(s, s)
#             s = ENUM_STRING_CACHE[s]
#         return s

#     return [
#         tuple([intern_string(s) for s in item])
#         for item in items
#     ]

class myenum():
    myenumlist = []
class MyKeyholder(bpy.types.PropertyGroup):
    faceHappy: bpy.props.PointerProperty(
        name = "Armature",
        description = "Armature pose for this lipsync group.",
        type=bpy.types.Object
    )
    dataOutput : bpy.props.StringProperty( default="no data yet")
    phenDataOutput : bpy.props.StringProperty( default="no data yet")

class MyMaterialProps(bpy.types.PropertyGroup):
    # pose: bpy.props.PointerProperty(
    #     name = "Pose Action",
    #     description = "Armature pose for this lipsync group.",
    #     type=bpy.types.Action
    # )
    # Armature: bpy.props.PointerProperty(
    #     name = "Armature",
    #     description = "Armature pose for this lipsync group.",
    #     type=bpy.types.Armature
    # )
    
    # key: bpy.props.PointerProperty(
    #     name = "Armature",
    #     description = "Armature pose for this lipsync group.",
    #     type=bpy.types.Key,
        
    # )
    name : bpy.props.StringProperty( default="n/a")
    diabox: bpy.props.EnumProperty(
        name= "",
        items= get_shape_key_items,
       
        options={'ANIMATABLE'},
        
    )

# def get_items(self, context):
#     l = []
#     if bpy.context.scene.my_custom_props.key:
#         for shape in bpy.data.shape_keys:
#             pass
#     return l