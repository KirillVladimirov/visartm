# -*- coding: utf-8 -*-
import numpy as np
import json
from algo.arranging.hamilton_path import HamiltonPath
from algo.arranging.quality import NDS
from algo.arranging.dendro_arranger import DendroArranger


from algo.arranging.metrics import metrics_list

try:
    params = json.loads(research.problem.params)
except BaseException:
    pass

model = research.model
topics = model.get_topics()


research.report_html("<h1>Annealing test.</h1>")
research.report("Берётся тематическая модель, для матрицы фи разными "
                " метриками вычисляется матрица расстояний.")
research.report("Потом для этой матрицы оптимизируется функционал "
                "суммы расстояний между соседями.")
research.report("Используется алгоритм дендрограммы (как baseline) и "
                "алгоритм симмуляции отжига с перебором "
                "числа шагов по логаримической сетке.")

for metric in metrics_list:
    research.report("Метрика %s" % metric)
    dist = model.get_topics_distances(metric=metric)
    da = DendroArranger(dist)
    dendro_perm = da.arrange()
    dendro_quality = NDS(dist, dendro_perm)
    research.report("Dendro %f" % dendro_quality)

    hp = HamiltonPath(dist, caller=research)
    hp.solve_lkh()
    lkh_quality = NDS(dist, hp.path)
    research.report("LKH %f" % lkh_quality)

    hp = HamiltonPath(dist, caller=research)
    steps_range = np.linspace(3, 8, 30)
    quality_chart = []
    for steps in steps_range:
        hp.solve_annealing(steps=int(10**steps))
        quality_chart.append(NDS(dist, hp.path))
        research.report("Annealing %d %f" %
                        (int(10**steps), quality_chart[-1]))

    axes = research.gca(figsize=(20, 10))
    axes.set_xlabel("Iterations(log10)", fontsize=20)
    axes.set_ylabel("Quality", fontsize=20)
    axes.plot(steps_range, quality_chart, label="Annealing")
    axes.plot([steps_range[0], steps_range[-1]],
              [dendro_quality, dendro_quality], label="Dendrogram")
    axes.plot([steps_range[0], steps_range[-1]],
              [lkh_quality, lkh_quality], label="LKH")
    lgd = axes.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    research.report_picture(bbox_extra_artists=(lgd,), width=800)
