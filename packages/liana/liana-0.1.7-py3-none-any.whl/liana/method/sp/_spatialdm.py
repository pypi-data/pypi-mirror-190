import numpy as np
from scipy.sparse import csr_matrix
from scipy.stats import norm

from anndata import AnnData
from pandas import DataFrame
from typing import Optional

from tqdm import tqdm

from liana.method.sp._SpatialMethod import SpatialMethod
from liana.method._global_lr_pipe import _global_lr_pipe
from liana.method.sp._spatial_utils import _local_to_dataframe, _local_permutation_pvals


class SpatialDM(SpatialMethod):
    def __init__(self, _method, _complex_cols, _obsm_keys):
        super().__init__(method_name=_method.method_name,
                         key_cols=_method.key_cols,
                         reference=_method.reference,
                         )

        self.complex_cols = _complex_cols
        self.obsm_keys = _obsm_keys
        self._method = _method

    def __call__(self,
                 adata: AnnData,
                 resource_name: str = 'consensus',
                 expr_prop: float = 0.05,
                 pvalue_method: str = 'analytical',
                 n_perm: int = 1000,
                 positive_only: bool = True,
                 use_raw: Optional[bool] = True,
                 layer: Optional[str] = None,
                 verbose: Optional[bool] = False,
                 seed: int = 1337,
                 resource: Optional[DataFrame] = None,
                 inplace=True
                 ):
        """
        Parameters
        ----------
        adata
            Annotated data object.
        resource_name
            Name of the resource to be loaded and use for ligand-receptor inference.
        expr_prop
            Minimum expression proportion for the ligands/receptors (and their subunits).
             Set to `0` to return unfiltered results.
        pvalue_method
            Method to obtain P-values: One out of ['permutation', 'analytical'];
            'analytical' by default.
        n_perm
            Number of permutations to be performed if `pvalue_method`=='permutation'
        positive_only
            Whether to calculate p-values only for positive correlations. `True` by default.
        use_raw
            Use raw attribute of adata if present.
        layer
            Layer in anndata.AnnData.layers to use. If None, use anndata.AnnData.X.
        verbose
            Verbosity flag
        seed
            Random seed for reproducibility.
        resource
            Parameter to enable external resources to be passed. Expects a pandas dataframe
            with [`ligand`, `receptor`] columns. None by default. If provided will overrule
            the resource requested via `resource_name`
        inplace
            If true return `DataFrame` with results, else assign to `.uns`.

        Returns
        -------
        If ``inplace = False``, returns:
        - 1) a `DataFrame` with ligand-receptor correlations for the whole slide (global)
        - 2) a `DataFrame` with ligand-receptor Moran's I for each spot
        - 3) a `DataFrame` with ligand-receptor correlations p-values for each spot
        Otherwise, modifies the ``adata`` object with the following keys:
        - :attr:`anndata.AnnData.uns` ``['global_res']`` with `1)`
        - :attr:`anndata.AnnData.obsm` ``['local_r']`` with  `2)`
        - :attr:`anndata.AnnData.obsm` ``['local_pvals']`` with  `3)`

        """
        if pvalue_method not in ['analytical', 'permutation']:
            raise ValueError('pvalue_method must be one of [analytical, permutation]')

        temp, lr_res, ligand_pos, receptor_pos = _global_lr_pipe(adata=adata,
                                                                 resource_name=resource_name,
                                                                 resource=resource,
                                                                 expr_prop=expr_prop,
                                                                 use_raw=use_raw,
                                                                 layer=layer,
                                                                 verbose=verbose,
                                                                 _key_cols=self.key_cols,
                                                                 _complex_cols=self.complex_cols,
                                                                 _obms_keys=self.obsm_keys
                                                                 )

        # n / sum(W) for Moran's I
        norm_factor = temp.obsm['proximity'].shape[0] / temp.obsm['proximity'].sum()
        dist = csr_matrix(norm_factor * temp.obsm['proximity'])

        # we use the same gene expression matrix for both x and y
        lr_res['global_r'], lr_res['global_pvals'] = \
            _global_spatialdm(x_mat=temp.X,
                              y_mat=temp.X,
                              x_pos=ligand_pos,
                              y_pos=receptor_pos,
                              xy_dataframe=lr_res,
                              dist=dist,
                              seed=seed,
                              n_perm=n_perm,
                              pvalue_method=pvalue_method,
                              positive_only=positive_only
                              )
        local_r, local_pvals = _local_spatialdm(x_mat=temp.X,
                                                y_mat=temp.X,
                                                x_pos=ligand_pos,
                                                y_pos=receptor_pos,
                                                xy_dataframe=lr_res,
                                                dist=dist,  # TODO msq?
                                                seed=seed,
                                                n_perm=n_perm,
                                                pvalue_method=pvalue_method,
                                                positive_only=positive_only
                                                )

        # convert to dataframes
        local_r = _local_to_dataframe(array=local_r,
                                      idx=temp.obs.index,
                                      columns=lr_res.interaction)
        local_pvals = _local_to_dataframe(array=local_pvals,
                                          idx=temp.obs.index,
                                          columns=lr_res.interaction)

        if inplace:
            adata.uns['global_res'] = lr_res
            adata.obsm['local_r'] = local_r
            adata.obsm['local_pvals'] = local_pvals

        return None if inplace else (lr_res, local_r, local_pvals)


