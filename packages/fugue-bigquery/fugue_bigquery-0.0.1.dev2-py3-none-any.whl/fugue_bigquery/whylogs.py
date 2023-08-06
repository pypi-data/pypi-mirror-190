from typing import Tuple

from fugue import DataFrames, Outputter
from fugue.plugins import parse_outputter
from IPython.display import display
from whylogs.api.fugue import fugue_profile
from whylogs.viz import NotebookProfileVisualizer


class WhyViz(Outputter):
    def __init__(self, func: str) -> None:
        super().__init__()
        self._func = func

    def process(self, dfs: DataFrames) -> None:
        visualization = NotebookProfileVisualizer()
        if self._func == "profile":
            p = fugue_profile(dfs[0])
            visualization.set_profiles(target_profile_view=p)
            display(visualization.profile_summary())
        elif self._func == "drift":
            p1 = fugue_profile(dfs[0])
            p2 = fugue_profile(dfs[1])
            visualization.set_profiles(
                target_profile_view=p1, reference_profile_view=p2
            )
            display(visualization.summary_drift_report())


@parse_outputter.candidate(
    lambda x: isinstance(x, tuple) and isinstance(x[0], str) and x[0] == "why"
)
def _parse_why(obj: Tuple[str, str]) -> Outputter:
    return WhyViz(obj[1])
