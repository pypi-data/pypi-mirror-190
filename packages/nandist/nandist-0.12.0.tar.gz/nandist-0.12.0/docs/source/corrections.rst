Overview
=========

The library ``nandist`` works in two ways based on the API that is used.

1. Distance functions
2. Pairwise distance functions

Distance functions
------------------

When using distance functions (such as ``nandist.euclidean``) to calculate distances between two arrays :math:`u` and :math:`v`, ``nandist`` works as follows:

1. It creates two new vectors :math:`u'` and :math:`v'` where components :math:`i` are removed if :math:`u_i` or :math:`v_i` were NaN.
2. It calls ``scipy.spatial.distance`` and passes the vectors :math:`u'` and :math:`v'`

.. note:: *Easy implementation*

    This is why ``nandist`` easily supports all distance functions offered by ``scipy.spatial``.

Pairwise functions
------------------

When using pairwise distance calculating functions to calculate pairwise distances between arrays in a single collection :math:`\mathbf{X}`` (``nandist.pdist``) or pairwise distances between arrays in two collections :math:`\mathbf{A}` and :math:`\mathbf{B}` (``nandist.cdist``), ``nandist`` works as follows:

1. It creates replacement collections :math:`\mathbf{X}'` (or :math:`\mathbf{A}'` and :math:`\mathbf{B}'`) where each component :math:`X_{i,j}` is replaced by :math:`0` if that component is NaN
2. It calls ``scipy.spatial.distance.pdist`` (or ``scipy.spatial.distance.cdist``) and passes the replacement collection :math:`\mathbf{X}'` (or :math:`\mathbf{A}'` and :math:`\mathbf{B}'`), returning the pairwise distance matrix :math:`\mathbf{Y}'`, which contains over-estimations of pairwise distances
3. It applies corrections to the over-estimated components of :math:`\mathbf{Y}'`

.. note:: *Computational speed versus correctness*

    By calling the optimized ``scipy.spatial.distance.pdist`` and ``scipy.spatial.distance.cdist`` functions under the hood, ``nandist`` offers almost the same computational speeds as ``scipy``.
    The only additional computational costs are incurred by changing the input matrix (or matrices) and by applying the corrections.

    On the other hand, these corrections can introduce numerical errors into returned distance matrix.
    Moreover, each distance metric requires its own correction.

Corrections
===========

Derivations for the corrections are given here.

Notation
--------
We introduce some general notational conveniences.

Vectors and arrays
^^^^^^^^^^^^^^^^^^

We denote vectors using normal type face :math:`u`.
A component `i` of that vector is indicated using :math:`u_i`.
We might define a vector using :math:`u = (u_1, u_2, \ldots, u_n)`.
In linear algebraic expressions, we will denote the vector :math:`u` in bold: :math:`\mathbf{u} = [u_1, u_2, \ldots, u_n]`.
These two forms may be used interchangeably.


Indicator set
^^^^^^^^^^^^^

.. math::
    :label: index_u

    \mathcal{U} = \{i \mid u_i \ne \text{NaN}\}

In :eq:`index_u` we define the indicator set :math:`\mathcal{U}` to be the indices of the vector :math:`u` that are not missing (NaN).
Similarly we can define the index set :math:`\mathcal{V}` for indices of the vector :math:`v` that are not NaN.

.. math::
    :label: complement_index_u

    \overline{\mathcal{U}} = \{i \mid u_i = \text{NaN}\}

In :eq:`complement_index_u` the complement set to :math:`\mathcal{U}` is defined, which contains all the indices of vector :math:`u` that *are* missing (NaN).


.. admonition:: *Example*

    Let's consider a vector :math:`u = (1, 0, \mathrm{NaN}, 1)`.
    Then, the corresponding indexing set :math:`\mathcal{U} = \{0, 1, 3\}`.
    Its complement :math:`\overline{\mathcal{U}} = \{2\}`.

Indicator matrix
^^^^^^^^^^^^^^^^

.. math::
    :label: indicator_u

    \begin{align}
    \mathbf{I}_{\mathcal{U}} \rightarrow I_{u,i} = \begin{cases}
    1  & \text{if}\; i \in \mathcal{U} \\
    0 & \text{otherwise}
    \end{cases}
    \end{align}