def _global_spatialdm(x_mat,
                      y_mat,
                      x_pos,
                      y_pos,
                      xy_dataframe,
                      dist,
                      seed,
                      n_perm,
                      pvalue_method,
                      positive_only,
                      x_key = 'ligand',
                      y_key = 'receptor'):
    """
    Global Moran's Bivariate I as implemented in SpatialDM

    Parameters
    ----------
    x_mat
        Gene expression matrix for entity x (e.g. ligand)
    y_mat
        Gene expression matrix for entity y (e.g. receptor)
    x_pos
        Index positions of entity x (e.g. ligand) in `mat`
    y_pos
        Index positions of entity y (e.g. receptor) in `mat`
    xy_dataframe
        a dataframe with x,y relationships to be estimated, for example `lr_res`.
    dist
        proximity weight matrix, obtained e.g. via `liana.method.get_spatial_proximity`.
        Note that for spatialDM/Morans'I `dist` has to be weighed by n / sum(W).
    seed
        Reproducibility seed
    n_perm
        Number of permutatins to perform (if `pvalue_method`=='permutation')
    pvalue_method
        Method to estimate pseudo p-value, must be in ['permutation', 'analytical']
    positive_only
        Whether to return only p-values for positive spatial correlations.
        By default, `True`.

    Returns
    -------
    Tupple of 2 1D Numpy arrays of size xy_dataframe.shape[1],
    or in other words calculates global_I and global_pval for
    each interaction in `xy_dataframe`

    """

    # normalize matrices
    x_mat = _standardize_matrix(x_mat, local=False)
    y_mat = _standardize_matrix(y_mat, local=False)

    # convert to spot_n x lr_n matrices
    x_mat = _get_ordered_matrix(mat=x_mat,
                                pos=x_pos,
                                order=xy_dataframe[x_key])
    y_mat = _get_ordered_matrix(mat=y_mat,
                                pos=y_pos,
                                order=xy_dataframe[y_key])

    # Get global r
    global_r = ((x_mat @ dist) * y_mat).sum(axis=1)

    # calc p-values
    if pvalue_method == 'permutation':
        global_pvals = _global_permutation_pvals(x_mat=x_mat,
                                                 y_mat=y_mat,
                                                 dist=dist,
                                                 global_r=global_r,
                                                 n_perm=n_perm,
                                                 positive_only=positive_only,
                                                 seed=seed
                                                 )
    elif pvalue_method == 'analytical':
        global_pvals = _global_zscore_pvals(dist=dist,
                                            global_r=global_r,
                                            positive_only=positive_only)

    return global_r, global_pvals



