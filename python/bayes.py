#!/usr/bin/env python3.7
# this is a program i wrote using the Real World Python book

import sys
import random
import·itertools
import numpy as np
import·cv2 as cv

##### global variables - start

MAP_FILE = 'cape_python.png'

SA1_CORNERS = (130, 265, 180, 315)  # (UL-X, UL-Y, LR-X, LR-Y)
SA2_CORNERS = (80, 255, 130, 305) # (UL-X, UL-Y, LR-X, LR-Y)
SA3_CORNERS = (105, 205, 155, 255) # (UL-X, UL-Y, LR-X, LR-Y)

##### global variable - stop



##### function and class declerations start

class Search ():
    """Bayesian Search & Rescue game with 3 search areas"""

    # Creating a method that will be run whenever an object is instantiated
    def __init__(self, name):
        # Setting some attributes that will be unique to each object. "self" is a reference to the instance of the class that is being created, or that a method was invoded on
        self.name = name
        # Adds color to this grayscale image
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        # Checks to see if files exists. "file=sys.stderr" makes the error code the color Red in the Python interpreter window
        if self.img is None:
            print('Could not load map file {}'.format(MAP_FILE),
                file=sys.stderr)
            sys.exit(1)
        
        # Setting some attributes for when the sailor is found. These are just placeholders for now
        # This is the search area
        self.area_actual = 0
        # This is the precise location
        self.sailor_actual = [0, 0] # As "local coords within a search area"
        # The map will be loaded as an array. Numpy can use a tool called vecotrization that can run operations on entire arrays rather than on individual elements.

        # Creating subarrays from the array that is the map so we can search within the search area. This is done with indexing.
        self.sa1 = self.img[SA1_CORNERS[1] : SA1_CORNERS[3],
                            SA1_CORNERS[0] : SA1_CORNERS[2]]

        self.sa2 = self.img[SA2_CORNERS[1] : SA2_CORNERS[3],
                            SA2_CORNERS[0] : SA2_CORNERS[2]]

        self.sa3 = self.img[SA3_CORNERS[1] : SA3_CORNERS[3],
                            SA3_CORNERS[0] : SA3_CORNERS[2]]

        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0

    
    def draw_map(self, last_known):
        """Display basemap with scale, last known xy location, search areas."""
        # This is the legen that you see on the bottom left
        cv.line(self.img, (20, 370), (70, 370), (0, 0, 0), 2)
        cv.putText(self.img, '0', (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '50 Nautical Miles', (71, 370),
                    cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        # These are the three squares/rectangles you see with the numbers 1, 2, and 3
        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]),
                               (SA1_CORNERS[2], SA1_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '1',
                    (SA1_CORNERS[0] + 3, SA1_CORNERS[1] + 15),
                    cv.FONT_HERSHEY_PLAIN, 1, 0)
        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1]),
                               (SA2_CORNERS[2], SA2_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '2',
                    (SA1_CORNERS[0] + 3, SA1_CORNERS[1] + 15),
                    cv.FONT_HERSHEY_PLAIN, 1, 0)
        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1]),
                               (SA3_CORNERS[2], SA3_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '3',
                    (SA1_CORNERS[0] + 3, SA1_CORNERS[1] + 15),
                    cv.FONT_HERSHEY_PLAIN, 1, 0)

        # This is the + sign that you see on the map showing the last know location
        cv.putText(self.img, '+', (last_known),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        # This is the legend at the bottom right
        cv.putText(self.img, '+ = Last Known Location', (274, 355),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '* = Actual Position', (275, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        # This line will show the base map
        cv.imshow('Search Area', self.img)
        # Moves this "Search Area" option to the upper right of the window
        cv.moveWindow('Search Area', 750, 10)
        # "Search Area" option shows up .5 seconds after the base map comes up
        cv.waitKey(500)
        
    def sailor_final_location(self, num_search_areas):
        """Return the actual x,y location of the missing sailor."""
        # Find sailor coordinates with respect to any Search Area subarray
        # selecting [0] means rows are used, [1] uses columns
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1], 1)
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0], 1)

       # triangular distribution that is somehow supposed to represent the areas that the sailor could be 
        area = int(random.triangular(1, num_search_areas + 1))

        if area == 1:
            x = self.sailor_actual[0] + SA1_CORNERS[0]
            y = self.sailor_actual[1] + SA1_CORNERS[1]
            self.area_actual = 1
        elif area == 2:
            x = self.sailor_actual[0] + SA2_CORNERS[0]
            y = self.sailor_actual[1] + SA2_CORNERS[1]
            self.area_actual = 2
        elif area == 3:
            x = self.sailor_actual[0] + SA3_CORNERS[0]
            y = self.sailor_actual[1] + SA3_CORNERS[1]
            self.area_actual = 3
        return x, y
    
    def calc_search_effectiveness(self):
        """ Set decimal search effectiveness value per search area. """
        self.sep1 = random.uniform(0.2, 0.9)
        self.sep2 = random.uniform(0.2, 0.9)
        self.sep3 = random.uniform(0.2, 0.9)

    def conduct_search(self, area_num, area_array, effectiveness_prob):
        """ Return the search results and list of searched coordinates """
        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])
        coords = list(itertools.product(local_x_range, local_y_range))
        random.shuffle(coords)
        coords = coords[:int(len(coords) * effectiveness_prob)]
        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])
        if area_num == self.area_actual and loc_actual in coords:
            return 'Found in Area {}.'.format(area_num), coords
        else:
            return 'Not Found', coords
            
    def revise_targe_probs(self):
        """ Update area target probablilities based on search effectiveness """ 
        denom = self.p1 * (1 - self.p1) + self.p2 * (1 - self.p2) + self.p3 * (1 - self.p3) 
        self.p1 = self.p1 * (1 - self.p1) / denom
        self.p1 = self.p2 * (1 - self.p2) / denom
        self.p1 = self.p3 * (1 - self.p3) / denom

    def draw_menu(search_num):
        """ Print menu of choices for conducting area seraches. """
        print('\nSearch {}'.format(search_num))
        print(
            """
            Choose next areas to search

            0 - Quit
            1 - Search Area 1 twice
            2 - Search Area 2 twice
            3 - Search Area 3 twice
            4 - Search Areas 1 & 2
            5 - Search Areas 1 & 3
            6 - Search Areas 2 & 3
            7 - Start Over
            """
        )

    

    


        

##### function and class declerations - stop



##### script - start



##### script - stop
