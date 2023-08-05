from hestia_earth.schema import TermTermType, PracticeStatsDefinition
from hestia_earth.utils.model import find_term_match, filter_list_term_type
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.completeness import _is_term_type_incomplete
from hestia_earth.models.utils.practice import _new_practice
from hestia_earth.models.utils.term import get_lookup_value
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.cropResidue": "False",
        "or": {
            "products": [
                {"@type": "Product", "term.@id": "aboveGroundCropResidueTotal", "value": "> 0"},
                {"@type": "Product", "term.@id": "aboveGroundCropResidueRemoved", "value": "> 0"}
            ],
            "completeness.products": "True"
        }
    }
}
RETURNS = {
    "Practice": [{
        "value": "0",
        "statsDefinition": "modelled"
    }]
}
LOOKUPS = {
    "crop": "isAboveGroundCropResidueRemoved"
}
TERM_ID = 'residueRemoved'


def _practice(value: float = 0):
    practice = _new_practice(TERM_ID)
    practice['value'] = [value]
    practice['statsDefinition'] = PracticeStatsDefinition.MODELLED.value
    return practice


def _run_from_products(cycle: dict):
    products = cycle.get('products', [])
    total = list_sum(find_term_match(products, 'aboveGroundCropResidueTotal').get('value', [0]))
    removed = list_sum(find_term_match(products, 'aboveGroundCropResidueRemoved').get('value', [0]))
    return [_practice(removed / total * 100)]


def _should_run_from_products(cycle: dict):
    crop_residue_incomplete = _is_term_type_incomplete(cycle, {'termType': TermTermType.CROPRESIDUE.value})
    products = cycle.get('products', [])
    aboveGroundCropResidueTotal = list_sum(find_term_match(products, 'aboveGroundCropResidueTotal').get('value', [0]))
    has_aboveGroundCropResidueTotal = aboveGroundCropResidueTotal > 0
    aboveGroundCropResidueRemoved = list_sum(
        find_term_match(products, 'aboveGroundCropResidueRemoved').get('value', [0]))
    has_aboveGroundCropResidueRemoved = aboveGroundCropResidueRemoved > 0

    logRequirements(cycle, model=MODEL, term=TERM_ID, by='products',
                    crop_residue_incomplete=crop_residue_incomplete,
                    has_aboveGroundCropResidueTotal=has_aboveGroundCropResidueTotal,
                    has_aboveGroundCropResidueRemoved=has_aboveGroundCropResidueRemoved)

    should_run = all([crop_residue_incomplete, has_aboveGroundCropResidueTotal, has_aboveGroundCropResidueRemoved])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, by='products')
    return should_run


def _is_residue_removed(product: dict):
    return get_lookup_value(product.get('term', {}), 'isAboveGroundCropResidueRemoved', model=MODEL, term=TERM_ID)


def _should_run_from_lookup(cycle: dict):
    products_complete = cycle.get('completeness', {}).get('products', False)
    crop_residue_incomplete = _is_term_type_incomplete(cycle, {'termType': TermTermType.CROPRESIDUE.value})
    crops = filter_list_term_type(cycle.get('products', []), TermTermType.CROP)
    removed_crops = list(filter(_is_residue_removed, crops))
    no_residue_removed_crops = len(removed_crops) == 0

    logRequirements(cycle, model=MODEL, term=TERM_ID, by='lookup',
                    products_complete=products_complete,
                    crop_residue_incomplete=crop_residue_incomplete,
                    no_residue_removed_crops=no_residue_removed_crops)

    should_run = all([products_complete, crop_residue_incomplete, no_residue_removed_crops])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, by='lookup')
    return should_run


def run(cycle: dict):
    return [_practice()] if _should_run_from_lookup(cycle) else (
        _run_from_products(cycle) if _should_run_from_products(cycle) else []
    )
