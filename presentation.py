from manim import *

class QBitScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self):
        self.lines = [NumberLine(
            x_range=[-2, 2, 1],
            length=4,
            include_tip=False,
            color=WHITE,
        ), NumberLine(
            x_range=[-2, 2, 1],
            length=4,
            include_tip=False,
            color=WHITE,
        )]
        self.arrows = [Arrow(
            start = ORIGIN,
            end = [1, 0, 0],
            color = YELLOW_E,
            buff = 0,
            max_stroke_width_to_length_ratio = 5
        )]
        self.axes = [Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": WHITE, "include_tip":False}
        )]
        self.shapes = [
            Circle(
                radius = 1,
                color = BLUE,
                fill_opacity = 0.5,
                stroke_color = WHITE
            )
        ]
        self.t=ValueTracker(0)
        self.x=ValueTracker(0)
        self.y=ValueTracker(1)
        self.qbit = always_redraw(lambda: MathTex(r"\begin{bmatrix}" + '%.2f' % np.cos(self.t.get_value()) + r"\\" + '%.2f' % np.sin(self.t.get_value()+0.001)+ r"\end{bmatrix}").to_corner(UL, buff=1))

    def add_updaters(self):
        self.arrows[0].add_updater(lambda z: z.become(Arrow(
            start = ORIGIN,
            end = [np.cos(self.t.get_value())*self.x.get_value(), np.sin(self.t.get_value())*self.y.get_value(), 0],
            color = YELLOW_E,
            buff = 0,
            max_stroke_width_to_length_ratio = 5
        )))

