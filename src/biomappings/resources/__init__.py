# -*- coding: utf-8 -*-

"""Biomappings resources."""

import csv
import itertools as itt
import os
from typing import Any, Dict, Iterable, List, Mapping, NamedTuple, Sequence, Tuple

from biomappings.utils import RESOURCE_PATH, get_canonical_tuple

MAPPINGS_HEADER = [
    "source prefix",
    "source identifier",
    "source name",
    "relation",
    "target prefix",
    "target identifier",
    "target name",
    "type",
    "source",
]
PREDICTIONS_HEADER = [
    "source prefix",
    "source identifier",
    "source name",
    "relation",
    "target prefix",
    "target identifier",
    "target name",
    "type",
    "confidence",
    "source",
]


class MappingTuple(NamedTuple):
    """A named tuple class for mappings."""

    source_prefix: str
    source_id: str
    source_name: str
    relation: str
    target_prefix: str
    target_identifier: str
    target_name: str
    type: str
    source: str

    def as_dict(self) -> Mapping[str, str]:
        """Get the mapping tuple as a dictionary."""
        return dict(zip(MAPPINGS_HEADER, self))

    @classmethod
    def from_dict(cls, mapping: Mapping[str, str]) -> "MappingTuple":
        """Get the mapping tuple from a dictionary."""
        return cls(*[mapping[key] for key in MAPPINGS_HEADER])


class PredictionTuple(NamedTuple):
    """A named tuple class for predictions."""

    source_prefix: str
    source_id: str
    source_name: str
    relation: str
    target_prefix: str
    target_identifier: str
    target_name: str
    type: str
    confidence: float
    source: str

    def as_dict(self) -> Mapping[str, Any]:
        """Get the prediction tuple as a dictionary."""
        return dict(zip(PREDICTIONS_HEADER, self))

    @classmethod
    def from_dict(cls, mapping: Mapping[str, str]) -> "PredictionTuple":
        """Get the prediction tuple from a dictionary."""
        return cls(*[mapping[key] for key in PREDICTIONS_HEADER])


def get_resource_file_path(fname) -> str:
    """Get a resource by its file name."""
    return os.path.join(RESOURCE_PATH, fname)


def _load_table(fname) -> List[Dict[str, str]]:
    with open(fname, "r") as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)
        return [dict(zip(header, row)) for row in reader]


def _write_helper(
    header: Sequence[str], lod: Iterable[Mapping[str, str]], path: str, mode: str
) -> None:
    lod = sorted(lod, key=mapping_sort_key)
    with open(path, mode) as file:
        if mode == "w":
            print(*header, sep="\t", file=file)
        for line in lod:
            print(*[line[k] for k in header], sep="\t", file=file)


def mapping_sort_key(prediction: Mapping[str, str]) -> Tuple[str, ...]:
    """Return a tuple for sorting mapping dictionaries."""
    return (
        prediction["source prefix"],
        prediction["source identifier"],
        prediction["relation"],
        prediction["target prefix"],
        prediction["target identifier"],
        prediction["type"],
        prediction["source"],
    )


TRUE_MAPPINGS_PATH = get_resource_file_path("mappings.tsv")


def load_mappings() -> List[Dict[str, str]]:
    """Load the mappings table."""
    return _load_table(TRUE_MAPPINGS_PATH)


def append_true_mappings(m: Iterable[Mapping[str, str]], sort: bool = False) -> None:
    """Append new lines to the mappings table."""
    _write_helper(MAPPINGS_HEADER, m, TRUE_MAPPINGS_PATH, "a")
    if sort:
        write_true_mappings(sorted(load_mappings(), key=mapping_sort_key))


def append_true_mapping_tuples(mappings: Iterable[MappingTuple]) -> None:
    """Append new lines to the mappings table."""
    append_true_mappings(mapping.as_dict() for mapping in mappings)


def write_true_mappings(m: Iterable[Mapping[str, str]]) -> None:
    """Write mappigns to the true mappings file."""
    _write_helper(MAPPINGS_HEADER, m, TRUE_MAPPINGS_PATH, "w")


def lint_true_mappings() -> None:
    """Lint the true mappings file"""
    write_true_mappings(sorted(load_mappings(), key=mapping_sort_key))


FALSE_MAPPINGS_PATH = get_resource_file_path("incorrect.tsv")


def load_false_mappings() -> List[Dict[str, str]]:
    """Load the false mappings table."""
    return _load_table(FALSE_MAPPINGS_PATH)


