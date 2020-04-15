"""
The template of the main script of the machine learning process
"""
import sys
import random
import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    ball_x=-1
    ball_y=-1
    vector=[0,0]
    placement=75 #point of fall
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        platform_x=scene_info.platform[0] 
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False
            
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_RIGHT)
            ball_served = True  
        else:
            #if ball_x==0 or ball_x==195: #ball touches the wall
            if ball_y>100: #ball is below bricks
                if scene_info.ball[1]-ball_y>0: #ball is moving downward
                    vector=[(scene_info.ball[0]-ball_x),(scene_info.ball[1]-ball_y)]
                    fall_time=(400-scene_info.ball[1])/vector[1]
                    placement=fall_time*vector[0]+scene_info.ball[0]
                else: #ball is moving upward
                    placement=100 #platform moves to center

            while placement>195 or placement<0:
                if placement>195:
                    placement=390-placement
                elif placement<0:
                    placement=-placement

            
            #temp=random.randint(1,5) #prevent forever loop
            if platform_x<placement-20:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif platform_x>placement-20:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            
            
                
            ball_x=scene_info.ball[0]
            ball_y=scene_info.ball[1]
