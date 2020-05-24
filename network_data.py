#!/usr/bin/env python3

import matplotlib.pyplot as plt
import collections
import networkx as nx
import scipy.stats as stats

def degree_distribution_plot(G):
    """
    Makes a plot for the degree distribution of the inputted graph where the y axis corresponds to the fraction of nodes
    in the graph and the x axis corresponds to the degree of a node. Both axes uses a logarithmic scale.

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

def graph_statistics(G):
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
    KS test currently not working properly.
    """

    curr_geodesic = nx.average_shortest_path_length(G)
    curr_clustering = nx.average_clustering(G)

    degrees = [G.degree(n) for n in G.nodes]

    # Does not seem to properly fit to powerlaw
    a, l, s = stats.powerlaw.fit(degrees)

    ks, p = stats.kstest(degrees, "powerlaw", args=(a, l, s))


    print("Geodesic: " + str(curr_geodesic) + "; Clustering: " + str(curr_clustering) +
          "; Degree Distribution: alpha = " + str(a) + ", KS = " + str(ks) + ", p = " + str(p))

    return (curr_geodesic, curr_clustering, a, ks, p)
