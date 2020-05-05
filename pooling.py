
from manimlib.imports import *
from manimlib.mobject.types.vectorized_mobject import VMobject

class Pooling(Scene):
    CONFIG = {
        "input_coords" : [],
        "output_coords" : [],
        "kernel_size" : 0,
        "stride" : 0,
        "title" : "max Pooling",
        "pooling" : "max",
    }

    def clear(self):
        self.input_coords = []
        self.output_coords = []
        return self

    def pool_init(self, kernel_size, stride, pooling_type, input_coords):
        self.kernel_size = kernel_size
        self.stride = stride
        self.pooling = pooling_type
        self.input_coords = input_coords


    def calculate_max_vector(self):
        l = 0
        while(l<len(self.input_coords)-self.kernel_size + 1):
            x_list = []
            m = 0
            while(m<len(self.input_coords)-self.kernel_size + 1):
                max = self.input_coords[0][0]
                for i in range(self.kernel_size):
                    for j in range(self.kernel_size):
                        if(max < self.input_coords[i+l][j+m]):
                            max = self.input_coords[i+l][j+m]
                m = m + self.stride
                x_list.append(max)
            l = l + self.stride
            self.output_coords.append(x_list)
    
    def calculate_min_vector(self):
        l = 0
        while(l<len(self.input_coords)-self.kernel_size + 1):
            x_list = []
            m = 0
            while(m<len(self.input_coords)-self.kernel_size + 1):
                min = self.input_coords[0][0]
                for i in range(self.kernel_size):
                    for j in range(self.kernel_size):
                        if(min > self.input_coords[i+l][j+m]):
                            min = self.input_coords[i+l][j+m]
                m = m + self.stride
                x_list.append(min)
            l = l + self.stride
            self.output_coords.append(x_list)

    def calculate_avg_vector(self):
        l = 0
        while(l<len(self.input_coords)-self.kernel_size + 1):
            x_list = []
            m = 0
            while(m<len(self.input_coords)-self.kernel_size + 1):
                sum = 0
                for i in range(self.kernel_size):
                    for j in range(self.kernel_size):
                        sum += self.input_coords[i+l][j+m]
                m = m + self.stride
                x_list.append(sum/(self.kernel_size*self.kernel_size))
            l = l + self.stride
            self.output_coords.append(x_list)

    def animate(self):
               
        if(self.pooling == "avg"):
            self.calculate_avg_vector()
        elif(self.pooling == "min"):
            self.calculate_min_vector()
        else:
            self.calculate_max_vector()
        in_vect = Matrix(self.input_coords)
        out_vect = Matrix(self.output_coords)
        in_vect.set_color(BLUE)
        out_vect.set_color(GREEN)
        arrow = TexMobject("\\longrightarrow")
        point = VectorizedPoint(in_vect.get_center())
        arrow.next_to(point, RIGHT)
        in_vect.next_to(arrow, LEFT)
        out_vect.next_to(arrow, RIGHT)
        # in_vect.to_edge(LEFT)
        # out_vect.to_edge(RIGHT)
        # out_vect.to_edge(RIGHT)
        # arrow.next_to(in_vect, RIGHT, buff = 1.5*scale_value)

        in_words = TextMobject("Input")
        in_words.next_to(in_vect, UP)
        in_words.set_color(BLUE_C)

        in_vect_top = TextMobject(self.pooling)
        in_vect_top.next_to(in_vect, DOWN)
        in_vect_top.set_color(RED)


        out_words = TextMobject("Output")
        out_words.next_to(out_vect, UP)
        out_words.set_color(GREEN_C)

        title = TextMobject(self.title)
        title.to_edge(UP)
        size = TextMobject("Kernel Size : " + str(self.kernel_size))
        size.to_edge(DOWN)
        stride = TextMobject("Stride : " + str(self.stride))
        stride.next_to(size, UP)

        self.add(title)
        self.add(size)
        self.add(stride)
        self.add(in_vect)
        self.add(in_words)
        self.add(in_vect_top)
        self.add(arrow)
        self.add(out_vect[2],out_vect[1])
        self.add(out_words)

        l = 0
        while(l<len(self.input_coords)-self.kernel_size + 1):
            m = 0
            while(m<len(self.input_coords)-self.kernel_size + 1):
                in_vect[0].set_color(BLUE)
                group = []
                for i in range(self.kernel_size):
                    for j in range(self.kernel_size):
                        in_vect[0][(i+l)*len(self.input_coords) + j+m].set_color(RED)
                        group.append(in_vect[0][(i+l)*len(self.input_coords) + j+m])

                value = str(self.output_coords[int(l/self.stride)][int(m/self.stride)])
                in_vect_num = TextMobject(value)
                in_vect_num.next_to(in_vect_top, DOWN)
                in_vect_num.set_color(RED)

                selection = VGroup(*list(group));
                frameBox = SurroundingRectangle(selection, buff = 2*SMALL_BUFF)
                frameBox.set_stroke(RED,1)
                self.add(frameBox)
                self.play(Write(in_vect_num))
                self.add(in_vect[0])
                self.play(Transform(in_vect_num, out_vect[0][int(l/self.stride*len(self.output_coords)) + int(m/self.stride)]))
                m = m + self.stride
                self.wait()
                self.remove(frameBox)
            l = l + self.stride

        self.remove(title)
        self.remove(size)
        self.remove(stride)
        self.remove(in_vect)
        self.remove(in_words)
        self.remove(in_vect_top)
        self.remove(arrow)
        self.remove(out_vect)

        self.remove(in_vect_num)
        self.remove(selection)
        
        self.remove(out_words)

    def construct(self):
        self.pool_init(2, 1, "max", [[2,6,1,10],[3,2,6,5],[5,7,8,6],[2,6,5,5]])
        self.animate()
        self.clear()
        self.wait()
        
        # self.pool_init(2, 2, "min", [[2,6,1,10],[3,2,6,5],[5,7,8,6],[2,6,5,5]])
        # self.animate()
        # self.clear()
        # self.wait()
        
        # self.pool_init(3, 1, "avg", [[2,6,1,10],[3,2,6,5],[5,7,8,6],[2,6,5,5]])
        # self.animate()
        # self.clear()
        # self.wait()