"""
The template of the main script of the machine learning process
"""
import sys
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
    position=[0,0]
    placement=75 #point of fall
    bounce=False
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        ball_x=scene_info.ball[0]
        ball_y=scene_info.ball[1]
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
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True  

        else:
            """if ball_y>100: #below the bricks
                if ball_x==0: #ball touches the left wall
                    if ball_y>position[1]:  #next position is lower
                        if position[1]+7<200: 
                            placement=position[1]
                            bounce=True
                        else:
                            placement=370-position[1]
                            bounce=True
                    else:
                        bounce=False
                elif ball_x==195: #ball touches the right wall
                    if ball_y>position[1]:  #next position is lower
                        if position[1]+7<200: 
                            placement=200-position[1]
                            bounce=True
                        else:
                            placement=position[1]-210
                            bounce=True
                    else:
                        bounce=False
                else:
                    pass
           
                position=scene_info.ball #update position of ball every frame
                if bounce: #ball touches the wall and make platform to the placement
                    if platform_x<placement:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                        if ball_y==395: #catch the ball
                            bounce=False
                    elif platform_x>placement:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                        if ball_y==395: #catch the ball
                            bounce=False
                    else:
                        comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                        if ball_y==395: #catch the ball
                            bounce=False
                else : #make platform to the center
                    if platform_x<75:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    elif platform_x>75:
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    else:
                        comm.send_instruction(scene_info.frame, PlatformAction.NONE) """
            
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)  
            
