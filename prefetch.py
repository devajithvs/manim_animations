from manimlib import *
import numpy as np

class MovingAround(Scene):
    CONFIG = {
        "cache_line" : 64,
        "vector_size" : 4096,
        "prefetch_length" : 128,
    }

    def construct(self):
        square = []
        i = 0
        square.append(Square(color=BLUE, fill_opacity=1))
        square[i].shift(LEFT).scale(0.09)
        for i in range(1,self.CONFIG["vector_size"]//self.CONFIG["cache_line"]):
            square.append(Square(color=BLUE, fill_opacity=1))
            square[i].next_to(square[i-1], RIGHT)
            square[i].shift(LEFT).scale(0.09)
        group = VGroup(*square)
        self.add(group.scale(0.5))

        self.play(group.animate.shift(LEFT * 10 + UP * 2.5))

        prefetch = dict()
        for i,elem in enumerate(square):
            prefetch_elem = i+self.CONFIG["prefetch_length"]//self.CONFIG["cache_line"]
            prefetch_elem2 = i+2*self.CONFIG["prefetch_length"]//self.CONFIG["cache_line"]
            prefetch_elem3 = i+4*self.CONFIG["prefetch_length"]//self.CONFIG["cache_line"]
            if i in prefetch:
                color = GREEN
            else:
                color = RED
            prefetch[prefetch_elem] = True
            prefetch[prefetch_elem2] = True
            prefetch[prefetch_elem3] = True
            
            # if prefetch_elem3 < len(square):
            #     self.play(elem.animate.set_color(color), square[prefetch_elem].animate.set_color(YELLOW), square[prefetch_elem2].animate.set_color(YELLOW), square[prefetch_elem3].animate.set_color(YELLOW), run_time=0.1)
            # elif prefetch_elem2 < len(square):
            #     self.play(elem.animate.set_color(color), square[prefetch_elem].animate.set_color(YELLOW), square[prefetch_elem2].animate.set_color(YELLOW), run_time=0.1)
            # elif prefetch_elem < len(square):
            if prefetch_elem < len(square):
                self.play(elem.animate.set_color(color), square[prefetch_elem].animate.set_color(YELLOW), run_time=0.1)
            else:
                if i in prefetch:
                    self.play(elem.animate.set_color(GREEN), run_time=0.1)
                else:
                    self.play(elem.animate.set_color(RED), run_time=0.1)