def _global_permutation_pvals(x_mat, y_mat, dist, global_r, n_perm, positive_only, seed):
    """
    Calculate permutation pvals

    Parameters
    ----------
    x_mat
        Matrix with x variables
    y_mat
        Matrix with y variables
    dist
        Proximity weights 2D array
    global_r
        Global Moran's I, 1D array
    n_perm
        Number of permutations
    positive_only
        Whether to mask negative p-values
    seed
        Reproducibility seed

    Returns
    -------
    1D array with same size as global_r

    """
    assert isinstance(dist, csr_matrix)
    rng = np.random.default_rng(seed)

    # initialize mat /w n_perm * number of X->Y
    idx = x_mat.shape[1]

    # permutation mat /w n_perms x LR_n
    perm_mat = np.zeros((n_perm, global_r.shape[0]))

    for perm in tqdm(range(n_perm)):
        _idx = rng.permutation(idx)
        perm_mat[perm, :] = ((x_mat[:, _idx] @ dist) * y_mat).sum(axis=1) # flipped x_mat

    if positive_only:
        global_pvals = 1 - (global_r > perm_mat).sum(axis=0) / n_perm
    else:
        # TODO Proof this makes sense
        global_pvals = 2 * (1 - (np.abs(global_r) > np.abs(perm_mat)).sum(axis=0) / n_perm)

    return global_pvals



def _local_spatialdm(x_mat,
                     y_mat,
                     x_pos,
                     y_pos,
                     xy_dataframe,
                     dist,
                     n_perm,
                     seed,
                     pvalue_method,
                     positive_only,
                     x_key = 'ligand',
                     y_key = 'receptor'
                     ):
    """
    Local Moran's Bivariate I as implemented in SpatialDM

    Parameters
    ----------
    x_mat
        Matrix with x variables
    y_mat
        Matrix with y variables
    x_pos
        Index positions of entity x (e.g. ligand) in `mat`
    y_pos
        Index positions of entity y (e.g. receptor) in `mat`
    xy_dataframe
        a dataframe with x,y relationships to be estimated, for example `lr_res`.
    dist
        proximity weight matrix, obtained e.g. via `liana.method.get_spatial_proximity`.
        Note that for spatialDM/Morans'I `dist` has to be weighed by n / sum(W).
    seed
        Reproducibility seed
    n_perm
        Number of permutatins to perform (if `pvalue_method`=='permutation')
    pvalue_method
        Method to estimate pseudo p-value, must be in ['permutation', 'analytical']
    positive_only
        Whether to return only p-values for positive spatial correlations.
        By default, `True`.

    Returns
    -------
        Tupple of two 2D Numpy arrays of size (n_spots, n_xy),
         or in other words calculates local_I and local_pval for
         each interaction in `xy_dataframe` and each sample in mat
    """
    x_mat = _standardize_matrix(x_mat, local=True)
    y_mat = _standardize_matrix(y_mat, local=True)

    ligand_mat = _get_ordered_matrix(mat=x_mat,
                                     pos=x_pos,
                                     order=xy_dataframe[x_key])
    receptor_mat = _get_ordered_matrix(mat=y_mat,
                                       pos=y_pos,
                                       order=xy_dataframe[y_key])
    ligand_mat, receptor_mat = ligand_mat.T, receptor_mat.T
    local_r = _calculate_local_moransI(ligand_mat, receptor_mat, dist)

    if pvalue_method == 'permutation':
        local_pvals = _local_permutation_pvals(x_mat=ligand_mat,
                                               y_mat=receptor_mat,
                                               dist=dist,
                                               local_truth=local_r,
                                               local_fun=_calculate_local_moransI,
                                               n_perm=n_perm,
                                               seed=seed,
                                               positive_only=positive_only
                                               )
    elif pvalue_method == 'analytical':
        local_pvals = _local_zscore_pvals(x_mat=ligand_mat,
                                          y_mat=receptor_mat,
                                          local_r=local_r,
                                          dist=dist,
                                          positive_only=positive_only)

    return local_r.T, local_pvals.T


def _standardize_matrix(mat, local=True):
    mat = np.array(mat - np.array(mat.mean(axis=0)))
    if not local:
        mat = mat / np.sqrt(np.sum(mat ** 2, axis=0, keepdims=True))
    return mat


# TODO Check why they omit m_squared?
def _divide_by_msq(mat):
    # how msq looks for uni-variate moran
    spot_n = mat.shape[0]
    msq = (np.sum(mat ** 2, axis=0) / (spot_n - 1))
    return mat / msq


def _get_ordered_matrix(mat, pos, order):
    _indx = np.array([pos[x] for x in order])
    return mat[:, _indx].T


