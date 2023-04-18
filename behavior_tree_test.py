from utils import Pose
from constants import FREQUENCY, SAMPLE_TIME, SCREEN_HEIGHT, SCREEN_WIDTH, PIX2M, M2PIX
from roomba import Roomba
from simulation import *
from behavior_tree import RoombaBehaviorTree
import numpy as np

def simulacao(move_foward_time, move_in_spiral_time, go_back_time, spiral_factor, initial_radius_spiral):

    behavior = RoombaBehaviorTree(move_foward_time, move_in_spiral_time, go_back_time, spiral_factor, initial_radius_spiral)
    pose = Pose(PIX2M * SCREEN_WIDTH / 2.0, PIX2M * SCREEN_HEIGHT / 2.0, 0.0)
    roomba_radius = 0.34/2.0
    roomba = Roomba(pose, 1.0, 2.0, roomba_radius, behavior)

    # Notacao:
    # 0: não foi limpo
    # 1: já foi limpo
    
    pixeis_totais = SCREEN_HEIGHT*SCREEN_WIDTH
    
    n = 3  # número de amostras da simulação utilizadas para cálculo do tempo médio
    tempo = n * [0]
    for k in range(len(tempo)):
        roomba.pose = Pose(PIX2M * SCREEN_WIDTH / 2.0, PIX2M * SCREEN_HEIGHT / 2.0, 0.0)
        simulation = Simulation(roomba)
        
        pygame.init()

        window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pygame.display.set_caption("Exame")

        clock = pygame.time.Clock()
        
        limpeza = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH))
        t = 0
        run = True
        while run:
            clock.tick(FREQUENCY)
            for i in range(3000):
                if t > 300:
                    tempo[k] = t
                    run = False
                    break
                    
                for height in range(int(roomba_radius*M2PIX + 1)):
                    for width in range(int(roomba_radius*M2PIX + 1)):
                        limpeza[int(roomba.pose.position.y*M2PIX - (roomba_radius*M2PIX + 1)/2 + width)][int(roomba.pose.position.x*M2PIX - (roomba_radius*M2PIX + 1)/2 + height)] = 1
                if np.count_nonzero(limpeza)/pixeis_totais >= 0.6:
                    tempo[k] = t
                    run = False
                    break
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                t += SAMPLE_TIME
                simulation.update()
                draw(simulation, window)

        pygame.quit()
    print('Média: ',np.mean(tempo),'Tempos: ',tempo)
    return np.mean(tempo)

