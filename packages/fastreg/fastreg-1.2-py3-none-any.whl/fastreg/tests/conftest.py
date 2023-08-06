import pytest
import fastreg as fr

seed = 2385198437

@pytest.fixture(params=[10_000, 100_000])
def data(request):
    N = request.param
    return fr.dataset(N=N, K1=5, K2=20, models='linear', seed=seed)

@pytest.fixture(params=[10_000])
def data_count(request):
    N = request.param
    return fr.dataset(
        N=N, K1=5, K2=20, models=['poisson', 'poisson_offset', 'poisson_zinf'],
        seed=seed
    )
