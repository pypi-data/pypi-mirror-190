import numpy as np
import pytest

from bbcpy.functions.temporal import adjust_class_sizes, sliding_windows


@pytest.mark.parametrize("n_repetitions", [10, 20, 30])
def test_adjust_class_sizes(n_repetitions):
    y = np.repeat([0, 1, 1, 2, 2, 2], n_repetitions)
    classes, count = np.unique(y, return_counts=True)
    n_classes = len(classes)
    n_extracted = n_repetitions*5

    res = adjust_class_sizes(y, n_extracted)
    assert res.shape == (n_classes*n_extracted,)

    res = adjust_class_sizes(y)
    assert res.shape == (n_repetitions*n_classes,)

    res = adjust_class_sizes(y, int(n_repetitions//2))
    assert res.shape == ((n_repetitions*n_classes)//2,)


@pytest.mark.parametrize("label_handler", ['unique', 'mean', 'max', 'min',
                                           'first', 'last', 'center'])
def test_sliding_windows_label_handler(label_handler):
    """Test Sliding Windows label handler parameter."""
    n_channels = 3
    step_size = 4
    window_size = 8
    n_samples = 100
    X = np.random.rand(n_samples, n_channels)
    y = np.repeat([0, 1, 2, 3, 3], n_samples//5)

    X_win, y_win = sliding_windows(X,
                                   y=y,
                                   step_size=step_size,
                                   window_size=window_size,
                                   label_handling=label_handler
                                   )
    if label_handler == 'unique':
        n_expected_samples = 21
    else:
        n_expected_samples = np.ceil(n_samples / step_size) - 1
    assert X_win.shape == (n_expected_samples,
                           n_channels,
                           window_size)


def test_sliding_windows_label_handler2():
    """Test Sliding Windows label handler parameter."""
    n_channels = 3
    step_size = 4
    window_size = 8
    n_samples = 100

    X = np.random.rand(n_samples, n_channels)
    y = np.repeat([0, 1, 2, 3, 3], n_samples//5)

    X_win, y_win = sliding_windows(X,
                                   y=y,
                                   step_size=step_size,
                                   window_size=window_size,
                                   adjust_class_size=True
                                   )
    classes, counts = np.unique(y_win, return_counts=True)
    assert np.array_equal(classes, np.unique(y))
    assert np.sum(np.diff(counts)) == 0
