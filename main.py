# import own .py files
from pygameGUI.GUI import GUI, Button
from pygameGUI.user_input import UserInput
from fractals.fractals import Mandelbrot, JuliaSet

# import external packages
import pygame

def fetch_options():
    """Return all available options that can be selected in the tkinter settings window."""
    label_names = ['Resolution:', 'Color Scheme:', 'Color Interpolation:', 'Color Selection based on:',
            'Julia Set:', 'Iterations:', 'Number of Colors:']
    resolution_options = ['1280x960 (4:3)', '1440x1080 (4:3)', '1920x1440 (4:3)', '1280x720 (16:9)', '1600x900 (16:9)', '1920x1080 (16:9)']
    cmap_options = ['blues, whites & oranges', 'orange, white & blue', 'pink & blue', 'lime', 'aqua & black']
    interpolation_options = ['linear','cubic (akima)','cubic (pchip)']
    color_norm_options = ['simple iteration count','smoothed iteration count']
    show_julia_options = ['disabled', 'enabled']
    return label_names, (resolution_options, cmap_options, interpolation_options, color_norm_options, show_julia_options)

def show_ui(label_names, options, var):
    """Open tkinter settings window.
    
    Args
    ----
    label_names: list[str]
        contains the descriptions of the different dropdown menus & sliders
    options: tuple of 5 lists of strings
        contains all options for the 5 dropdown menus
    var: tuple of currently selected options

    Returns
    -------
    ui: Class Instance of UserInput
        stores previously selected values until settings window is opened again
    """
    ui = UserInput(label_names, options, var[2][0], var[2][1], var[2][2], var[2][3], var[2][4], var[3][0], var[3][1])
    frame = ui.create_frame()
    ui.build_layout(frame)
    frame.mainloop()
    return ui

def create_buttons(var):
    """Create buttons and place them based on current resolution
    
    Args
    ----
    var: tuple of currently selected options

    Returns
    -------
    Different lists of buttons (so we can easily show the currently required buttons on the screen)
    """
    button_settings = Button((255, 255, 255), (0, 0, 0), 0.01*var[0], 0.01*var[0], 200, 50, 'open settings')
    button_quit = Button((255, 255, 255), (0, 0, 0), 0.01*var[0], 0.01*var[0] + 60, 200, 50, 'exit game')
    button_zoom_instructions = Button((255, 255, 255), (0, 0, 0), 0.01*var[0], 0.92*var[1], 0.98*var[0], 50, 
                                'Instructions: (1) left-click to zoom in, (2) right-click to zoom out, (3) middle-click to move')
    button_julia_instructions = Button((255, 255, 255), (0, 0, 0), 0.01*var[0], 0.92*var[1], 0.98*var[0], 50,
                                'Instructions: move mouse over Mandelbrot to see corresponding Julia set; zoom as before')
    button_settings_open = Button((255, 255, 255), (255, 0, 0), 0.01*var[0], 0.92*var[1], 0.98*var[0], 50,
                                'Close settings to continue fractal exploration.')
    buttons_set_zoom = [button_settings, button_quit, button_zoom_instructions]
    buttons_set_julia = [button_settings, button_quit, button_julia_instructions]
    buttons_set_open = [button_settings, button_quit, button_settings_open]
    buttons_all = [button_settings, button_quit, button_zoom_instructions, button_julia_instructions, button_settings_open]
    return buttons_all, buttons_set_zoom, buttons_set_julia, buttons_set_open

def show_buttons(screen, buttons):
    """Take the given buttons and display them

    Args
    ----
    screen: pygame screen
        the screen on which the game is currently displayed
    buttons: list of buttons
        the buttons we want to display on the screen
    """
    for i in buttons:
        i.show(screen)
    pygame.display.update()

def update_resolution(gui, screen, var):
    """Create new pygame display if user changed resolution
    
    Args
    ----
    gui: Class Instance of GUI
    screen: pygame screen
        the screen on which the game is currently displayed
    var: tuple of currently selected options
    
    Returns
    -------
    gui: Class Instance of GUI
    screen: pygame screen
        the screen on which the game is to be displayed
    update: boolean
        whether the resolution was changed and we consequently had to re-initialize gui and screen
    """
    update = False
    if gui.width != var[0] or gui.height != var[1]:
        pygame.display.quit()
        gui = GUI('Mandelbrot', var[0], var[1])
        screen = pygame.display.set_mode((var[0], var[1]))
        update = True
    return gui, screen, update

