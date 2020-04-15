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
    next_frame=False
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        ball_x=scene_info.ball[0]
        ball_y=scene_info.ball[1]
        platform_x=scene_info.platform[0] 
        catch=False
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
        if ball_y<=100 or ball_y-position[1]<0:
            next_frame=False
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_RIGHT)
            ball_served = True  
        else:
            if ball_y>position[1] and next_frame and catch==False:  #next position is lower
                vector_x=ball_x-position[0]
                vector_y=ball_y-position[1]
                next_frame=False
                t=float((395-ball_y)/vector_y)
                placement=vector_x*t+ball_x
                while placement<0 or placement>195:
                    if placement<0:
                        placement=-placement
                    else:
                        placement=390-placement
                placement=placement-20

            if ball_y>100: #below the bricks
                if ball_x==0: #ball touches the left wall
                    next_frame = True
                elif ball_x==195: #ball touches the right wall
                    next_frame = True


                position=scene_info.ball #update position of ball every frame
                if platform_x<placement:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    #print("move right")
                elif platform_x>placement:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    #print("move left")
                else:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                    #print("move none")
                
            
