from manim import *
class HistogramScene(Scene):
    CONFIG={
        'axis_config': {
            'x_min': 0,
            'x_max': 8,
            'y_min': 0,
            'y_max': 10,
            'y_axis_config': {
                'tips': False,
            },
        },
        'rect_config': {
            'fill_opacity': 0.7,
            'fill_color': RED,
            'stroke_color': BLACK,
            'stroke_width': 1,
        },
    }
    def construct(self):
        axes=self.get_axes()
        bars=self.get_histogram(axes)
        n_scores=10000
        scores=np.array([self.get_random_score() for _ in range(n_scores)])
        index_tracker=ValueTracker(n_scores)
        def get_index():
            value=np.clip(index_tracker.get_value(),0,n_scores-1)
            return int(value)
        bars.add_updater(lambda b: self.set_histogram_bars(bars, scores[:get_index()], axes))
        anims=[axes,bars]
        self.play(Write(axes),Create(bars))
        for value in [10, 100, 1000, 10000]:
            anims={
                ApplyMethod(
                    index_tracker.set_value, value,
                    rate_func=linear,
                    run_time=5
                )
            }
            self.play(*anims)
        self.wait()
    def get_axes(self):
        axes=Axes(
            x_range=(self.CONFIG['axis_config']['x_min'], self.CONFIG['axis_config']['x_max'], 1),
            y_range=(self.CONFIG['axis_config']['y_min'], self.CONFIG['axis_config']['y_max'], 1),
            **self.CONFIG['axis_config']['y_axis_config']
        )
        axes.x_axis.set_opacity(0)
        axes.to_edge(LEFT, buff=0.5)
        return axes
    def get_histogram(self,axes):
        bars=VGroup()
        for y in range(1,self.CONFIG['axis_config']['y_max'],1):
            bar=Rectangle(
                **self.CONFIG['rect_config'],
                height=axes.y_axis.unit_size,
            )
            bar.y=y
            bar.move_to(axes.c2p(0,y), LEFT)
            bars.add(bar)
        return bars
    def get_relative(self, all_scores):
        scores=set(all_scores)
        n_scores=len(all_scores)
        return dict([
            (s, np.sum(all_scores==s)/n_scores) for s in scores
        ])
    def set_histogram_bars(self,bars,score,axes):
        prop_maps=self.get_relative(score)
        epsilon=0.001
        for bar in bars:
            prop=prop_maps.get(bar.y,epsilon)
            bar.stretch_to_fit_width(
                prop*axes.x_axis.unit_size*10,
                about_edge=LEFT,
            )
    def get_random_score(self):
        score=1
        radius=1
        while True:
            point=np.random.uniform(-radius,radius,2)
            hit_radius=np.linalg.norm(point)
            if hit_radius>radius:
                return score
            else:
                score+=1
                radius=np.sqrt(radius**2-hit_radius**2)