In :eq:`indicator_u` an "indicator matrix" :math:`\mathbf{I}_{\mathcal{U}}` is introduced for a matrix of vectors :math:`u` where each matrix component :math:`I_{u,i}` has value :math:`1` if the component :math:`i` is in the index set :math:`\mathcal{U}` for the vector :math:`u`.
This corresponds to having values :math:`1` in the matrix where vector components are not missing.
A "NaN" indicating matrix can be constructed simply by using a different indication set, i.e. :math:`\mathbf{I}_{\overline{\mathcal{U}}` will have values :math:`1` in the matrix where vector components _are_ missing.

.. admonition:: *Example*

    Let's consider a matrix :math:`\mathbf{U} = [\mathbf{u}_1, \mathbf{u}_2]` of vectors :math:`\mathbf{u}_1 = [1, 0, \mathrm{NaN}, 1]` and :math:`\mathbf{u}_2 = [\mathrm{NaN}, 1, 0, 1]`.
    Then, the corresponding indicator matrix for not-missing components :math:`\mathbf{I}_{\mathcal{U}}` is:

    .. math::

        \mathbf{I}_{\mathcal{U}} = \begin{bmatrix}
            1, 1, 0, 1 \\
            0, 1, 1, 1
        \end{bmatrix}

    And its complement indicator matrix for indicating missing components :math:`\mathbf{I}_{\overline{\mathcal{U}}}` is:

    .. math::

        \mathbf{I}_{\overline{\mathcal{U}}} = \begin{bmatrix}
            0, 0, 1, 0 \\
            1, 0, 0, 0
        \end{bmatrix}

In ``numpy``, the equivalents are:

.. code-block:: python

    # Indicator for NaN values in U:
    np.isnan(U)

    # Indicator for not-NaN values in U:
    ~np.isnan(U)


Minkowski
---------

The weighted Minkowski distance :math:`d` is given by:

.. math::
    :label: minkowski

    d = {\|u-v\|}_p = \left(\sum{w_i(|(u_i - v_i)|^p)}\right)^{1/p}.

When replacing NaN components in :math:`u` and :math:`v` with :math:`0`, the resulting distance :math:`d'` is over-estimated.
We can expand the sum components to identify how much the distance is overestimated.
For ease of notation we also raise both sides of the equation to the power of the Minkowski parameter :math:`p`.

