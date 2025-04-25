import bpy
from bpy.types import Panel, Operator
#from RealtimeSTT import AudioToTextRecorder
#from .RealtimeSTT import importer
from allosaurus.app import read_recognizer
from allosaurus.model import get_all_models
from allosaurus.audio import read_audio
#from allosaurus.audio import read_audio
import wx
import logging
from .easybpy import *
import math
logging.basicConfig(filename="debugAndErrorLog.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.DEBUG)


#import os 

  
engligh_phone_inventory = {'a', 'aː', 'b', 'd', 'd̠', 'e', 'eː', 'e̞', 'f', 'h', 'i', 'iː', 'j', 'k', 'kʰ', 'l', 'm', 'n', 'o', 'oː', 'p', 'pʰ', 'r', 's', 't', 'tʰ', 't̠', 'u', 'uː', 'v', 'w', 'x', 'z', 'æ', 'ð', 'øː', 'ŋ', 'ɐ', 'ɐː', 'ɑ', 'ɑː', 'ɒ', 'ɒː', 'ɔ', 'ɔː', 'ɘ', 'ə', 'əː', 'ɛ', 'ɛː', 'ɜː', 'ɡ', 'ɪ', 'ɪ̯', 'ɯ', 'ɵː', 'ɹ', 'ɻ', 'ʃ', 'ʉ', 'ʉː', 'ʊ', 'ʌ', 'ʍ', 'ʒ', 'ʔ', 'θ'}
engligh_phone_inventory_simplifed = {'a' : 1 , 'aː': 1, 'e': 2, 'eː': 2, 'e̞': 2, 'i': 3, 'iː': 3, 'o': 4, 'oː': 4, 'u': 5, 'uː': 5, 'æ': 2, 'ɐ': 2, 'ɐː': 2, 'ɑ': 1, 'ɑː': 1, 'ɛ': 1, 'ɛː': 1, 'ɜː': 1,  'ɪ' : 3, 'ɪ̯' : 3, 'ʉ':5, 'ʉː':5}

# # load your model
model = read_recognizer()

# run inference -> æ l u s ɔ ɹ s
output = model.recognize('16-122828-0002.wav', timestamp=True)
models = get_all_models()

#print(output)





#print(models)
#print(output)

class dataholder():
    data= ""
    audioLength = 0
    audio_to_fps =0
    #2logging.debug(audio_to_fps)
def get_data_from_audio(file):
    output = model.recognize(file, timestamp=True, lang_id= 'eng')
    audio_object = read_audio(file)
    audio_duration = audio_object.duration()
    #print(output)
    split_output = output.split("\n")
    list = []
    for x in split_output:
        list.append(x)
    
    
    
    #     print(x)
    bpy.context.scene.my_object.dataOutput = output
    
    return list, audio_duration

def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def apply_pose(pose_id, blend_factor=1):
    #  https://blender.stackexchange.com/questions/258952/how-to-properly-execute-poselib-operators-pose-library/258970#258970?s=d03c6944322f4034875046fad6b365de
    
    win = bpy.context.window
    scr = win.screen
    assets = [area for area in scr.areas if area.type == 'FILE_BROWSER']
    if len(assets):
        region = [region for region in assets[0].regions if region.type == 'TOOLS']
        space = assets[0].spaces[0]
        space.deselect_all()
        space.activate_asset_by_id(bpy.data.actions[pose_id])
        if len(region):
            kwargs = {
                'window': win,
                'screen': scr,
                'area'  : assets[0],
                'region': region[0],
                'scene' : bpy.context.scene,
            }
            with bpy.context.temp_override(**kwargs):
                bpy.ops.poselib.blend_pose_asset(
                    
                    blend_factor=blend_factor,
                    flipped=False)
                

                
            # armature = bpy.context.scene.my_custom_props.Armature
            # for bone in armature.pose.bones:
            #     bone.keyframe_insert(data_path = "location")
            #     bone.keyframe_insert(data_path = "scale")
                    
            #         # *** IMPORTANT ***
            #         # Remove the hashtag symbol in front of the bone.keyframe_insert()
            #         # line that cooresponds to the type of rotation you're using for each bone
            #         # and replace with a space
            #         # Then add a hashtag in front of the one that was previously commented out in gray text
                    
            #         # I'm assuming that you're only using one type of rotation for all bones in your armature
            #         # since the Valve Biped system uses quaternions
                    
            #         # If your custom rig uses a combination of any of these... you're on your own. This script
            #         # won't work.
                    
            #     bone.keyframe_insert(data_path = "rotation_quaternion")
        else:
            logging.debug("Current Pose Library does not have a tools menu open.")
    else:
        logging.debug("There is no Pose LIbrary open.")

def get_pose_index(action ):
    i = 0
    while i < len(bpy.data.actions):
        print(bpy.data.actions[i])
        if bpy.data.actions[i] == action:
            return i
        i+=1
    return 0

class BakeAudioOperator(Operator):
    """Print object name in Console"""
    bl_idname = "object.bake_audio_operator"
    bl_label = "Simple Object Operator"
    bl_region_type = "UI"
    bl_label = "Audio engineering"
    bl_category = "HorseyTime Util"

    def execute(self, context):
       #
       # ##
       # ######### KEYFRAME .keyframe_insert(data_path='value', frame=1)
        logging.debug("baked audio!")
        if dataholder.data == "":
            logging.debug("no data")
            return {'FINISHED'}
        else:
            for list in dataholder.data:
                split_list = list.split()
                find_vowel = split_list[2]
                print(list)
                if find_vowel in engligh_phone_inventory_simplifed:
                    match engligh_phone_inventory_simplifed[find_vowel]:
                        case 1:
                            my_start_frame = math.ceil(float(split_list[1])/dataholder.audio_to_fps )
                            my_end_frame = math.ceil(float(split_list[0])/dataholder.audio_to_fps )
                            logging.debug(f"baked {find_vowel} at {my_start_frame} and {my_end_frame} when it should {split_list[1]} and {split_list[0]}")

                            name = bpy.context.scene.my_custom_props[0].diabox
                            obj = context.scene.my_object.faceHappy
                            items = []
                            if obj:
                                try:
                                    
                                    for i, key_block in enumerate(obj.data.shape_keys.key_blocks):
                                        if key_block.name == name:
                                            key_block.keyframe_insert(data_path='value', frame=my_start_frame)
                                            key_block.keyframe_insert(data_path='value', frame=my_end_frame)
                                            break

                                            
                                except Exception as e:
                                    logging.debug(e)
                            else:
                                logging.debug("no faceHappy")
                            #
                #logging.debug("couldn't find phentic in simp list", str(split_list[2]))
        
        return {'FINISHED'}

class ImportAudioOperator(Operator):
    """Print object name in Console"""
    bl_idname = "object.import_audio_operator"
    bl_label = "Simple Object Operator"
    bl_region_type = "UI"
    bl_label = "Audio engineering"
    bl_category = "HorseyTime Util"

    def execute(self, context):
        
        file = get_path(' Wav files(*.wav)|*.wav')
        if file == None:
            return {'FINISHED'}
        output, duration =get_data_from_audio(file)
        dataholder.data = output
        dataholder.audioLength =duration
        dataholder.audio_to_fps = math.ceil(duration * bpy.context.scene.render.fps)
        logging.debug(f" The audio to fps rounded: {dataholder.audio_to_fps}" )
        logging.debug(bpy.context.scene.my_custom_props[0].diabox)
        return {'FINISHED'}

class CreateShapeKeysOperator(Operator):
    """Print object name in Console"""
    bl_idname = "object.create_shape_keys_operator"
    bl_label = "Simple Object Operator"
    bl_region_type = "UI"
    bl_label = "Audio engineering"
    bl_category = "HorseyTime Util"

    def execute(self, context):
        
        if not bpy.context.scene.my_custom_props:
            my_item = bpy.context.scene.my_custom_props.add()
                
            my_item = bpy.context.scene.my_custom_props.add()
                
            my_item = bpy.context.scene.my_custom_props.add()
                
            my_item = bpy.context.scene.my_custom_props.add()
                
            my_item = bpy.context.scene.my_custom_props.add()
        

        
        return {'FINISHED'}
    
list =["a","e","i","o","u"]

class HorseyTime_PT_Panel(Panel):
    bl_idname = "HorseyTime_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Audio engineering"
    bl_category = "HorseyTime Util"
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        sce = context.scene
        col = layout.column()
        row = col.row()
        col.operator(CreateShapeKeysOperator.bl_idname, text="Import Shapekeys", icon="GRID")
        col.prop(sce.my_object, "dataOutput")
        col.prop(sce.my_object, "faceHappy", text="mesh to keyframe shapekey")
        row = layout.row()
        col = layout.column()

        for item in bpy.context.scene.my_custom_props:
            row = layout.row()
            row.prop(item,"diabox")
        col.operator(ImportAudioOperator.bl_idname, text="Import Audio", icon="CONSOLE")
        col.operator(BakeAudioOperator.bl_idname, text="Bake Audio", icon="SPEAKER")
          
        
        

