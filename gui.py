import imgui
from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import pygame
import sys
import random
from Board import board_cmp, generateRandomBoardsFromColorMap, crossover_population, do_mutate
import functools


class GUIState:
    def __init__(self):
        self.sidelen = 8
        self.grid = [[0 for _ in range(8)] for _ in range(8)]
        self.current_color_selection = 0
        self.is_solving = False
        self.best_fitness = 999
        self.generation = 0
        self.population = []
        self.best_board = None


pal_colors = [(0,1,0), (1,0,0), (1,1,0), (0,0,1), (1,0,1), (0,1,1), (1,1,1), (0,0,0), (0.18,0.10,0.20), (1,0.64, 0)]

state = GUIState()

def main():
    pygame.init()
    size = 1000, 800 
    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    imgui.create_context()
    impl = PygameRenderer()
    
    sort_key = functools.cmp_to_key(board_cmp)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            impl.process_event(event)

        width, height = pygame.display.get_window_size()
        imgui.get_io().display_size = (width, height)
        impl.process_inputs()
        imgui.new_frame()

        imgui.set_next_window_size(300, 750)
        imgui.set_next_window_position(10, 10)
        imgui.begin("select current color")
        
        changed, state.sidelen = imgui.input_int("Side Length (N)", state.sidelen)
        if changed:
            state.sidelen = max(2, min(14, state.sidelen)) 
            state.grid = [[0 for _ in range(state.sidelen)] for _ in range(state.sidelen)]

        imgui.separator()
        imgui.text("Color Palette")
        for i, (r,g,b)  in enumerate(pal_colors):
            imgui.push_id(str(f"palette_{i}"))
            if imgui.color_button(f"Color {i}", r, g, b, 1.0, width=30, height=30):
                state.current_color_selection = i
            if (i+1) %3 != 0: imgui.same_line()
            imgui.pop_id()

        imgui.separator()
        if imgui.button("run genetic algorithm", width=280, height=40):
            state.is_solving = True
            state.generation = 0
            num_colors = max(max(row) for row in state.grid) + 1
            state.population = generateRandomBoardsFromColorMap(
                numDesired=1000, 
                sidelen=state.sidelen, 
                numColors=num_colors, 
                colormap=state.grid
            )
            state.population.sort(key=sort_key)
            state.best_fitness = state.population[0].fitness

        if state.is_solving:
            imgui.text_colored(f"Generation: {state.generation}", 0.2, 1.0, 0.2)
            imgui.text(f"Best Fitness: {state.best_fitness}")
            if imgui.button("Stop Solver"): state.is_solving = False
            
            crossover_population(state.population)
            do_mutate(state.population)
            state.population.sort(key=sort_key)
            
            state.generation += 1
            state.best_fitness = state.population[0].fitness
            state.best_board = state.population[0]
            
            if state.best_fitness == 0:
                state.is_solving = False

        imgui.end()

        imgui.set_next_window_size(600, 600)
        imgui.set_next_window_position(320, 10)
        imgui.begin("Board Editor")
        
        cell_size = 500 // state.sidelen
        

        for r in range(state.sidelen):
            for c in range(state.sidelen):
                imgui.push_id(f"cell_{r}_{c}")
                
                color_idx = state.grid[r][c]
                cur_r, cur_g, cur_b = pal_colors[color_idx]
                
                label = "##tile"
                if state.best_board and state.best_board.rep[r][c].hasQueen():
                    label = "Q"

                imgui.push_style_color(imgui.COLOR_BUTTON, cur_r, cur_g, cur_b)
                if imgui.button(f"{label}", width=cell_size, height=cell_size):
                    state.grid[r][c] = state.current_color_selection
                imgui.pop_style_color()
                
                if c < state.sidelen - 1:
                    imgui.same_line()
                imgui.pop_id()
        
        imgui.end()

        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()



if __name__ == "__main__":
    main()
