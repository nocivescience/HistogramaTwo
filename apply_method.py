from manim import *
class ApplyMethodScene(Scene):
    def construct(self):
        cirlce=Circle()
        self.play(
            ApplyMethod(cirlce.move_to, UP),
            ApplyMethod(cirlce.scale, 2),
        )
        self.wait()