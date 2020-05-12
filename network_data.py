#!/usr/bin/env python3

import matplotlib.pyplot as plt
import collections
import networkx as nx
import numpy as np
import plfit

def degree_distribution_plot(G):
    """
    Makes a plot for the degree distribution of the inputted graph where the y axis corresponds to the fraction of nodes
    in the graph and the x axis corresponds to the degree of a node. The y axis uses a logarithmic scale.

    Parameters
    ----------
    G : Graph
        A graph corresponding to a human social network.

    Notes
    -----
    Values on axes are predetermined and may not be optimal for a given graph.
    """

    # Adapted from https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_degree_histogram.html
    degrees = [G.degree(n) for n in G.nodes]
    degreeCount = collections.Counter(degrees)
    deg, cnt = zip(*degreeCount.items())
    cnt_frac = []
    for i in range(len(cnt)):
        cnt_frac.append(cnt[i] / G.number_of_nodes())

    plt.scatter(deg, cnt_frac, s=10)

    plt.title("Degree Distribution")
    plt.ylabel("Fraction")
    plt.yscale("log")
    y_ticks = [1, 0.1, 0.01, 0.001, 0.0001]
    plt.yticks(y_ticks, y_ticks)
    plt.xlabel("Degree")
    plt.xscale("log")
    x_ticks = [3, 30, 300]
    plt.xticks(x_ticks, x_ticks)

    plt.show(block=False)

def statistics(G):
    """
    Prints the characteristic path length (geodesic) of the inputted network, the clustering coefficient of the inputted
    network, and Kolmogorov-Smirnov test results for the similarity of the degree distribution with a power law
    distribution of the inputted network.

    Parameters
    ----------
    G : Graph
        A graph corresponding to a human social network.

    Notes
    -----
    KS test from plfit.py package implementing algorithm for mapping data to a power-law distribution from Clauset et
    al. (2009).
    """

    curr_geodesic = nx.average_shortest_path_length(G)
    curr_clustering = nx.average_clustering(G)

    degrees = [G.degree(n) for n in G.nodes]
    est = plfit.plfit(x=degrees, discrete=True, nosmall=False)
    a = est._alpha
    p, k = est.test_pl()

    print("Geodesic: " + str(curr_geodesic) + "; Clustering: " + str(curr_clustering) +
          "; Degree Distribution: alpha = " + str(a) + ", KS = " + str(np.mean(k)) + ", p = " + str(p))

    return (curr_geodesic, curr_clustering, a, k, p)
