from pathlib import Path

import pytest
import yaml

from fencer.api_spec import APISpec, BasicEndpoint


@pytest.fixture
def orders_spec():
    return yaml.safe_load((Path(__file__).parent / 'orders_api_spec.yaml').read_text())


def test_load_endpoints(orders_spec):
    api_spec = APISpec(spec=orders_spec, base_url='')
    api_spec.load_endpoints()
    spec_endpoints = [
        endpoint.endpoint for endpoint in api_spec.endpoints
    ]
    expected_endpoints = [
        BasicEndpoint(method='get', path='/orders', base_url=''),
        BasicEndpoint(method='post', path='/orders', base_url=''),
        BasicEndpoint(method='get', path='/orders/{order_id}', base_url=''),
        BasicEndpoint(method='put', path='/orders/{order_id}', base_url=''),
        BasicEndpoint(method='delete', path='/orders/{order_id}', base_url=''),
        BasicEndpoint(method='post', path='/orders/{order_id}/cancel', base_url=''),
    ]
    assert len(expected_endpoints) == len(spec_endpoints)
    for endpoint in expected_endpoints:
        assert endpoint in spec_endpoints


def test_produce_path_parameter():
    pass


def test_capture_query_params():
    pass


def test_produce_query_param_value():
    pass


def test_resolve_component():
    pass


def test_resolve_anyof_component():
    pass


def test_resolve_allof_component():
    pass



