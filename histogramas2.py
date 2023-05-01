from manim import *


class MiHistogram2(Scene):
    CONFIG = {
        "axis_config": {
            "x_min": 0,
            "x_max": 8,
            "y_min": 0,
            "y_max": 60,
        },
        "rect_config": {
            "fill_opacity": 0.7,
            "fill_color": ORANGE,
            "stroke_color": BLACK,
            "stroke_width": 1
        }
    }
    def construct(self):
        axes = self.get_axes()
        n_scores = 10000
        scores = np.array([np.random.randint(1,8)*2 for _ in range(n_scores)])
        index_tracker = ValueTracker(n_scores)
        def get_index():
            value = np.clip(index_tracker.get_value(), 0, n_scores-1)
            return int(value)
        bars = self.get_histogram(axes)
        anims = [axes, bars]
        bars.add_updater(lambda b: self.set_histogram_bars(
            bars, scores[:get_index()], axes))
        self.add(bars)
        score_label = VGroup(Tex("This is mind: "), Integer(1))
        score_label.arrange(RIGHT, buff=0.1)
        score_label[1].add_updater(
            lambda m: m.set_value(scores[get_index()-1]))
        score_label[1].add_updater(lambda m: m.set_fill(
            bars[scores[get_index()-1]].get_fill_color()))
        n_trials_label = VGroup(Tex("Reconteo: "), Integer(0))
        n_trials_label.arrange(RIGHT)
        explaining_text = VGroup(score_label, n_trials_label).arrange(DOWN, buff=0.1)
        explaining_text[1].align_to(explaining_text[0], LEFT)
        explaining_text.to_corner(UP+RIGHT)
        self.play(Write(explaining_text))
        self.play(*[FadeIn(anim) for anim in anims])
        self.add(score_label, n_trials_label)
        for value in [10, 100, 1000, 10000]:
            anims = {
                ApplyMethod(
                    index_tracker.set_value, value,
                    rate_func=linear,
                    run_time=15
                )
            }
            self.play(*anims)
        self.wait()

    def get_axes(self):
        axes = Axes(
            x_range=(self.CONFIG['axis_config']['x_min'], self.CONFIG['axis_config']['x_max'], 1),
            y_range=(self.CONFIG['axis_config']['y_min'], self.CONFIG['axis_config']['y_max'], 100),
        )
        axes.to_edge(DOWN, buff=0.6)
        axes.to_edge(LEFT, buff=0.6)
        return axes

    def get_histogram(self, axes):
        bars = VGroup()
        for x in range(0, 8, 1):
            bar = Rectangle(**self.CONFIG['rect_config'], width=axes.x_axis.unit_size)
            bar.move_to(axes.c2p(x, 0), DOWN)
            bar.x = x
            bars.add(bar)
        return bars

    def get_relative_proportion_map(self, all_scores):
        scores = set(all_scores)
        n_scores = len(all_scores)
        return dict([(s, np.sum(all_scores == s)/n_scores) for s in set(scores)])

    def set_histogram_bars(self, bars, scores, axes):
        prop_map = self.get_relative_proportion_map(scores)
        epsilon = 1e-6
        for bar in bars:
            prop = prop_map.get(bar.x, epsilon)
            bar.stretch_to_fit_height(prop*axes.y_axis.unit_size*100, about_edge=DOWN)

    def get_random_score(self):
        score = 1
        radius = 1
        while True:
            point = np.random.uniform(-1, 1, size=2)
            hit_radius = np.linalg.norm(point)
            if hit_radius > radius:
                return score
            else:
                score += 1
                radius = np.sqrt(radius**2-hit_radius**2)
