from manim import *
class HistogramScene(Scene):
    CONFIG={
        'n_bars': 6,
    }
    def construct(self):
        n_score=1000
        score=np.array([self.get_random_score() for i in range(n_score)])
        index_tracker=ValueTracker(n_score)
        def get_index():
            value=np.clip(index_tracker.get_value(),0,n_score-1)
            return int(value)
        bars=self.get_bars()
        bars.add_updater(
            lambda b: self.set_histogram_bars(b,score[:get_index()]),
        )
        self.add(bars)
        index_tracker.set_value(1)
        for value in [10,100,1000]:
            anims=[ApplyMethod(index_tracker.set_value,value)]
            self.play(*anims,run_time=2)
        self.wait()
    def get_bars(self):
        bars=VGroup()
        for i in range(self.CONFIG['n_bars']):
            bar=Rectangle(
                height=1,
                width=np.random.random(),
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=1,
            )
            bars.add(bar)
        bars.arrange(DOWN,buff=0.1, aligned_edge=LEFT).to_edge(LEFT,buff=1)
        return bars
    def get_random_score(self):
        return np.random.randint(0,10)
    def get_relatives_proporticion(self,all_score):
        return all_score/sum(all_score)
    def set_histogram_bars(self,bars,scores):
        props_maps=self.get_relatives_proporticion(scores)
        for bar in bars:
            bar.stretch_to_fit_width(props_maps[i],)
            