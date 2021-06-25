from mesa import Agent,Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import math
import config
import utils

possible_directions=[(-1,0),(-1,1),(-1,-1),(0,1),(0,-1),(1,1),(1,0),(1,-1)]

class FlockingAgent(Agent):

    def __init__(self, unique_id,x,y,dir,model):
        super().__init__(unique_id, model)
        self.dir=dir
        self.avoidance_malus=False

    def move(self):
        x,y=self.pos
        dx,dy=self.dir
        self.model.grid.move_agent(self,(x+dx,y+dy)) 

    def avoid(self,dir):  #regola 1 
        dx,dy=dir
        x,y=self.pos
        avoid_direction=(0,0)

        if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x-dx,y-dy))): #opposite side
            avoid_direction=(-dx,-dy)
        else:
            if dx==0:
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x-1,y))):
                    avoid_direction=(-1,0)
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x+1,y))):
                    avoid_direction=(1,0)
                for i in [-1,1]:
                    for j in [-1,1]:
                          if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x+i,y+j))):
                              avoid_direction=(i,j)
            elif dy==0:
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x,y+1))):
                    avoid_direction=(0,1)
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x,y-1))):
                    avoid_direction=(0,-1)
                for i in [-1,1]:
                    for j in [-1,1]:
                          if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x+i,y+j))):
                              avoid_direction=(i,j)
                              break
            elif self.dir==(-1,1) or self.dir==(1,-1):
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x+1,y+1))):
                     avoid_direction=(1,1)
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x-1,y-1))):
                     avoid_direction=(-1,-1)
                for i in [-1,1]:
                          if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x+i,y))):
                              avoid_direction=(i,0)
                              break
                for j in [-1,1]:
                          if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x,y+j))):
                              avoid_direction=(0,j)
                              break
            else: 
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x-1,y+1))):
                    avoid_direction=(-1,1)
                if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x+1,y-1))):
                    avoid_direction=(1,-1)
                for i in [-1,1]:
                          if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x+i,y))):
                              avoid_direction=(i,0)
                              break
                for j in [-1,1]:
                          if self.model.grid.is_cell_empty(self.model.grid.torus_adj((x,y+j))):
                              avoid_direction=(0,j)
                              break
        return avoid_direction

    def aproach(self): #regola 3

        aproach_direction=(0,0)

        possible_flockmates = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=config.aproach_radius
        )

        if len(possible_flockmates)!=0:

            sum_x=0
            sum_y=0
            count=0

            for birds in possible_flockmates:
                    if birds.avoidance_malus:
                        continue 
                    pos_x,pos_y=birds.pos
                    sum_x=sum_x+pos_x
                    sum_y=sum_y+pos_y
                    count=count+1

            if count==0:
                aproach_direction=(0,0)        
            else:
                center=(math.floor(sum_x/count),math.floor(sum_y/count))
                aproach_direction=utils.get_direction(self.pos,center,self.model.grid.width,self.model.grid.height)    
        
        return aproach_direction

    def align(self):   #regola 2
        
        align_direction=(0,0)

        flockmates= self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=config.align_radius
        )

        if len(flockmates)!=0:

            directions=[0,0,0,0,0,0,0,0]
            no_sort_directions=[0,0,0,0,0,0,0,0]

            for bird in flockmates: 
                if bird.avoidance_malus:
                    continue
                index=possible_directions.index(bird.dir)
                directions[index]=directions[index]+1/utils.get_distance(self.pos,bird.pos,True,self.model.grid.width,self.model.grid.height)
                no_sort_directions[index]=no_sort_directions[index]+1/utils.get_distance(self.pos,bird.pos,True,self.model.grid.width,self.model.grid.height)
            
            directions.sort(reverse=True)
            max_value=directions[0]
            ind=no_sort_directions.index(max_value)
            align_direction=possible_directions[ind]

        return align_direction


    def step(self):

        if self.avoidance_malus:
            self.avoidance_malus=False

        neighbors= self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=config.avoid_radius
        )

        new_direction=self.dir

        if len(neighbors)!=0:
            if len(neighbors)!=8:
                conflict_dir=utils.get_direction(self.pos,neighbors[0].pos,self.model.grid.width,self.model.grid.height)
                new_direction=self.avoid(conflict_dir)
                self.avoidance_malus=True
        else:
            neighbors= self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=config.aproach_radius
            )
            if len(neighbors)!=0:
                align_direction=self.align()
                aproach_direction=self.aproach()
                if align_direction==(0,0):
                    new_direction=aproach_direction
                else:
                    new_direction=utils.calculate_resulting_dir(align_direction,aproach_direction)

        if new_direction!=(0,0):              
            self.dir=new_direction
            
        self.move()

class FlockingModel(Model):

    def __init__(self,N,width,height):

        self.grid=MultiGrid(width,height,True)
        self.schedule=RandomActivation(self)
        self.running=True
        sum_x=0
        sum_y=0

        for i in range(N):
            
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            dir=self.random.choice(possible_directions)
            agent = FlockingAgent(i,x,y,dir,self)
            self.schedule.add(agent)
            self.grid.place_agent(agent,(x, y))

    def step(self):
        self.schedule.step()
    