def append_false_mappings(m: Iterable[Mapping[str, str]], sort: bool = False) -> None:
    """Append new lines to the false mappings table."""
    _write_helper(MAPPINGS_HEADER, m, FALSE_MAPPINGS_PATH, "a")
    if sort:
        write_false_mappings(sorted(load_false_mappings(), key=mapping_sort_key))


def write_false_mappings(m: Iterable[Mapping[str, str]]) -> None:
    """Write mappings to the false mappings file."""
    _write_helper(MAPPINGS_HEADER, m, FALSE_MAPPINGS_PATH, "w")


def lint_false_mappings() -> None:
    """Lint the false mappings file."""
    write_false_mappings(sorted(load_false_mappings(), key=mapping_sort_key))


UNSURE_PATH = get_resource_file_path("unsure.tsv")


def load_unsure() -> List[Dict[str, str]]:
    """Load the unsure table."""
    return _load_table(UNSURE_PATH)


def append_unsure_mappings(m: Iterable[Mapping[str, str]], sort: bool = False) -> None:
    """Append new lines to the "unsure" mappings table."""
    _write_helper(MAPPINGS_HEADER, m, UNSURE_PATH, "a")
    if sort:
        write_unsure_mappings(sorted(load_unsure(), key=mapping_sort_key))


def write_unsure_mappings(m: Iterable[Mapping[str, str]]) -> None:
    """Write mappings to the unsure mappings file."""
    _write_helper(MAPPINGS_HEADER, m, UNSURE_PATH, "w")


def lint_unsure_mappings() -> None:
    """Lint the unsure mappings file."""
    write_unsure_mappings(sorted(load_unsure(), key=mapping_sort_key))


PREDICTIONS_PATH = get_resource_file_path("predictions.tsv")


def load_predictions() -> List[Dict[str, str]]:
    """Load the predictions table."""
    return _load_table(PREDICTIONS_PATH)


def write_predictions(m: Iterable[Mapping[str, str]]) -> None:
    """Write new content to the predictions table."""
    _write_helper(PREDICTIONS_HEADER, m, PREDICTIONS_PATH, "w")


def append_prediction_tuples(
    prediction_tuples: Iterable[PredictionTuple], deduplicate: bool = True, sort: bool = False
) -> None:
    """Append new lines to the predictions table that come as canonical tuples."""
    append_predictions(
        (prediction_tuple.as_dict() for prediction_tuple in prediction_tuples),
        deduplicate=deduplicate,
        sort=sort,
    )


def append_predictions(
    mappings: Iterable[Mapping[str, str]], deduplicate: bool = True, sort: bool = False
) -> None:
    """Append new lines to the predictions table."""
    if deduplicate:
        existing_mappings = {
            get_canonical_tuple(existing_mapping)
            for existing_mapping in itt.chain(
                load_mappings(),
                load_false_mappings(),
                load_predictions(),
            )
        }
        mappings = (
            mapping for mapping in mappings if get_canonical_tuple(mapping) not in existing_mappings
        )

    _write_helper(PREDICTIONS_HEADER, mappings, PREDICTIONS_PATH, "a")
    if sort:
        write_predictions(sorted(load_predictions(), key=mapping_sort_key))


def lint_predictions() -> None:
    """Lint the predictions file."""
    write_predictions(sorted(load_predictions(), key=mapping_sort_key))


def load_curators():
    """Load the curators table."""
    return _load_table(get_resource_file_path("curators.tsv"))


def filter_predictions(custom_filter: Mapping[str, Mapping[str, Mapping[str, str]]]) -> None:
    """Filter all of the predictions by removing what's in the custom filter then re-write.

    :param custom_filter: A filter 3-dictionary of source prefix to target prefix
        to source identifier to target identifier
    """
    predictions = load_predictions()
    predictions = [
        prediction for prediction in predictions if _check_filter(prediction, custom_filter)
    ]
    write_predictions(predictions)


def _check_filter(
    prediction: Mapping[str, str],
    custom_filter: Mapping[str, Mapping[str, Mapping[str, str]]],
) -> bool:
    source_prefix, target_prefix = prediction["source prefix"], prediction["target prefix"]
    source_id, target_id = prediction["source identifier"], prediction["target identifier"]
    return target_id != custom_filter.get(source_prefix, {}).get(target_prefix, {}).get(source_id)
