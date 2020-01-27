from maya import cmds

# Store a bind pose for use with the script
#cmds.dagPose(skeleton_node, name="my_pose", save=True)

# Predefined target pose and top node of skeleton
target_pose="my_pose"
skeleton_node="Hips"

def get_preroll_frames():
    # Prompt the user to enter the amount of desired frames for preroll
    result = cmds.promptDialog(
                        title='Enter Preroll Frames',
                        message='Enter Preroll:',
                        button=['OK', 'Cancel'],
                        defaultButton='OK',
                        cancelButton='Cancel',
                        dismissString='Cancel')

    if result == 'OK':
        my_text = cmds.promptDialog(query=True, text=True)
        if my_text.isnumeric():
            return int(my_text)
        else:
            cmds.error('Enter numerical value')
    
def set_preroll_bind_pose(skeleton_node, preroll_frames, target_pose):
    # Set keyframes on current time for all joints in heirarchy
    # adjust time to new preroll time
    # set joints to bind pose
    # set keys on all joints
    current_time=cmds.currentTime(query=True)
    all_bones = cmds.listRelatives(skeleton_node, ad=True, type="joint")
    cmds.setKeyframe(all_bones, t=current_time)
    cmds.currentTime(current_time-preroll_frames)
    cmds.dagPose(skeleton_node, name=target_pose, restore=True)
    preroll_time=current_time-preroll_frames
    cmds.setKeyframe(all_bones, t=preroll_time)
    
preroll_frames=get_preroll_frames()

if preroll_frames:
    set_preroll_bind_pose(skeleton_node, preroll_frames, target_pose)