.. math::
    :label: minkowski-overestimation

    \begin{split}
    d'^p &= &\sum{w_i(|(u'_i - v'_i)|^p)} \\
       &= &\sum\limits_{i \in {\mathcal{U}\cap\mathcal{V}}}{w_i|(u'_i - v'_i)|^p} \\
       & &+\sum\limits_{i \in {\overline{\mathcal{U}}}}{w_i|(-v'_i)|^p} \\
       & &+ \sum\limits_{i \in {\overline{\mathcal{V}}}}{w_i|(u'_i)|^p}
    \end{split}

The second and third summations cause the over-estimation of the pairwise distances.
Hence, these must be subtracted from the distance :math:`d'^p` to get the correct distance :math:`d^p`.

In the distance matrix :math:`\mathbf{Y}'` each component :math:`y'_{u,v}` represents the calculated distance between :math:`u'` and :math:`v'`.
Each component :math:`y'_{u,v}` must be corrected if there are NaNs in either :math:`u` or :math:`v`.

Corrections are performed in four steps:

1. Raise each component of :math:`\mathbf{Y}'` to the power :math:`p`
2. Decrease each component :math:`y'_{u,v}` with the value :math:`\sum_{i \in {\overline{\mathcal{U}}}}{w_i|(-v'_i)|^p}`
3. Decrease each component :math:`y'_{u,v}` with the value :math:`\sum_{i \in {\overline{\mathcal{V}}}}{w_i|u'_i|^p}`
4. Raise each component of the resulting matrix to the power :math:`1/p`

.. warning:: *Computational inaccuracies*

    Each of these steps can introduce numerical inaccuracies.

To correct each component, we create correction matrices of the same shape as the distance matrix :math:`\mathbf{Y}'` so we can simply operate element-wise.
A pseudo-implementation is shown below.

.. code-block:: python
    :caption: Pseudo-implementation for Minkowski corrections

    import numpy as np
    import scipy

    def cdist_minkowski(U, V, w=None, p=2):
        """Pseudo-implementation of pairwise Minkowski distance calculations"""
        # Replace NaNs with zeros
        U0, V0 = np.nan_to_num(U), np.nan_to_num(V)

        # First estimate of distance matrix D (raised to minkowski parameter p)
        Dp = scipy.spatial.distance.cdist(U0, V0, 'minkowski', w=w, p=p) ** p

        # Corrections
        Dp -= np.matmul(np.isnan(U), (w*np.abs(V0)**p).T)
        Dp -= np.matmul(w*np.abs(U0)**p, np.isnan(V).T)

        # Return corrected distances raised to the power 1/p
        return Dp**(1/p)

.. note::
    *Applicability*

    Through its parameter :math:`p`, the Minkowski distance is a generalized distance metric for other distance metrics such as the cityblock (:math:`p=1`) and Euclidean (:math:`p=2`) distance metrics.
    Hence, corrections for these distance metrics are the same.

Cosine
------

The cosine distance :math:`d` is defined by:

.. math::

    d = 1 - \frac{u \cdot v}{\|u\|_2 \|v\|_2}.


All NaN components in :math:`u` and :math:`v` are first replaced with :math:`0`, leading to the distance value :math:`d'`.

.. math::

    d' = 1 - \frac{u' \cdot v'}{\|u'\|_2 \|v'\|_2}.

An overestimation occurs in the components :math:`\|u'\|_2` and :math:`\|v'\|_2`.
This over-estimation is with respect to the true values they would have if components in :math:`u` and :math:`v` were removed if that component is missing in either :math:`u` or :math:`v`.

.. admonition:: *Example*

    If :math:`u = (1, 0, \text{NaN})` and :math:`v = (1, 1, 1)`, then by removing the last component (because it is NaN in :math:`u`) would lead to :math:`u = (1, 0)` and :math:`v = (1, 1)`.
    The values of :math:`\|u\|_2 = 1` and :math:`\|v\|_2 = \sqrt{2}`.

    However, if we replace missing values with zeros, we would get :math:`u' = (1, 0, 0)` and :math:`v' = (1, 1, 1)`.
    The values of :math:`\|u'\|_2 = 1` and :math:`\|v'\|_2 = \sqrt{3}`.

    Note that :math:`\|v'\|_2 = \sqrt{3}` overestimates its true value :math:`\|v\|_2 = \sqrt{2}`.

We first identify that the numerator of the fraction is not affected by zero-replacement:

.. math::
    u \cdot v = u' \cdot v'

Using some algebraic manipulation, we derive an expression for the true distance :math:`d`:

.. math::

    \begin{align}
    u \cdot v &= u' \cdot v' \\
    \|u\|_2\|v\|_2 \left(1 - d\right) &= \|u'\|_2\|v'\|_2 \left(1 - d'\right) \\
    d &= 1 - \frac{\|u'\|_2\|v'\|_2}{\|u\|_2\|v\|_2}\left(1 - d'\right)
    \end{align}

This is implemented as follows:

.. code-block:: python
    :caption: Pseudo-implementation for cosine corrections

    import numpy as np
    import scipy

    def cdist_cosine(U, V, w=None, p=2):
        """Pseudo-implementation of pairwise cosine distance calculations"""
        # Replace NaNs with zeros
        U0, V0 = np.nan_to_num(U), np.nan_to_num(V)

        # Distances D (uncorrected)
        D = scipy.spatial.distance.cdist(U0, V0, 'cosine', w=w, )

        # Numerator (norms of U0, V0)
        num = np.sqrt(
            np.matmul(np.square(U0), (w * np.ones_like(V)).T)
            )
            * np.sqrt(
                np.matmul(w * np.ones_like(U), np.square(V0).T)
           )

        # Denominator (norms of U, V with nans removed)
        den = np.sqrt(
            np.matmul(np.square(U0), w.T * ~np.isnan(V).T)
            )
            * np.sqrt(
            np.matmul(w * ~np.isnan(U), np.square(V0).T)
        )

        # Return corrected distances
        return 1 - (num/den)*(1-D)
