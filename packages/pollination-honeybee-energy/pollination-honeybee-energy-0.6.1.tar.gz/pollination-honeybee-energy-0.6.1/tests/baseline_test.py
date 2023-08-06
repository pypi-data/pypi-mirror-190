from pollination.honeybee_energy.baseline import ModelToBaseline
from queenbee.plugin.function import Function


def test_model_to_baseline():
    function = ModelToBaseline().queenbee
    assert function.name == 'model-to-baseline'
    assert isinstance(function, Function)