class QBits(QBitScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def construct(self):
        self.setup()
        self.add_updaters()
        bit = MathTex('0').move_to(self.qbit.get_center())
        self.play(Create(VGroup(self.lines[0], self.lines[1], self.arrows[0])))
        self.wait(1)
        self.play(self.x.animate.set_value(-1), Write(bit), run_time = 1)
        self.wait(1)
        self.play(self.x.animate.set_value(1), Transform(bit, MathTex('1').move_to(self.qbit.get_center())), run_time = 1)
        self.wait(1)
        self.play(Rotate(self.lines[0], angle=90*DEGREES), Unwrite(bit))
        self.add(self.axes[0])
        self.remove(self.lines[0], self.lines[1])
        self.play(Write(self.qbit))
        self.wait(1)
        self.play(self.t.animate(run_time=2).increment_value(360*DEGREES), DrawBorderThenFill(self.shapes[0], run_time=4))
        self.wait(1)

class UnitaryMatrices(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def setup(self):
        self.text = []
        self.steps = 6
        self.text.append(MathTex('c','','=','a','+', 'i', 'b'))
        self.text.append(MathTex('c','^*','=','a','-', 'i', 'b'))
        self.text.append(MathTex(r"A^{\dagger}=\begin{bmatrix}a_1+ib_1&a_2+ib_2\\a_3+ib_3&a_4+ib_4\\\end{bmatrix}^{\dagger}"))
        self.text.append(MathTex(r"A^{\dagger}=\begin{bmatrix}a_1+ib_1&a_2+ib_2\\a_3+ib_3&a_4+ib_4\\\end{bmatrix}^{*T}"))
        self.text.append(MathTex(r"A^{\dagger}=\begin{bmatrix}a_1-ib_1&a_2-ib_2\\a_3-ib_3&a_4-ib_4\\\end{bmatrix}^{T}"))
        self.text.append(MathTex(r"A^{\dagger}=\begin{bmatrix}a_1-ib_1&a_3-ib_3\\a_2-ib_2&a_4-ib_4\\\end{bmatrix}"))
        self.text.append(MathTex(r"A^\dagger A = I"))
        VGroup(self.text[0], self.text[1]).arrange(DOWN, buff=1)
    
    def step(self, step):
        if step == 0 :
            self.play(Write(self.text[0]), Write(Text("Unitary Matrices").to_edge(UP, buff=1)))
        elif step == 1:
            self.play(FadeTransformPieces(self.text[step-1].copy(), self.text[step]))
        elif step == 2:
            self.remove(self.text[0])
            self.play(FadeTransformPieces(self.text[step-1], self.text[step]))
        elif step >= 3 and step <= 5:
            self.play(TransformMatchingShapes(self.text[step-1], self.text[step]))
        elif step == 6:
            self.play(TransformMatchingShapes(self.text[step-1], self.text[step]))
        else:
            self.play(TransformMatchingTex(self.text[step-1], self.text[step]))
        self.wait(1)

class Unitary(UnitaryMatrices):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def construct(self):
        self.step(0)
        self.step(1)
        self.step(2)
        self.step(3)
        self.step(4)
        self.step(5)
        self.step(6)

class Algorithm(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def setup(self):
        self.text = []
        self.steps = 25
        self.text.append(MathTex(r"\left(I_{n-k+1}-\frac{2u_ku_k^\dagger}{u_k^\dagger u_k}\right)B^{(k)}"))
        self.text.append(MathTex(r"\left(I_{n-k+1}-\frac{2u_ku_k^\dagger}{u_k^\dagger u_k}\right)b=\beta_k e_1"))
        self.text.append(MathTex(r"u=b+e^{i\theta}||b||e_1"))
        self.text.append(MathTex(r"u=b+e^{i\theta}e_1"))
        self.text.append(MathTex(r"\frac{2}{u^\dagger u}"))
        self.text.append(MathTex(r"\frac{2}{||b||^2+||e_1||^2+2|b_1|"))
        self.text.append(MathTex(r"\frac{2}{2+2|b_1|"))
        self.text.append(MathTex(r"\frac{1}{1+|b_1|"))
        self.text.append(MathTex(r"\frac{2e^{-i\theta}}{u^\dagger u}"))
        self.text.append(MathTex(r"\frac{e^{-i\theta}}{1+|b_1|}"))
        self.text.append(MathTex(r"\frac{1}{e^{i\theta}+b_1}"))
        self.text.append(MathTex(r"Hb"))
        self.text.append(MathTex(r"-e^{i\theta}||b||e_1"))
        self.text.append(MathTex(r"-e^{i\theta}e_1"))
        self.text.append(MathTex(r"r=-e^{i\theta}e_1^T"))
        self.text.append(MathTex(r"HA"))
        self.text.append(MathTex(r"\left(I-\frac{2 u u^\dagger}{u^\dagger u}\right)A"))
        self.text.append(MathTex(r"A-\frac{2u}{u^\dagger u}\left(A^\dagger u\right)^\dagger"))
        self.text.append(MathTex(r"A-\frac{1}{1+|b_1|}\left(b+e^{i\theta}e_1\right)\left(A^\dagger(b+e^{i\theta e_1})\right)^\dagger"))
        self.text.append(MathTex(r"A-\frac{1}{1+|b_1|}(b+e^{i\theta}e_1)(e_1^T+e^{-i\theta}r)"))
        self.text.append(MathTex(r"A-\frac{1}{1+|b_1|}(be_1^Te^{i\theta}e_1e_1^T+e_1r+e^{-i\theta}br)"))
        self.text.append(MathTex(r"A-\frac{b\cdot r}{u_1}"))
        self.text.append(MathTex(r"(HA)_{2:n,2:n}=A_{2:n,2:n}-\frac{b(2:n)\cdot r(2:n)}{u_1}"))
        self.text.append(MathTex(r"A(i,j)_{nb+1}=A(i,j)_{nb}-\sum_{k-1}^{nb}A(i,k)\times A(k,j)"))
        self.text.append(Code(code_string="A(nb+1:n,nb+1:n)=A(nb+1:n,nb+1:n)-A(nb+1:n,1:nb)*A(1:nb,nb+1:n)"))
    
    def step(self, step):
        if step == 0 :
            self.play(Write(self.text[0]))
        elif step in {2,4,8,11,14,15,22,23}:
            self.play(Unwrite(self.text[step-1]))
            self.play(Write(self.text[step]))
        else:
            self.play(TransformMatchingShapes(self.text[step-1], self.text[step]))
        self.wait(1)

class AlgorithmWalkthrough(Algorithm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def construct(self):
        for i in range(0,self.steps):
            self.step(i)

    
