import tkinter as tk

class UserInput(object):
    """Stores basic variables of tkinter GUI (label names and various settings)"""
    def __init__(self, label_names, dropdown_options,
                resolution = 0, cmap = 0, interpolation_method = 2, color_norm = 1, show_julia = 0, 
                max_iter = 100, unique_colors = 4000):
        """Constructor of UserInput class instance
                
        Args
        ----
        label_names: string
            string to be display the label for each setting in the tkinter window
        dropdown_options: string
            populates dropdown settings with strings from list of options
        resolutions, cmap, interpolation_method, color_norm, show_julia: int
            default value for each dropdown fractal setting option when tkinter window is first generated; integer references 
            list to generate actual value displayed
        max_iter, unique_colors: int
            default value for each slider fractal setting option when tkinter window is first generated
        """
        self.label_names = label_names
        self.dropdown_options = dropdown_options
        self.dropdown_values = [resolution, cmap, interpolation_method, color_norm, show_julia]
        self.slider_values = [max_iter, unique_colors]

    def create_frame(self):
        """Create tkinter frame
        
        Returns
        -------
        basic frame object representing tkinter window
        """
        frame = tk.Tk()
        frame.title('Fractal Inputs')
        frame.geometry('450x400')
        return frame

    def get_inputs(self):
        """Return instance variables (resolution reformatted into width & height)
        
        Returns
        -------
        width, height: int
            updated resolution of the window
        dropdown_values, slider_values: str
            instance variables for sliders
        """
        res = self.dropdown_options[0][self.dropdown_values[0]].split(' ')
        res = res[0].split('x')
        width, height = int(res[0]), int(res[1])
        return (width, height, self.dropdown_values, self.slider_values)
        
    def build_layout(self, frame):
        """Creates tkinter objects to be displayed (labels, dropdowns, sliders) as well as update button
        
        Args
        ----
        frame: object
            the frame on which the tkinter is currently displayed
        """
        labels = self.create_labels(frame, "comicsans", 12)
        txtfields, dropdowns = self.create_dd(frame)
        slider1 = tk.Scale(frame, from_=1, to=5000, orient=tk.HORIZONTAL)
        slider2 = tk.Scale(frame, from_=2, to=5000, orient=tk.HORIZONTAL)
        slider1.set(self.slider_values[0])
        slider2.set(self.slider_values[1])
        sliders = [slider1, slider2]
        self.place_objects(labels, dropdowns, sliders, .08, .05)
        update_button = tk.Button(frame, text='Update Fractal', 
                        command=lambda:self.update_button_clicked(frame, txtfields, sliders), 
                        font=("comicsans", 12))
        update_button.pack(fill='x', side='bottom', pady = 25)

    def create_labels(self, frame, font, font_size):
        """Create tkinter labels (description of dropdown / sliders)
           
        Args
        ----
        frame: object
            the frame on which the tkinter is currently displayed
        font: str
            font type used to generate text in tkinter window
        font_size: int
            font size used to generate text in tkinter window

        Returns 
        -------
        labels: list of tuples
            contains formatting setting for each label
        """
        labels = []
        for val in self.label_names:
            label = tk.Label(frame, text=val, font=(font, font_size))
            labels.append(label)
        return labels

    def create_dd(self, frame):
        """Create tkinter dropdown objects

        Args
        ----
        frame: object
            the frame on which the tkinter is currently displayed

        Returns 
        -------
        txtfields: list of strings
            contains text options for each dropdown menu
        dropdowns: list of tuples
            generates each dropdown menu for the tkinter window
        """
        txtfields = []
        dropdowns = []
        for idx, lst in enumerate(self.dropdown_options):
            txtfield = tk.StringVar(frame)
            txtfield.set(lst[self.dropdown_values[idx]])
            txtfields.append(txtfield)
            dropdown = tk.OptionMenu(frame, txtfield, *lst)
            dropdowns.append(dropdown)
        return txtfields, dropdowns

    def place_objects(self, labels, dropdowns, sliders, x, y):
        """Place tkinter objects
        
        Args
        ----
        labels: list of tuples
            contains formatting setting for each label
        dropdowns: list of tuples
            contains formatting setting for each dropdown menu
        sliders: list of tuples
            contains formatting setting for each slider
        x, y: float
            coordinates of each object in tkinter window
        """
        objects = dropdowns + sliders # move outside of function (join lists when calling function)
        for idx, label in enumerate(labels):
            label.place(relx = x, rely = y)
            if idx < len(dropdowns):
                y2 = y
            else:
                y2 = y - 0.04
            objects[idx].place(relx = x + 0.42, rely = y2)
            y += 0.12

    def update_button_clicked(self, frame, dropdowns, sliders):
        """When update button clicked (1) update instance variables and (2) close tkinter frame
        
        Args
        ----
        frame: object
            the frame on which the tkinter is currently displayed
        dropdowns: list of tuples
            current formatting setting for each dropdown menu
        sliders: list of tuples
            current formatting setting for each slider
        """
        for idx, dropdown in enumerate(dropdowns):
            self.dropdown_values[idx] = self.dropdown_options[idx].index(dropdown.get())
        for idx, slider in enumerate(sliders):
            self.slider_values[idx] = slider.get()
        frame.destroy()