def _global_zscore_pvals(dist, global_r, positive_only):
    """

    Parameters
    ----------
    dist
        proximity weight matrix (spot_n x spot_n)
    global_r
        Array with
    positive_only: bool
        whether to mask negative correlation p-values

    Returns
    -------
        1D array with the size of global_r

    """
    dist = np.array(dist.todense())
    spot_n = dist.shape[0]

    # global distance variance as in spatialDM
    numerator = spot_n ** 2 * ((dist * dist).sum()) - \
                (2 * spot_n * (dist @ dist).sum()) + \
                (dist.sum() ** 2)
    denominator = spot_n ** 2 * (spot_n - 1) ** 2
    dist_var_sq = (numerator / denominator) ** (1 / 2)

    global_zscores = global_r / dist_var_sq

    if positive_only:
        global_zpvals = norm.sf(global_zscores)
    else:
        global_zpvals = norm.sf(np.abs(global_zscores)) * 2

    return global_zpvals


def _calculate_local_moransI(x_mat, y_mat, dist):
    """

    Parameters
    ----------
    x_mat
        2D array with x variables
    y_mat
        2D array with y variables
    dist
    
    Returns
    -------
    Returns 2D array of local Moran's I with shape(n_spot, xy_n)

    """
    local_x = x_mat * (dist @ y_mat)
    local_y = x_mat * (dist @ y_mat)
    local_r = (local_x + local_y).T

    return local_r


def _local_zscore_pvals(x_mat, y_mat, local_r, dist, positive_only):
    """

    Parameters
    ----------
    x_mat
        2D array with x variables
    y_mat
        2D array with y variables
    local_r
        2D array with Local Moran's I
    dist
        proximity weights
    positive_only
        Whether to mask negative correlations pvalue

    Returns
    -------
    2D array of p-values with shape(n_spot, xy_n)

    """
    spot_n = dist.shape[0]

    x_norm = np.apply_along_axis(norm.fit, axis=0, arr=x_mat)
    y_norm = np.apply_along_axis(norm.fit, axis=0, arr=y_mat)

    # get x,y std
    x_sigma, y_sigma = x_norm[1, :], y_norm[1, :]

    x_sigma = x_sigma * spot_n / (spot_n - 1)
    y_sigma = y_sigma * spot_n / (spot_n - 1)

    std = _get_local_var(x_sigma, y_sigma, dist, spot_n)
    local_zscores = local_r / std

    if positive_only:
        local_zpvals = norm.sf(local_zscores)
        pos_msk = ((x_mat > 0) + (y_mat > 0)).T  # mask?
        local_zpvals[~pos_msk] = 1
    else:
        local_zpvals = norm.sf(np.abs(local_zscores))

    return local_zpvals


def _get_local_var(x_sigma, y_sigma, dist, spot_n):
    """

    Parameters
    ----------
    x_sigma
        Standard deviations for each x (e.g. std of all ligands in the matrix)
    y_sigma
        Standard deviations for each y (e.g. std of all receptors in the matrix)
    dist
        proximity weight matrix
    spot_n
        number of spots/cells in the matrix

    Returns
    -------
    2D array of standard deviations with shape(n_spot, xy_n)

    """
    dist_sq = (np.array(dist.todense()) ** 2).sum(axis=1)

    n_weight = 2 * (spot_n - 1) ** 2 / spot_n ** 2
    sigma_prod = x_sigma * y_sigma
    core = n_weight * sigma_prod

    var = np.multiply.outer(dist_sq, core) + core
    std = var ** (1 / 2)

    return std.T


# initialize instance
_spatialdm = SpatialMethod(
    method_name="SpatialDM",
    key_cols=['ligand_complex', 'receptor_complex'],
    reference="Zhuoxuan, L.I., Wang, T., Liu, P. and Huang, Y., 2022. SpatialDM: Rapid "
              "identification of spatially co-expressed ligand-receptor reveals cell-cell "
              "communication patterns. bioRxiv. "
)

spatialdm = SpatialDM(_method=_spatialdm,
                      _complex_cols=['ligand_means', 'receptor_means'],
                      _obsm_keys=['proximity']
                      )


