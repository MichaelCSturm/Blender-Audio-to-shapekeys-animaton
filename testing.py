def render_lipsync_to_action(context, tgt_action, seq):
    props = context.scene.props
    
    key_interpolation = props.key_interpolation
    limit_pps:bool = props.limit_pps
    phonemes_per_second:float = props.phonemes_per_second
    rest_gap:float = props.rest_gap

    fps = context.scene.render.fps
    
    phone_list = get_phonemes_from_audio(context, seq)
    if len(phone_list) == 0:
        return

    #Throw out extra phonemes
    if limit_pps:
        sec_per_phone = 1 / phonemes_per_second
        new_phone_list = []
        last_phone_time:float = 0
        
        for phone in phone_list:
            if not new_phone_list:
                new_phone_list.append(phone)
                last_phone_time = phone["time"]
            elif phone["time"] - last_phone_time > sec_per_phone:
                new_phone_list.append(phone)
                last_phone_time = phone["time"]
        
        phone_list = new_phone_list

    #Make sure phone table is up to date
    update_phoneme_group_pose_list(context)
    

    phoneme_table = load_phoneme_table(context)

    #Map phone codes to phoneme table entries
    phoneme_hash:dict[str, dict] = {}
    for info in phoneme_table["phonemes"]:
        #print("Adding phoneme ", info)
        phoneme_hash[info["code"]] = info

    #Map group names to pose actions
    group_pose_hash:dict[str, bpy.props.PointerProperty] = {}
    for pose_props in props.phoneme_poses:
        group_pose_hash[pose_props.group] = pose_props.pose

    seq_time_start = seq.frame_offset_start / fps
    seq_time_end = (seq.frame_offset_start + seq.frame_final_duration) / fps

    #Convert phonemes to phone groups and add rests
    groups_seq:[dict] = []

    groups_seq.append(["rest", phone_list[0]["time"] - rest_gap])
    
    list_size = len(phone_list) - 2
    for phone_idx in range(len(phone_list) - 2):
        p0 = phone_list[phone_idx]
        p1 = phone_list[phone_idx + 1]
        
        phone = p0["phone"]
        if phone in phoneme_hash:
            groups_seq.append([phoneme_hash[phone]["group"], p0["time"]])
        else:
            print("missing phoneme:", phone)
        
        gap = p1["time"] - p0["time"]
        
        if gap > rest_gap * 2:
            groups_seq.append(["rest", p0["time"] + rest_gap])
            groups_seq.append(["rest", p1["time"] - rest_gap])
        elif gap > rest_gap:
            groups_seq.append(["rest", (p0["time"] + p1["time"]) / 2])
            
    phone = phone_list[-1]["phone"]
    if phone in phoneme_hash:
        groups_seq.append([phoneme_hash[phone]["group"], phone_list[-1]["time"]])
    else:
        print("missing phoneme:", phone)
    groups_seq.append({"rest", phone_list[-1]["time"] + rest_gap})
            
    #print("---Group seq")
    #print(groups_seq)
    

    #Clear existing animation
    tgt_action.fcurves.clear()
    for marker in tgt_action.pose_markers.values():
        tgt_action.pose_markers.remove(marker)

    #Write tracks
    for idx, phone_timing in enumerate(groups_seq):
        #print(phone_timing)
                        
        group_name, time = phone_timing
        #print("group_name " , group_name)
        if not group_name in group_pose_hash:
            continue
        
        src_action = group_pose_hash[group_name]
        if not src_action:
            continue

        marker = tgt_action.pose_markers.new(group_name)
        marker.frame = int(time * fps)
        
        #Ensure groups are present
        for src_group in src_action.groups:
            if not src_group.name in tgt_action.groups:
                tgt_action.groups.new(src_group.name)


        for src_curve in src_action.fcurves:
            #print("src_curve.data_path ", src_curve.data_path, src_curve.array_index)
            
            if src_curve.is_empty:
                continue

            tgt_curve = tgt_action.fcurves.find(src_curve.data_path, index = src_curve.array_index)
            if not tgt_curve:
                tgt_curve = tgt_action.fcurves.new(src_curve.data_path, index = src_curve.array_index)
                if src_curve.group:
                    tgt_curve.group = tgt_action.groups[src_curve.group.name]
            
            frame_range = src_action.curve_frame_range
            #print("range ", range)
            for src_kf in src_curve.keyframe_points:

                tgt_kf = tgt_curve.keyframe_points.insert(frame = (src_kf.co[0] - frame_range[0] + int(time * fps)), value = src_kf.co[1])
                
                tgt_kf.interpolation = src_kf.interpolation
                if key_interpolation == "constant":
                    tgt_kf.interpolation = 'CONSTANT'
                elif key_interpolation == "linear":
                    tgt_kf.interpolation = 'LINEAR'
                elif key_interpolation == "bezier":
                    tgt_kf.interpolation = 'BEZIER'
                    
                tgt_kf.easing = src_kf.easing
                tgt_kf.handle_left = src_kf.handle_left
                tgt_kf.handle_right = src_kf.handle_right
                tgt_kf.period = src_kf.period
