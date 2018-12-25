import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import (
    KMeans, AffinityPropagation, MeanShift, SpectralClustering, AgglomerativeClustering, DBSCAN
)

CLUSTER_TYPES = (
    KMeans,
    AffinityPropagation,
    MeanShift,
    SpectralClustering,
    AgglomerativeClustering,
    DBSCAN
)


def _n_clusters(X, mdl):
    if not type(mdl) in (AffinityPropagation, MeanShift, DBSCAN):
        n_clusters = X.mdl_cluster.get_params()['n_clusters']

    elif type(mdl) == AffinityPropagation:
        n_clusters = X.mdl_cluster.cluster_centers_indices_.shape[0]

    elif type(mdl) == MeanShift:
        n_clusters = X.mdl_cluster.cluster_centers_.shape[0]

    elif type(mdl) == DBSCAN:
        n_clusters = X.mdl_cluster.core_sample_indices_.shape[0]

    return n_clusters


def _data_cluster(X, mdl, decomposed=False, pca_comps=4):
    if type(mdl) not in CLUSTER_TYPES:
        raise TypeError('Must pass a sklearn cluster class. Refer to documentation.')

    X.mdl_cluster = mdl

    if decomposed:
        print('Clustering with the first ' + str(pca_comps) + ' PCA components.')
        mdl_pca = PCA(n_components=pca_comps)
        comps = mdl_pca.fit_transform(X.flatten())
        X.mdl_cluster.fit(comps)
        n_clusters = _n_clusters(X, mdl)
        if type(X.mdl_cluster) in (AffinityPropagation, MeanShift):
            n_clusters = X.mdl_cluster.cluster_centers_.shape[0]
        labels = X.mdl_cluster.labels_.reshape(X.data.shape[:-1])

    else:
        X.mdl_cluster.fit(X.flatten())
        n_clusters = _n_clusters(X, mdl)
        labels = X.mdl_cluster.labels_.reshape(X.data.shape[:-1])

    try:
        if decomposed:
            specs = mdl_pca.inverse_transform(X.mdl_cluster.cluster_centers_)
        else:
            specs = X.mdl_cluster.cluster_centers_

    except AttributeError:
        specs = np.zeros((n_clusters, X.data.shape[-1]))
        lbls = labels + 1
        for cluster_number in range(n_clusters):
            msk = np.zeros(X.data.shape)
            for spectral_point in range(X.data.shape[-1]):
                msk[..., spectral_point] = np.multiply(
                    X.data[..., spectral_point],
                    np.where(lbls == cluster_number+1, lbls, 0)/(cluster_number+1)
                )
                    
            if X.ndim == 3:
                specs[cluster_number, :] = np.squeeze(np.mean(np.mean(msk, 1), 0))
            elif X.ndim == 4:
                specs[cluster_number, :] = np.squeeze(np.mean(np.mean(np.mean(msk, 2), 1), 0))

    return labels, specs
