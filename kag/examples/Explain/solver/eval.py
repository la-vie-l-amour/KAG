import logging
from kag.common.conf import KAG_CONFIG
from kag.common.registry import import_modules_from_path

from kag.solver.logic.solver_pipeline import SolverPipeline

logger = logging.getLogger(__name__)


class ExplainDemo:

    """
    init for kag client
    """

    def qa(self, query):
        resp = SolverPipeline.from_config(KAG_CONFIG.all_config["kag_solver_pipeline"])
        answer, trace_log = resp.run(query)

        return answer, trace_log

    """
        parallel qa from knowledge base
        and getBenchmarks(em, f1, answer_similarity)
    """


if __name__ == "__main__":
    import_modules_from_path("./prompt")

    demo = ExplainDemo()
    query = "内分泌科属于哪个科室？"
    answer, trace_log = demo.qa(query)
    print(f"Question: {query}")
    print(f"Answer: {answer}")
    print(f"TraceLog: {trace_log}")
    import json 
    with open('trace.json', 'w', encoding='utf-8') as f:
        json.dump(trace_log, f, ensure_ascii=False, indent=4)
