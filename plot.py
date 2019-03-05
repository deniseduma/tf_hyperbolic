#!/usr/bin/env python3

import matplotlib.pyplot as plt
import re
from collections import namedtuple
import tensorflow as tf

tf.enable_eager_execution()

from embed import MANIFOLDS
from hype.sn import initialize
from hype.tf_graph import load_edge_list

plt.style.use("ggplot")

# TODO - tSNE to collapse higher dims


def poincare_plot(names, embeddings, name, take=100):
    fig = plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.cla()
    ax.set_xlim((-1.1, 1.1))
    ax.set_ylim((-1.1, 1.1))
    ax.add_artist(plt.Circle((0, 0), 1.0, color="black", fill=False))
    for i, w in enumerate(names[:take]):
        c0, c1, *rest = embeddings[i]
        x = c0
        y = c1
        ax.plot(x, y, "o", color="r")
        ax.text(x - 0.1, y + 0.04, re.sub("\.n\.\d{2}", "", w), color="b")
    fig.savefig("plots/" + name + ".png", dpi=fig.dpi)
    plt.show()


Opts = namedtuple("Opts", "manifold dim negs batchsize burnin dampening")

if __name__ == "__main__":
    opt = Opts("poincare", 5, 50, 10, 20, 0.75)
    manifold = MANIFOLDS[opt.manifold](debug=False, max_norm=500_000)
    idx, objects, weights = load_edge_list("wordnet/mammal_closure.csv", False)
    model, data, model_name, conf = initialize(
        manifold, opt, idx, objects, weights, sparse=False
    )
    ck_name = "mammals-5d.tf"
    model.load_weights(f"checkpoints/{ck_name}")
    poincare_plot(objects, model.emb.numpy(), ck_name)
