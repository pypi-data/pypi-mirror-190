from bbcpy.functions.normalizations import baseline
import numpy as np
import pytest

def test_baseline():
    assert True


# WIP
# def test_baseline():
#     dummy_epo = np.ones((10, 16, 100))  # (samples x channels x epochs)
#     idxref = [20, 80]
#     time = np.array([range(np.int(idxref[0]),
#                            np.int(idxref[1])+1)])
#     epo_t = np.linspace(idxref[0], idxref[1], time.shape[1])
#
#     idxref_2 = [20, 120]
#
#     # raise if the idxref is out of the range
#     with pytest.raises(ValueError):
#         baseline(dummy_epo, idxref_2)
#
#     # Check if the mean is correct
#     epo_norm = baseline(dummy_epo, idxref)
#     t_epo_norm = np.ones((10, 16, 100))
#     t_epo_norm[:, :, epo_t] = 0
#     assert t_epo_norm == epo_norm
