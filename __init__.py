import bpy
bl_info = {
    "name": "Audio Again",
    "author": "michaelSturm",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}

from . HorseytimePropertys import MyMaterialProps, myenum, MyKeyholder
from . HorseytimePanel import HorseyTime_PT_Panel, CreateShapeKeysOperator, ImportAudioOperator, BakeAudioOperator

# bpy.utils.register_class(MyItem)
# bpy.utils.register_class(MySceneProperties)
# bpy.types.Scene.my_props = bpy.props.PointerProperty(type=MySceneProperties)
classes = { CreateShapeKeysOperator, MyKeyholder, ImportAudioOperator, BakeAudioOperator}
def register():
    
    bpy.utils.register_class(MyMaterialProps)
    bpy.utils.register_class(HorseyTime_PT_Panel)
    bpy.types.Scene.my_custom_props= bpy.props.CollectionProperty(type=MyMaterialProps)
    
    for c in classes:
        
        bpy.utils.register_class(c)
    #bpy.types.Scene.my_custom_sub_props= bpy.props.PointerProperty(type=Poses)
    print("register finished starting")
    bpy.types.Scene.my_object = bpy.props.PointerProperty(type=MyKeyholder)
    
    

def unregister(): 
    for c in classes:
        bpy.utils.unregister_class(c)
    print("deleting classes")
    bpy.utils.unregister_class(MyMaterialProps)
    bpy.utils.unregister_class(HorseyTime_PT_Panel)
    
    del bpy.types.Scene.my_custom_props
    del bpy.types.Scene.my_object
    #del bpy.types.Scene.my_custom_sub_props
    