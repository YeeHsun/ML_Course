class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.done = 0  #done = 0 when finishing changing car lane
        self.command = 0  #0:NONE 1:SPEED 2:SPEED-RIGHT 3:SPEED-LEFT 4:RIGHT 5:LEFT 6:BRAKE 7:BRAKE-RIGHT 8:BRAKE-LEFT
        self.target_lane_left = 0
        self.target_lane_right = 0
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        
        def check_grid():
            grid = set()
            speed_ahead = 100
            if self.car_pos[0] <= 65: # left bound//65
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 565: # right bound//565
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 250:
                                speed_ahead = car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 250:
                            grid.add(3)
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 250:
                            grid.add(1)
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
            if self.done == 0:
                return move(grid= grid, speed_ahead = speed_ahead)
            else:
                if self.command == 0:
                    return ["NONE"]
                elif self.command == 1:
                    self.done = 0
                    return ["SPEED"]
                    
                elif self.command == 2:
                    if self.car_pos[0]==self.lanes[self.target_lane_right]:
                        self.done = 0
                    return ["SPEED","MOVE_RIGHT"]
                elif self.command == 3:
                    if self.car_pos[0]==self.lanes[self.target_lane_left]:
                        self.done = 0
                    return ["SPEED","MOVE_LEFT"]
                elif self.command == 4:
                    if self.car_pos[0]==self.lanes[self.target_lane_right]:
                        self.done = 0
                    return ["MOVE_RIGHT"]
                elif self.command == 5:
                    if self.car_pos[0]==self.lanes[self.target_lane_left]:
                        self.done = 0
                    return ["MOVE_LEFT"]
                elif self.command == 6:
                    self.done = 0
                    return ["BRAKE"]
                    
                elif self.command == 7:
                    if self.car_pos[0]==self.lanes[self.target_lane_right]:
                        self.done = 0
                    return ["BRAKE","MOVE_RIGHT"]
                elif self.command == 8:
                    if self.car_pos[0]==self.lanes[self.target_lane_left]:
                        self.done = 0
                    return ["BRAKE","MOVE_LEFT"]
                
                    
                
            
        def move(grid, speed_ahead): 
            if self.player_no == 0:
                print(grid)
                '''print ("car lane:")
                print (self.car_lane)
                print ("car pos:")
                print (self.car_pos[0])
                print ("left")
                print(self.lanes[self.target_lane_left])
                print ("right")
                print(self.lanes[self.target_lane_right])'''
            #print (self.done)
            if len(grid) == 0:
                return ["SPEED"]
            else:
                if (2 not in grid): # Check forward 
                    # Back to lane center
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
                else:
                    #if self.car_lane==0 or self.car_lane==1 or self.car_lane==2 or self.car_lane==3 or self.car_lane==4:
                    if (5 in grid): # NEED to BRAKE
                        if self.done == 0:
                            if self.car_lane+1<=8:
                                self.target_lane_right = self.car_lane+1  #right lane of curent lane
                            else:
                                self.target_lane_right = self.car_lane
                            if self.car_lane-1>=0:
                                self.target_lane_left = self.car_lane-1   #left lane of curent lane
                            else:
                                self.target_lane_left = self.car_lane
                            
                        self.done = 1                        #haven't changed lane
                        '''print (target_lane_left)
                        print (target_lane_right)'''
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            #if self.car_vel < speed_ahead:                                    
                            self.command = 2 #speed-right
                            print ("speed right")
                            '''else:
                                self.command = 4''' #brake-right
                                
                        elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn right
                            #if self.car_vel < speed_ahead:                                    
                            self.command = 3 #speed-right
                            print ("speed left")   
                            '''else:
                                self.command = 5 #brake-right'''
                                
                        elif (6 not in grid) and (9 not in grid): # turn right
                            #if self.car_vel < speed_ahead:                                    
                            self.command = 2 #speed-right
                            print ("speed right")    
                            '''else:
                                self.command = 4 #brake-right'''
                                
                        elif (4 not in grid) and (7 not in grid): # turn left 
                            #if self.car_vel < speed_ahead:
                            self.command = 3 #speed-left
                            print ("speed left")    
                            '''else:
                                self.command = 5 #brake-left'''
                                
                        else : 
                            if self.car_vel < speed_ahead:  # BRAKE
                                self.command = 1
                                
                            else:
                                print ("brake")
                                self.command = 6
                                
                    if (self.car_pos[0] < 60 ):
                        self.command = 2 #speed-left
                        #return ["SPEED", "MOVE_RIGHT"]                        
                    if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                        self.command = 2 #speed-left
                        #return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                        self.command = 3 #speed-left
                        #return ["SPEED", "MOVE_LEFT"]                        
                    if (3 not in grid) and (6 not in grid): # turn right
                        self.command = 2 #speed-left
                        #return ["SPEED", "MOVE_RIGHT"]
                    if (1 not in grid) and (4 not in grid): # turn left 
                        self.command = 3 #speed-left
                        #return ["SPEED", "MOVE_LEFT"]                         
                    if (6 not in grid) and (9 not in grid): # turn right
                        self.command = 4 #speed-left
                        #return ["MOVE_RIGHT"]
                    if (4 not in grid) and (7 not in grid): # turn left 
                        self.command = 5 #speed-left
                        #return ["MOVE_LEFT"] 
                    '''else:
                        if (5 in grid): # NEED to BRAKE
                            target_lane_right = self.car_lane+1
                            target_lane_left = self.car_lane-1
                            self.done = 1
                            print (target_lane_left)
                            print (target_lane_right)
                            
                            if (4 not in grid) and (7 not in grid): # turn left 
                                if self.car_vel < speed_ahead:
                                    while self.car_pos[0]>target_lane_left:
                                        return ["SPEED", "MOVE_LEFT"]
                                    self.done = 0
                                else:
                                    while self.car_pos[0]>target_lane_left:
                                        return ["BRAKE", "MOVE_LEFT"]
                                    self.done = 0
                            elif (6 not in grid) and (9 not in grid): # turn right
                                if self.car_vel < speed_ahead:
                                    while self.car_pos[0]<target_lane_right:
                                        return ["SPEED", "MOVE_RIGHT"]
                                    self.done = 0
                                else:
                                    while self.car_pos[0]<target_lane_right:
                                        return ["BRAKE", "MOVE_RIGHT"]
                                    self.done = 0
                            else : 
                                if self.car_vel < speed_ahead:  # BRAKE
                                    return ["SPEED"]
                                else:
                                    return ["BRAKE"]
                        if (self.car_pos[0] < 60 ):
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (4 not in grid): # turn left 
                            return ["SPEED", "MOVE_LEFT"]
                        if (3 not in grid) and (6 not in grid): # turn right
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 not in grid) and (7 not in grid): # turn left 
                            return ["MOVE_LEFT"]    
                        if (6 not in grid) and (9 not in grid): # turn right
                            return ["MOVE_RIGHT"]'''
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