def display_fractal(fractal, gui, screen, var, pg_x = 0, pg_y = 0, c_x = 0, c_y = 0):
    """Update fractal with current settings, recalculate and show it in pygame
    
    Args
    ----
    fractal: class instance of Fractal
    gui: Class Instance of GUI
    screen: pygame screen
        the screen on which the game is currently displayed
    var: tuple of currently selected options#
    pg_x, pg_y: integer
        pygame coordinates that denote from where on we will show the given fractal on the given screen (default = 0 as we usually start in top left corner)
    c_x, c_y: integer
        complex coordinates of a point selected by the user (used to update JuliaSet; default = 0)
    """
    # update fractal variables
    if var[2][4] == 1:
        fractal.width = int(var[0]/2)
    elif var[2][4] == 0:
        fractal.width = int(var[0])
    fractal.height = var[1]
    fractal.max_iter = var[3][0]
    if isinstance(fractal, JuliaSet): # update with chosen C value if fractal is a JuliaSet
        fractal.max_iter = 200 # no need for very high max_iter values as zoom is disabled (override user setting)
        fractal.C = c_x + c_y *1j
    # calculate fractal
    m, ms = fractal.calc()
    mu_rgb = fractal.color_fractal(m, ms, var[2][1], var[3][1], var[2][2], var[2][3])
    # blit to screen
    surface = gui.make_surface(mu_rgb)
    screen.blit(surface, (pg_x, pg_y))

def zoom_fractal(lmr_click, fractal, point):
    """Zoom / move fractal on screen depending on type of mouseclick (left / middle / right)
    
    Args
    ----
    lmr_click: integer
        pygame mouseclick identification (1 == left-click; 2 == mid-click; 3 == right-click)
    fractal: class instance of Fractal
    point: tuple of 2 integer
        pygame coordinates of a point selected by the user
    """
    c_x, c_y = fractal.get_coord(point)
    if lmr_click == 1:
        fractal.zoom((c_x, c_y), 3.0)
    elif lmr_click == 2:
        fractal.zoom((c_x, c_y), 1.0)
    elif lmr_click == 3:
        fractal.zoom((c_x, c_y), 0.33)

def main():
    run = True
    label_names, options = fetch_options()
    var = (1280, 960, [0, 0, 2, 1, 0], [100, 4000]) # default settings when program is started
    ui = show_ui(label_names, options, var) # open settings
    var = ui.get_inputs() # read chosen settings

    # initialise pygame
    pygame.init()
    buttons_all, buttons_set_zoom, buttons_set_julia, buttons_set_open = create_buttons(var)
    current_tick = 0
    next_tick = 0

    # initialise fractals
    gui = GUI('Mandelbrot', var[0], var[1])
    screen = pygame.display.set_mode((var[0], var[1]))
    mandel = Mandelbrot(var[0], var[1], var[3][0])
    display_fractal(mandel, gui, screen, var)
    julia = JuliaSet(int(var[0]/2), var[1], var[3][0])

    show_buttons(screen, buttons_set_zoom)
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons_all[0].isOver(event.pos): # open settings
                show_buttons(screen, buttons_set_open)
                ui = show_ui(label_names, options, var) # open settings
                var = ui.get_inputs() # read selected settings
                gui, screen, update = update_resolution(gui, screen, var)
                if update == True: # if new resolution selected
                    buttons_all, buttons_set_zoom, buttons_set_julia, buttons_set_open = create_buttons(var)
                display_fractal(mandel, gui, screen, var)
                if var[2][4] == 0:
                    show_buttons(screen, buttons_set_zoom)
                elif var[2][4] == 1:
                    display_fractal(julia, gui, screen, var, var[0]/2, 0, julia.C.real, julia.C.imag)
                    show_buttons(screen, buttons_set_julia)

            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons_all[1].isOver(event.pos)) or event.type == pygame.QUIT: # exit game
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button <= 3: # zoom
                point = event.pos
                if var[2][4] == 1 and point[0] < int(var[0]/2): # if Julia enabled, limit points that mandelbrot can be zoomed at
                    zoom_fractal(event.button, mandel, point)
                    display_fractal(mandel, gui, screen, var)
                    show_buttons(screen, buttons_set_julia)      
                elif var[2][4] == 0:
                    zoom_fractal(event.button, mandel, point)
                    display_fractal(mandel, gui, screen, var)
                    show_buttons(screen, buttons_set_zoom)               

            elif var[2][4] == 1 and event.type == pygame.MOUSEMOTION: # update julia set
                point = event.pos
                current_tick = int(pygame.time.get_ticks())
                
                if current_tick > next_tick and point[0] < int(var[0]/2): # if mouse hovers above mandelbrot, update julia set every 15 ms (roughly 60fps)
                    next_tick += 15
                    c_x, c_y = mandel.get_coord(point)
                    display_fractal(julia, gui, screen, var, var[0]/2, 0, c_x, c_y)
                    show_buttons(screen, buttons_set_julia)

        pygame.display.update()
    
    pygame.quit()
    quit()

if __name__=='__main__':
    main()