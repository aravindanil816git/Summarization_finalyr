
import networkx as nx
from networkx.exception import NetworkXError
from networkx.utils import not_implemented_for
import networkx as nx
import numpy as np
 
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

def pagerank(G, alpha=0.85, personalization=None,
             max_iter=100, tol=1.0e-6, nstart=None, weight='weight',
             dangling=None):
   
    if len(G) == 0:
        return {}

    if not G.is_directed():
        D = G.to_directed()
    else:
        D = G
    W = nx.stochastic_graph(D, weight='weight')
    N = W.number_of_nodes()
    x = dict.fromkeys(W, 1.0 / N)
    p=dict.fromkeys(W, 1.0 / N)
    dangling_weights = p
   
    dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]

    for _ in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
        for n in x:
            # this matrix multiply looks odd because it is
            # doing a left multiply x^T=xlast^T*W
            for nbr in W[n]:
                x[nbr] += alpha * xlast[n] * W[n][nbr][weight]
            x[n] += danglesum * dangling_weights[n] + (1.0 - alpha) * p[n]
        # check convergence, l1 norm
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < N*tol:
            return x
    raise NetworkXError('pagerank: power iteration failed to converge '
                        'in %d iterations.' % max_iter)




document = """To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name. In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler
"""

sentence_tokenizer = PunktSentenceTokenizer()
sentences = sentence_tokenizer.tokenize(document)


bow_matrix = CountVectorizer().fit_transform(sentences)
normalized = TfidfTransformer().fit_transform(bow_matrix)
similarity_graph = normalized * normalized.T
nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
scores = pagerank(nx_graph)


print sorted(((scores[i],s) for i,s in enumerate(sentences)),reverse=True)








