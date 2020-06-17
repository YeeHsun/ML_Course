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
        self.done = 0  
        self.init_lane = 1
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
                    if x > -80 and x < -20 :
                        if y > 80 and y < 120:
                            grid.add(3)
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 80 and x > 20:
                        if y > 80 and y < 120:
                            grid.add(1)
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead)
            
                
                    
                
            
        def move(grid, speed_ahead): 
            if self.player_no == 0 or self.player_no == 1 or self.player_no == 2 or self.player_no == 3:
                print(grid)
                '''print ("car lane:")
                print (self.car_lane)
                print ("car pos:")
                print (self.car_pos[0])
                print ("left")
                print(self.lanes[self.target_lane_left])
                print ("right")
                print(self.lanes[self.target_lane_right])
                print (self.init_lane)
                print (self.car_pos[0])'''

            #print (self.done)
            if len(grid) == 0:
                if self.done == 0:
                    self.init_lane=self.lanes[self.car_lane]
                    self.done = 1
                if self.car_pos[0]>self.init_lane-35:
                    return ["SPEED","MOVE_LEFT"]
                elif self.car_pos[0]<self.init_lane-35:
                    return ["SPEED","MOVE_RIGHT"]
                else:
                    return ["SPEED"]
            else:
                if (1 in grid) :
                    if self.car_pos[0]>self.init_lane-25:
                        return ["SPEED","MOVE_LEFT"]
                    elif self.car_pos[0]<self.init_lane-25:
                        return ["SPEED","MOVE_RIGHT"]
                    else:
                        return ["SPEED"]
                elif (3 in grid):
                    if self.car_pos[0]>self.init_lane-45:
                        return ["SPEED","MOVE_LEFT"]
                    elif self.car_pos[0]<self.init_lane-45:
                        return ["SPEED","MOVE_RIGHT"]
                    else:
                        return ["SPEED"]
                elif (1 in grid) and (3 in grid):
                        return ["NONE"]
                else:
                    return ["SPEED"]
                    
                                
                    
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
