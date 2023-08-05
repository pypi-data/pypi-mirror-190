from unittest.mock import patch
import json
from tests.utils import fake_new_practice, fixtures_path

from hestia_earth.models.cycle.residueRemoved import (
    MODEL, TERM_ID, _should_run_from_lookup, _should_run_from_products, run
)

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


def test_should_run_from_lookup():
    # no products => run
    cycle = {'completeness': {'products': True}}
    assert _should_run_from_lookup(cycle) is True

    # with crop products
    cycle['products'] = [{'term': {'termType': 'crop'}}]

    # with residue removed product => not run
    cycle['products'][0]['term']['@id'] = 'wheatStraw'
    assert not _should_run_from_lookup(cycle)

    # without residue removed product => run
    cycle['products'][0]['term']['@id'] = 'wheatGrain'
    assert _should_run_from_lookup(cycle) is True


def test_should_run():
    # no products => no run
    cycle = {'completeness': {'cropResidue': False}, 'products': []}
    should_run = _should_run_from_products(cycle)
    assert not should_run

    # with `aboveGroundCropResidueTotal` => no run
    cycle['products'].append({'term': {'@id': 'aboveGroundCropResidueTotal'}, 'value': [10]})
    should_run = _should_run_from_products(cycle)
    assert not should_run

    # with `aboveGroundCropResidueRemoved` => run
    cycle['products'].append({'term': {'@id': 'aboveGroundCropResidueRemoved'}, 'value': [10]})
    should_run = _should_run_from_products(cycle)
    assert should_run is True


@patch(f"{class_path}._new_practice", side_effect=fake_new_practice)
def test_run_from_lookup(*args):
    with open(f"{fixtures_folder}/from-lookup/cycle.jsonld", encoding='utf-8') as f:
        data = json.load(f)

    with open(f"{fixtures_folder}/from-lookup/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(data)
    assert result == expected


@patch(f"{class_path}._new_practice", side_effect=fake_new_practice)
def test_run_from_products(*args):
    with open(f"{fixtures_folder}/from-products/cycle.jsonld", encoding='utf-8') as f:
        data = json.load(f)

    with open(f"{fixtures_folder}/from-products/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(data)
    assert result == expected
