import random
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
        self.change_lane = 0
        self.command = 0
        global alive
        alive = True
        pass

    def update(self, scene_info):  
        if alive ==True:
            def check_grid():
                car_grid = set()  #computer car information 
                coin_grid = set() #coin imformation
                position_ahead = 80000
                speed_ahead = 100
                if self.car_pos[0] <= 35: # left bound//35
                    car_grid.add(5)
                    car_grid.add(7)
                    car_grid.add(10)

                elif self.car_pos[0] >= 595: # right bound//595
                    car_grid.add(6)
                    car_grid.add(8)
                    car_grid.add(11)


                for car in scene_info["cars_info"]:
                    if car["id"] != self.player_no: #not player's car
                        x = self.car_pos[0] - car["pos"][0] # x relative position
                        y = self.car_pos[1] - car["pos"][1] # y relative position
                        if x > -80 and x < 0 :
                            if y > 80 and y < 300:
                                car_grid.add(2)  #far right front
                                if 300> y >150:
                                    car_grid.add(4) #middle right front
                                if y < 160:
                                    car_grid.add(6)
                                    
                            elif y < 80 and y > -80:
                                car_grid.add(8)
                            elif y < -80 and y > -150:
                                car_grid.add(11)
                        if x < 80 and x > 0:
                            if y > 80 and y < 300:
                                car_grid.add(1)
                                if 300 > y > 150:
                                    car_grid.add(3)
                                if y < 160:
                                    car_grid.add(5)
                                    
                            elif y < 80 and y > -80:
                                car_grid.add(7)
                            elif y < -80 and y > -150:
                                car_grid.add(10)
                        if x <= 20 and x >= -20 : 
                            if y > 0 and y < 200:
                                position_ahead = y
                                speed_ahead = car["velocity"]
                                car_grid.add(9) 
                #coin information
                for coin in scene_info["coins"]:
                    coin_x = self.car_pos[0] - coin[0] # x relative position
                    coin_y = self.car_pos[1] - coin[1] # y relative position
                    if coin_x > -80 and coin_x < 0 :
                        if coin_y > 80 and coin_y < 150:
                            coin_grid.add(6)
                        elif coin_y < 80 and coin_y > -80:
                            coin_grid.add(8)
                    if coin_x < 80 and coin_x > 0:
                        if coin_y > 80 and coin_y < 150:
                            coin_grid.add(5)
                        elif coin_y < 80 and coin_y > -80:
                            coin_grid.add(7)


                if self.change_lane == 0:
                    return move(car_grid= car_grid,coin_grid=coin_grid, position_ahead = position_ahead,speed_ahead=speed_ahead)
                else:
                    if self.command == 1:
                        if (self.car_pos[0]==self.init_lane-63) or (self.car_pos[0] == self.init_lane-62) or (self.car_pos[0] ==self.init_lane-61):
                            self.change_lane = 0
                            print("change right")   
                        return ["SPEED","MOVE_RIGHT"]
                    elif self.command == 2:
                        if (self.car_pos[0]==self.init_lane-10) or (self.car_pos[0] == self.init_lane-9) or (self.car_pos[0] == self.init_lane-11):
                            self.change_lane = 0
                            print("change left")
                        return ["SPEED","MOVE_LEFT"]
                    elif self.command == 3:
                        self.change_lane = 0
                        return ["NONE"]
                
                    
                        
                    
                
            def move(car_grid,coin_grid,position_ahead,speed_ahead): 
                if self.player_no == 0 :
                    #print (self.car_pos[0])
                    #print("coin_grid")
                    #print(coin_grid)
                    #print("car_grid")
                    print (car_grid)
                    print (self.init_lane)
                    #print ("car lane:")
                    #print (self.car_lane)
                    """print ("car pos:")
                    print (self.car_pos[0])
                    print ("left")
                    print(self.lanes[self.target_lane_left])
                    print ("right")
                    print(self.lanes[self.target_lane_right])
                    print (self.init_lane)
                    print (self.car_pos[0])"""

                #print (self.done)
                
                if len(car_grid) == 0 and len(coin_grid) == 0:
                    if self.done == 0:
                        self.init_lane=self.lanes[self.car_lane]
                        self.done = 1
                    return goto(destination=self.init_lane-36)
                else:
                    if position_ahead<200:
                        if (9 in car_grid) and (8 not in car_grid) and (11 not in car_grid) and self.init_lane<595:
                            print("emergency right1")
                            if self.change_lane == 0:
                                self.init_lane=abs(self.init_lane + 70)
                                self.change_lane = 1
                            self.command = 1 
                        elif (9 in car_grid) and (7 not in car_grid) and (10 not in car_grid) and self.init_lane>105:
                            print("emergency left2")
                            if self.change_lane == 0:
                                self.init_lane=abs(self.init_lane - 70)
                                self.change_lane = 1
                            self.command = 2
                        if position_ahead<150:
                            print("BRAKE")
                            """if scene_info["frame"]%2 == 0:
                                return ["BRAKE"]
                            else:"""
                            return set_speed(target_speed=speed_ahead)
                        
                        

                             
                    if (5 not in car_grid and 7 not in car_grid and position_ahead>150):
                        if (5 in coin_grid or 7 in coin_grid):
                            print("eat left coin")
                            return goto(destination=self.init_lane-63)
                
                    if (6 not in car_grid and 8 not in car_grid and position_ahead>150):
                        if (6 in coin_grid or 8 in coin_grid):
                            print("eat right coin")
                            return goto(destination=self.init_lane-9)

                    if (5 in car_grid) and (6 in car_grid):
                        return set_speed(target_speed=speed_ahead)

                    if ((1 in car_grid) and (4 in car_grid) and (3 not in car_grid) and (5 not in car_grid)) or ((1 in car_grid) and (6 in car_grid) and (3 not in car_grid) and (5 not in car_grid)):
                        if (5 not in car_grid) and (7 not in car_grid) and self.init_lane>105:
                            print ("change left lane 1")
                            if self.change_lane == 0:
                                self.init_lane=abs(self.init_lane - 70)
                                self.change_lane = 1
                            self.command = 2
                    if ((2 in car_grid) and (3 in car_grid) and (4 not in car_grid) and (6 not in car_grid)) or ((2 in car_grid) and (5 in car_grid) and (4 not in car_grid) and (6 not in car_grid)):
                        if (6 not in car_grid) and (8 not in car_grid) and self.init_lane<595:
                            print("change right lane 1")
                            if self.change_lane == 0:
                                self.init_lane=abs(self.init_lane + 70)
                                self.change_lane = 1
                            self.command = 1 
                    if ((1 in car_grid) and (2 in car_grid)):
                        if self.car_lane == 0 or self.car_lane == 1 or self.car_lane ==2 or self.car_lane ==3:
                            if (6 not in car_grid) and (8 not in car_grid) and self.init_lane<595:
                                print("change right lane 2")
                                if self.change_lane == 0:
                                    self.init_lane=abs(self.init_lane + 70)
                                    self.change_lane = 1
                                self.command = 1
                            elif (5 not in car_grid) and (7 not in car_grid) and self.init_lane>105:
                                if self.change_lane == 0:
                                    print("change left lane 2")
                                    self.init_lane=abs(self.init_lane - 70)
                                    self.change_lane = 1
                                self.command = 2
                            else:
                                self.command = 3
                        else:
                            if (5 not in car_grid) and (7 not in car_grid) and self.init_lane>105:
                                print("change left lane 3")
                                if self.change_lane == 0:
                                    self.init_lane=abs(self.init_lane - 70)
                                    self.change_lane = 1
                                self.command = 2     
                            elif (6 not in car_grid) and (8 not in car_grid) and self.init_lane<595:
                                print("change right lane 3")
                                if self.change_lane == 0:
                                    self.init_lane=abs(self.init_lane + 70)
                                    self.change_lane = 1
                                self.command = 1 
                            else:
                                self.command = 3
                    
                    

                    elif (5 not in car_grid) and (6 not in car_grid) and (7 not in car_grid) and (8 not in car_grid):
                        return goto(destination=self.init_lane-36)
                    elif ((5 in car_grid) and (6 not in car_grid) and (8 not in car_grid)) or ((5 in car_grid) and (7 in car_grid) and (6 not in car_grid) and (8 not in car_grid)):
                        print("dodge to right")
                        return goto(destination=self.init_lane-9)
                    elif ((6 in car_grid) and (5 not in car_grid) and (7 not in car_grid)) or ((6 in car_grid) and (8 in car_grid) and (5 not in car_grid) and (7 not in car_grid)):
                        print("dodge to left")
                        return goto(destination=self.init_lane-63)
                    
                    
                    #elif ((5 in car_grid) and (6 in car_grid)) or ((5 in car_grid) and (8 in car_grid)) or ((6 in car_grid) and (7 in car_grid)) or ((9 in car_grid) and (7 in car_grid) and (8 in car_grid)):
                        #print("BRAKE")
                        #if scene_info["frame"]%2 == 0:
                            #return ["BRAKE"]
                        #else:
                            #return ["NONE"]
                    
                    
                    else:
                        return ["SPEED"]
                                           
            def goto(destination):
                if self.car_pos[0]>destination:
                    return ["SPEED","MOVE_LEFT"]
                elif self.car_pos[0]<destination:
                    return ["SPEED","MOVE_RIGHT"]
                else:
                    return ["SPEED"]

            def set_speed(target_speed):
                if self.car_vel>target_speed:
                    return ["BRAKE"]
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
        global alive
        alive =True
        pass
