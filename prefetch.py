from manimlib import *
import numpy as np

class MovingAround(Scene):
    CONFIG = {
        "cache_line" : 64,
        "rows" : 10,
        "vector_size" : 4096,
        "prefetch_length" : 128,
    }

    def construct(self):
        rows = []
        groups = []
        for row_num in range(self.CONFIG["rows"]):
            square = []
            for i in range(self.CONFIG["vector_size"]//self.CONFIG["cache_line"]):
                square.append(Square(color=BLUE, fill_opacity=1))
                if i >= 1:
                    square[i].next_to(square[i-1], RIGHT)
                square[i].shift(LEFT).scale(0.09).scale(0.5)
            group = VGroup(*square)
            if len(groups) > 1:
                group.next_to(groups[-1], BOTTOM)
            groups.append(group)
            rows.append(square)

        matrix = VGroup(*groups)
        self.add(matrix)

        self.play(matrix.animate.shift(LEFT * 10 + UP * 5), run_time=0)

        prefetch = dict()
        for j,square in enumerate(rows):
            for i,elem in enumerate(square):
                print(i)
                prefetch_elem = j*len(square)+i+self.CONFIG["prefetch_length"]//self.CONFIG["cache_line"]
                prefetch_elem2 = j*len(square)+i+2*self.CONFIG["prefetch_length"]//self.CONFIG["cache_line"]
                prefetch_elem3 = j*len(square)+i+4*self.CONFIG["prefetch_length"]//self.CONFIG["cache_line"]
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
                if prefetch_elem -j*len(square) < len(square):
                    i_prefetch, j_prefetch = prefetch_elem%len(square), prefetch_elem//len(square)
                    print(i,j, i_prefetch, j_prefetch)
                    self.play(rows[j+1][i].animate.set_color(color), rows[j_prefetch+1][i_prefetch].animate.set_color(YELLOW), run_time=0.1)
                else:
                    if i in prefetch:
                        self.play(elem.animate.set_color(GREEN), run_time=0.1)
                    else:
                        self.play(elem.animate.set_color(RED), run_time=0.1)
