from manim import *
from manim_slides import Slide
class QBitScene(Slide):
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
        self.qbit = always_redraw(lambda: MathTex(r"\begin{bmatrix}" + '%.2f' % np.cos(self.t.get_value()) + r"\\" + '%.2f' % np.sin(self.t.get_value()+0.001)+ r"\end{bmatrix}").to_corner(UL, buff=2))
        self.title = Title("QBit Representation")

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
        self.play(Create(VGroup(self.lines[0], self.lines[1], self.arrows[0])), Write(self.title))
        self.next_slide()
        self.play(self.x.animate.set_value(-1), Write(bit), run_time = 1)
        self.next_slide()
        self.play(self.x.animate.set_value(1), Transform(bit, MathTex('1').move_to(self.qbit.get_center())), run_time = 1)
        self.next_slide()
        self.play(Rotate(self.lines[0], angle=90*DEGREES), Unwrite(bit))
        self.add(self.axes[0])
        self.remove(self.lines[0], self.lines[1])
        self.play(Write(self.qbit))
        self.next_slide()
        self.play(self.t.animate(run_time=2).increment_value(360*DEGREES), DrawBorderThenFill(self.shapes[0], run_time=4))
        self.next_slide()

class UnitaryMatrices(Slide):
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
        self.title = Title("Unitary Matrices")
    
    def step(self, step):
        if step == 0 :
            self.play(Write(self.text[0]), Write(self.title))
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
        self.next_slide()

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

class Algorithm(Slide):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def setup(self):
        self.title = Title("Householder QR Algorithm")
        self.text = []
        self.steps = 18
        self.text.append(MathTex(r"b = A[k:n,k]~,~r=A[k,k:n]"))
        self.text.append(MathTex(r"u = ||b||e_1-b"))
        self.text.append(MathTex(r"u=b+e^{i\theta}||b||e_1"))
        self.text.append(MathTex(r"u=b+e^{i\theta}e_1"))
        self.text.append(MathTex(r"u=b+\frac{b_1}{|b_1|}e_1"))
        self.text.append(MathTex(r"\tau=\frac{2}{u^\dagger u}"))
        self.text.append(MathTex(r"\tau=\frac{2}{||b||^2+||e_1||^2+2|b_1|"))
        self.text.append(MathTex(r"\tau=\frac{2}{2+2|b_1|"))
        self.text.append(MathTex(r"\tau=\frac{1}{1+|b_1|"))
        self.text.append(MathTex(r"HA=\left(I-\tau u u^\dagger\right)A"))
        self.text.append(MathTex(r"HA=A-\tau\left(A^\dagger u\right)^\dagger"))
        self.text.append(MathTex(r"HA=A-\tau\left(b+e^{i\theta}e_1\right)\left(A^\dagger(b+e^{i\theta e_1})\right)^\dagger"))
        self.text.append(MathTex(r"HA=A-\tau(b+e^{i\theta}e_1)(e_1^T+e^{-i\theta}r)"))
        self.text.append(MathTex(r"HA=A-\tau(be_1^Te^{i\theta}e_1e_1^T+e_1r+e^{-i\theta}br)"))
        self.text.append(MathTex(r"HA=A-\frac{b\cdot r}{u_1}"))
        self.text.append(VGroup(MathTex(r"u=\frac{1}{e^{i\theta}(1+|b_1|)}\left(b+\frac{b_1}{|b_1|}e_1\right)"), MathTex(r"\tau=1+|b_1|")).arrange(DOWN, buff=1))
        self.text.append(MathTex(r"HA=A-u\cdot r"))
        self.text.append(Code(code_string="phase = A[nb,nb]/abs(A[nb,nb])\n Tau[nb] = (1+abs(A[nb, nb]))\nA[nb, nb] += phase \n A[nb:n, nb] = A[nb:n, nb]/(phase*Tau[nb])\n A[nb,nb] = -phase\n A[nb+1:n,nb+1:n]= A[nb+1:n, nb+1:n]-A[nb+1:n,nb].*A[nb:nb, nb+1:n]"))
        self.mat = []
        self.mat.append(VGroup(Rectangle(width=6, height=6, color=WHITE), Rectangle(width=1, height=6, color=WHITE).shift(LEFT*2.5), Rectangle(width=6, height=1, color=WHITE).shift(UP*2.5)))
        self.mat.append(VGroup(MathTex("b").shift(LEFT*2.5), MathTex("r").shift(UP*2.5), MathTex("A").scale(3).shift(DR*0.5)))
        self.mat.append(VGroup(MathTex("b").shift(LEFT*2.5), MathTex("r").shift(UP*2.5), MathTex("A").scale(3).shift(DR*0.5)))
        self.mat.append(VGroup(MathTex(r"e^{i\theta}=\frac{b_1}{|b_1|}").shift(UL*2.5), MathTex(r"u=\frac{b}{e^{i\theta}{\tau}}").shift(LEFT*2.5), MathTex(r"\tau=1+|b_1|").shift(UP*3), MathTex(r"HA=A-u\cdot r").shift(DR*0.5)).shift(4*RIGHT))
        self.mat.append(VGroup(Rectangle(width=6, height=6, color=WHITE), Rectangle(width=1, height=6, color=WHITE).shift(LEFT*2.5), Rectangle(width=6, height=1, color=WHITE).shift(UP*2.5)))
        self.mat.append(VGroup(MathTex(r"u").shift(LEFT*2.5), MathTex("r").shift(UP*2.5), MathTex("HA").scale(3).shift(DR*0.5), MathTex(r"-e^{i\theta}").shift(UL*2.5)))

    
    def step(self, step):
        if step == 0 :
            self.play(Write(self.text[0]))
        elif step in {1,2,4,9,15,16,17}:
            self.play(Unwrite(self.text[step-1]))
            self.play(Write(self.text[step]))
        else:
            self.play(TransformMatchingShapes(self.text[step-1], self.text[step]))
        self.next_slide()

class AlgorithmWalkthrough(Algorithm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def construct(self):
        for i in range(1,self.steps):
            self.step(i)
        self.remove(self.text[-1])
        self.play(Create(self.mat[0]), Create(self.mat[1]))
        self.next_slide()
        self.play(MoveAlongPath(self.mat[0], Line(ORIGIN, LEFT*4)), MoveAlongPath(self.mat[1], Line(ORIGIN, LEFT*4)), TransformFromCopy(self.mat[1], self.mat[3]))
        self.next_slide()
        self.play(MoveAlongPath(self.mat[0], Line(LEFT*4,ORIGIN)), Transform(self.mat[3], self.mat[5]), FadeOut(self.mat[1]))
        # self.play(TransformMatchingShapes(VGroup(self.mat[0], self.mat[1]).arrange(RIGHT, buff=1), self.mat[2]))

class QuantumCircuits(Slide):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def setup(self):
        self.Title = Title("Quantum Circuits")
        self.gates = {}
        self.gates["H"] = (VGroup(MathTex("H"), SurroundingRectangle(MathTex("H"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.gates["X"] = (VGroup(MathTex("X"), SurroundingRectangle(MathTex("X"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.gates["Y"] = (VGroup(MathTex("X"), SurroundingRectangle(MathTex("X"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.gates["Z"] = (VGroup(MathTex("Z"), SurroundingRectangle(MathTex("Z"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.gates["S"] = (VGroup(MathTex("S"), SurroundingRectangle(MathTex("S"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.gates["T"] = (VGroup(MathTex("X"), SurroundingRectangle(MathTex("X"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.gates["?"] = (VGroup(MathTex("?"), SurroundingRectangle(MathTex("?"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.gates["Ph"] = (VGroup(MathTex(r"Ph(\theta)"), SurroundingRectangle(MathTex(r"Ph(\theta)"), color=WHITE, buff=MED_SMALL_BUFF))).add_background_rectangle(color=BLACK,opacity=1)
        self.matgates = {}
        self.matgates["H"] = MathTex(r"\frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\1 & -1\end{bmatrix}")
        self.matgates["X"] = MathTex(r"\begin{bmatrix}0 & 1\\1 & 0\end{bmatrix}")
        self.matgates["Y"] = MathTex(r"\begin{bmatrix}0 & -i\\i & 0\end{bmatrix}")
        self.matgates["Z"] = MathTex(r"\begin{bmatrix}1 & 0\\0 & -1\end{bmatrix}")
        self.matgates["S"] = MathTex(r"\begin{bmatrix}1 & 0\\0 & i\end{bmatrix}")
        self.matgates["T"] = MathTex(r"\begin{bmatrix}1 & 0\\0 & e^{i\pi/4}\end{bmatrix}")
        self.matgates["Ph"] = MathTex(r"\begin{bmatrix}1 & 0\\0 & e^{i\theta}\end{bmatrix}")
    
    def construct(self):
        gates1 = VGroup(MathTex(r"\left|{\Psi}\right\rangle").add_background_rectangle(color=BLACK,opacity=1),self.gates["H"], self.gates["X"], self.gates["Y"], self.gates["Z"], self.gates["S"], self.gates["T"], self.gates["Ph"]).arrange(buff=0.5).shift(UP)
        matgates1 = VGroup(MathTex(r"\left|{\Psi}\right\rangle"),self.matgates["H"], self.matgates["X"], self.matgates["Y"], self.matgates["Z"], self.matgates["S"], self.matgates["T"], self.matgates["Ph"]).arrange(buff=0.2).shift(DOWN)
        totalgates = MathTex(r"\left|{\Psi}\right\rangle\frac{1}{\sqrt{2}}\begin{bmatrix}i&-e^{i\theta+i\pi/4}\\i&e^{i\theta+i\pi/4}\end{bmatrix}").shift(DOWN)
        lines = VGroup(VGroup(Line(ORIGIN, RIGHT*11), MathTex(r"\left|{\Psi_1}\right\rangle").add_background_rectangle(color=BLACK,opacity=1)),VGroup(Line(ORIGIN, RIGHT*11), MathTex(r"\left|{\Psi_2}\right\rangle").add_background_rectangle(color=BLACK,opacity=1)),VGroup(Line(ORIGIN, RIGHT*11), MathTex(r"\left|{\Psi_3}\right\rangle").add_background_rectangle(color=BLACK,opacity=1)),VGroup(Line(ORIGIN, RIGHT*11), MathTex(r"\left|{\Psi_4}\right\rangle").add_background_rectangle(color=BLACK,opacity=1))).arrange(DOWN, buff=0.3)
        self.play(Write(self.Title), Create(Line(LEFT*5, RIGHT*6).shift(UP)), Create(gates1[0]))
        self.next_slide()
        self.play(Create(gates1[1:]))
        self.next_slide()
        self.play(TransformFromCopy(gates1, matgates1))
        self.next_slide()
        self.play(FadeTransform(matgates1, totalgates))
        self.next_slide()
        self.clear()
        self.add(self.Title)
        self.play(Create(lines))
        self.next_slide()
        unknown = VGroup([self.gates["?"].copy().match_height(lines[0]) for i in range(40)]).arrange_in_grid(rows=4, buff=0.3)
        unitary = VGroup(Rectangle(width=0.3, height=0.5, color=WHITE, fill_color = BLACK, fill_opacity = 1).match_height(unknown), MathTex("U").match_height(self.gates["H"]) )
        self.play(Write(unitary))
        self.next_slide()
        self.play(Transform(unitary, unknown))

class TheProblem(Slide):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def setup(self):
        self.title = Title("The Problem")
        self.steps = []
        self.steps.append(VGroup(MathTex(r"U\to G_1G_2...G_k"), Tex(r"Where $G_i$ are available quantum gates.")).arrange(DOWN, buff=0.5))
        self.steps.append(VGroup(MathTex(r"H_1H_2...H_nD\to G_1G_2...G_k"), Tex(r"Where $H_i = I-\frac{2uu^\dagger}{u\dagger u}$ and $D$ is diagonal")).arrange(DOWN, buff=0.5))
        self.steps.append(VGroup(MathTex(r"U\to H_1H_2...H_nD"), Tex(r"This is householder QR!")).arrange(DOWN, buff=0.5))
    
    def construct(self):
        self.play(Write(self.title), Write(self.steps[0]))
        self.next_slide()
        self.play(TransformMatchingShapes(self.steps[0][0], self.steps[1][0]), FadeTransform(self.steps[0][1], self.steps[1][1]))
        self.next_slide()
        self.play(TransformMatchingShapes(self.steps[1][0], self.steps[2][0]), FadeTransform(self.steps[1][1], self.steps[2][1]))
        self.next_slide()

    
