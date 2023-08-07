from __future__ import annotations

import logging
import pathlib
import re
from dataclasses import dataclass
from pprint import pformat as pf
from typing import TYPE_CHECKING, Any, Type

import pydantic
import pytest
from pytest import MonkeyPatch, param

import great_expectations.exceptions as ge_exceptions
import great_expectations.execution_engine.pandas_execution_engine
from great_expectations.experimental.datasources.dynamic_pandas import PANDAS_VERSION
from great_expectations.experimental.datasources.interfaces import TestConnectionError
from great_expectations.experimental.datasources.pandas_datasource import (
    CSVAsset,
    JSONAsset,
    PandasDatasource,
    _FilesystemDataAsset,
)

if TYPE_CHECKING:
    from great_expectations.alias_types import PathStr
    from great_expectations.data_context import AbstractDataContext
    from great_expectations.experimental.datasources.interfaces import (
        BatchSortersDefinition,
    )

logger = logging.getLogger(__file__)

# apply markers to entire test module
pytestmark = [
    pytest.mark.skipif(
        PANDAS_VERSION < 1.2, reason=f"ZEP pandas not supported on {PANDAS_VERSION}"
    )
]


@pytest.fixture
def pandas_datasource() -> PandasDatasource:
    return PandasDatasource(name="pandas_datasource")


@pytest.fixture
def csv_path() -> pathlib.Path:
    relative_path = pathlib.Path(
        "..", "..", "test_sets", "taxi_yellow_tripdata_samples"
    )
    abs_csv_path = (
        pathlib.Path(__file__).parent.joinpath(relative_path).resolve(strict=True)
    )
    return abs_csv_path


class SpyInterrupt(RuntimeError):
    """
    Exception that may be raised to interrupt the control flow of the program
    when a spy has already captured everything needed.
    """


@pytest.fixture
def capture_reader_fn_params(monkeypatch: MonkeyPatch):
    """
    Capture the `reader_options` arguments being passed to the `PandasExecutionEngine`.

    Note this fixture is heavily reliant on the implementation details of `PandasExecutionEngine`,
    should this change this fixture will need to change.
    """
    captured_args: list[list] = []
    captured_kwargs: list[dict[str, Any]] = []

    def reader_fn_spy(*args, **kwargs):
        logging.info(f"reader_fn_spy() called with...\n{args}\n{kwargs}")
        captured_args.append(args)
        captured_kwargs.append(kwargs)
        raise SpyInterrupt("Reader options have been captured")

    monkeypatch.setattr(
        great_expectations.execution_engine.pandas_execution_engine.PandasExecutionEngine,
        "_get_reader_fn",
        lambda *_: reader_fn_spy,
        raising=True,
    )

    yield captured_args, captured_kwargs


@pytest.mark.unit
class TestDynamicPandasAssets:
    @pytest.mark.parametrize(
        "method_name",
        [
            param("read_clipboard"),
            param("read_csv"),
            param("read_excel"),
            param("read_feather"),
            param(
                "read_fwf", marks=pytest.mark.xfail(reason="unhandled type annotation")
            ),
            param("read_gbq"),
            param("read_hdf"),
            param("read_html"),
            param("read_json"),
            param("read_orc"),
            param("read_parquet"),
            param("read_pickle"),
            param("read_sas"),
            param("read_spss"),
            param(
                "read_sql",
                marks=pytest.mark.xfail(reason="conflict with 'sql' type name"),
            ),
            param(
                "read_sql_query",
                marks=pytest.mark.xfail(reason="type name logic expects 'sqlquery'"),
            ),
            param(
                "read_sql_table",
                marks=pytest.mark.xfail(reason="type name logic expects 'sqltable'"),
            ),
            param("read_stata"),
            param(
                "read_table",
                marks=pytest.mark.xfail(reason="conflict with 'table' type name"),
            ),
            param(
                "read_xml",
                marks=pytest.mark.skipif(
                    PANDAS_VERSION < 1.2,
                    reason=f"read_xml does not exist on {PANDAS_VERSION} ",
                ),
            ),
        ],
    )
    def test_data_asset_defined_for_io_read_method(self, method_name: str):
        _, type_name = method_name.split("read_")
        assert type_name

        asset_class_names: set[str] = {
            t.__name__.lower().split("asset")[0] for t in PandasDatasource.asset_types
        }
        print(asset_class_names)

        assert type_name in asset_class_names

    @pytest.mark.parametrize("asset_class", PandasDatasource.asset_types)
    def test_minimal_validation(self, asset_class: Type[_FilesystemDataAsset]):
        """
        These parametrized tests ensures that every `PandasDatasource` asset model does some minimal
        validation, and doesn't accept arbitrary keyword arguments.
        This is also a proxy for testing that the dynamic pydantic model creation was successful.
        """
        with pytest.raises(pydantic.ValidationError) as exc_info:
            asset_class(  # type: ignore[call-arg]
                name="test",
                base_directory=pathlib.Path(__file__),
                regex=re.compile(r"yellow_tripdata_sample_(\d{4})-(\d{2})"),
                invalid_keyword_arg="bad",
            )

        errors_dict = exc_info.value.errors()
        assert {
            "loc": ("invalid_keyword_arg",),
            "msg": "extra fields not permitted",
            "type": "value_error.extra",
        } == errors_dict[  # the extra keyword error will always be the last error
            -1  # we don't care about any other errors for this test
        ]

    @pytest.mark.parametrize(
        ["asset_model", "extra_kwargs"],
        [
            (CSVAsset, {"sep": "|", "names": ["col1", "col2", "col3"]}),
            (JSONAsset, {"orient": "records", "convert_dates": True}),
        ],
    )
    def test_data_asset_defaults(
        self,
        asset_model: Type[_FilesystemDataAsset],
        extra_kwargs: dict,
    ):
        """
        Test that an asset dictionary can be dumped with only the original passed keys
        present.
        """
        kwargs: dict[str, Any] = {
            "name": "test",
            "base_directory": pathlib.Path(__file__),
            "regex": re.compile(r"yellow_tripdata_sample_(\d{4})-(\d{2})"),
        }
        kwargs.update(extra_kwargs)
        print(f"extra_kwargs\n{pf(extra_kwargs)}")
        asset_instance = asset_model(**kwargs)
        assert asset_instance.dict(exclude={"type"}) == kwargs

    @pytest.mark.parametrize(
        "extra_kwargs",
        [
            {"sep": "|", "decimal": ","},
            {"usecols": [0, 1, 2], "names": ["foo", "bar"]},
            {"dtype": {"col_1": "Int64"}},
        ],
    )
    def test_data_asset_reader_options_passthrough(
        self,
        empty_data_context: AbstractDataContext,
        csv_path: pathlib.Path,
        capture_reader_fn_params: tuple[list[list], list[dict]],
        extra_kwargs: dict,
    ):
        batch_request = (
            empty_data_context.sources.add_pandas("my_pandas")
            .add_csv_asset(
                "my_csv",
                base_directory=csv_path,
                regex=r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2}).csv",
                **extra_kwargs,
            )
            .get_batch_request({"year": "2018"})
        )
        with pytest.raises(SpyInterrupt):
            empty_data_context.get_validator(batch_request=batch_request)

        captured_args, captured_kwargs = capture_reader_fn_params
        print(f"positional args:\n{pf(captured_args[-1])}\n")
        print(f"keyword args:\n{pf(captured_kwargs[-1])}")

        assert captured_kwargs[-1] == extra_kwargs


@pytest.mark.unit
def test_construct_pandas_datasource(pandas_datasource: PandasDatasource):
    assert pandas_datasource.name == "pandas_datasource"


@pytest.mark.unit
def test_add_csv_asset_to_datasource(
    pandas_datasource: PandasDatasource, csv_path: pathlib.Path
):
    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(\d{4})-(\d{2}).csv",
    )
    assert asset.name == "csv_asset"  # type: ignore[attr-defined]
    assert asset.base_directory == csv_path  # type: ignore[attr-defined]
    assert asset.regex.match("random string") is None  # type: ignore[attr-defined]
    assert asset.regex.match("yellow_tripdata_sample_11D1-22.csv") is None  # type: ignore[attr-defined]
    m1 = asset.regex.match("yellow_tripdata_sample_1111-22.csv")  # type: ignore[attr-defined]
    assert m1 is not None


@pytest.mark.unit
def test_construct_csv_asset_directly(csv_path: pathlib.Path):
    # noinspection PyTypeChecker
    asset = CSVAsset(  # type: ignore[call-arg]
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(\d{4})-(\d{2}).csv",  # type: ignore[arg-type]
    )
    assert asset.name == "csv_asset"
    assert asset.base_directory == csv_path
    assert asset.regex.match("random string") is None
    assert asset.regex.match("yellow_tripdata_sample_11D1-22.csv") is None
    m1 = asset.regex.match("yellow_tripdata_sample_1111-22.csv")
    assert m1 is not None


@pytest.mark.unit
def test_csv_asset_with_regex_unnamed_parameters(
    pandas_datasource: PandasDatasource, csv_path: pathlib.Path
):
    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(\d{4})-(\d{2}).csv",
    )
    options = asset.batch_request_options_template()  # type: ignore[attr-defined]
    assert options == {"batch_request_param_1": None, "batch_request_param_2": None}


@pytest.mark.unit
def test_csv_asset_with_regex_named_parameters(
    pandas_datasource: PandasDatasource, csv_path: pathlib.Path
):
    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2}).csv",
    )
    options = asset.batch_request_options_template()  # type: ignore[attr-defined]
    assert options == {"year": None, "month": None}


@pytest.mark.unit
def test_csv_asset_with_some_regex_named_parameters(
    pandas_datasource: PandasDatasource, csv_path: pathlib.Path
):
    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(\d{4})-(?P<month>\d{2}).csv",
    )
    options = asset.batch_request_options_template()  # type: ignore[attr-defined]
    assert options == {"batch_request_param_1": None, "month": None}


@pytest.mark.unit
def test_csv_asset_with_non_string_regex_named_parameters(
    pandas_datasource: PandasDatasource, csv_path: pathlib.Path
):
    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(\d{4})-(?P<month>\d{2}).csv",
    )
    with pytest.raises(ge_exceptions.InvalidBatchRequestError):
        # year is an int which will raise an error
        asset.get_batch_request({"year": 2018, "month": "04"})  # type: ignore[attr-defined]


@pytest.mark.unit
def test_get_batch_list_from_fully_specified_batch_request(
    pandas_datasource: PandasDatasource, csv_path: pathlib.Path
):
    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2}).csv",
    )
    request = asset.get_batch_request({"year": "2018", "month": "04"})  # type: ignore[attr-defined]
    batches = asset.get_batch_list_from_batch_request(request)  # type: ignore[attr-defined]
    assert len(batches) == 1
    batch = batches[0]
    assert batch.batch_request.datasource_name == pandas_datasource.name
    assert batch.batch_request.data_asset_name == asset.name  # type: ignore[attr-defined]
    assert batch.batch_request.options == {"year": "2018", "month": "04"}
    assert batch.metadata == {
        "year": "2018",
        "month": "04",
        "base_directory": asset.base_directory / "yellow_tripdata_sample_2018-04.csv",  # type: ignore[attr-defined]
    }
    assert batch.id == "pandas_datasource-csv_asset-year_2018-month_04"


@pytest.mark.unit
def test_get_batch_list_from_partially_specified_batch_request(
    pandas_datasource: PandasDatasource, csv_path: pathlib.Path
):
    # Verify test directory has files that don't match what we will query for
    file_name: PathStr
    all_files: list[str] = [
        file_name.stem for file_name in list(pathlib.Path(csv_path).iterdir())
    ]
    # assert there are files that are not csv files
    assert any([not file_name.endswith("csv") for file_name in all_files])
    # assert there are 12 files from 2018
    files_for_2018 = [
        file_name for file_name in all_files if file_name.find("2018") >= 0
    ]
    assert len(files_for_2018) == 12

    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2}).csv",
    )
    request = asset.get_batch_request({"year": "2018"})  # type: ignore[attr-defined]
    batches = asset.get_batch_list_from_batch_request(request)  # type: ignore[attr-defined]
    assert (len(batches)) == 12
    batch_filenames = [
        pathlib.Path(batch.metadata["base_directory"]).stem for batch in batches
    ]
    assert set(files_for_2018) == set(batch_filenames)

    @dataclass(frozen=True)
    class YearMonth:
        year: str
        month: str

    expected_year_month = {
        YearMonth(year="2018", month=format(m, "02d")) for m in range(1, 13)
    }
    batch_year_month = {
        YearMonth(year=batch.metadata["year"], month=batch.metadata["month"])
        for batch in batches
    }
    assert expected_year_month == batch_year_month


@pytest.mark.unit
@pytest.mark.parametrize(
    "order_by",
    [
        ["+year", "month"],
        ["+year", "+month"],
        ["+year", "-month"],
        ["year", "month"],
        ["year", "+month"],
        ["year", "-month"],
        ["-year", "month"],
        ["-year", "+month"],
        ["-year", "-month"],
        ["month", "+year"],
        ["+month", "+year"],
        ["-month", "+year"],
        ["month", "year"],
        ["+month", "year"],
        ["-month", "year"],
        ["month", "-year"],
        ["+month", "-year"],
        ["-month", "-year"],
    ],
)
def test_pandas_sorter(
    pandas_datasource: PandasDatasource,
    csv_path: pathlib.Path,
    order_by: BatchSortersDefinition,
):
    # Verify test directory has files we expect
    years = ["2018", "2019", "2020"]
    months = [format(m, "02d") for m in range(1, 13)]
    file_name: PathStr
    all_files: list[str] = [
        file_name.stem for file_name in list(pathlib.Path(csv_path).iterdir())
    ]
    # assert there are 12 files for each year
    for year in years:
        files_for_year = [
            file_name
            for file_name in all_files
            if file_name.find(f"yellow_tripdata_sample_{year}") == 0
        ]
        assert len(files_for_year) == 12

    asset = pandas_datasource.add_csv_asset(
        name="csv_asset",
        base_directory=csv_path,
        regex=r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2}).csv",
        order_by=order_by,
    )
    batches = asset.get_batch_list_from_batch_request(asset.get_batch_request())  # type: ignore[attr-defined]
    assert (len(batches)) == 36

    @dataclass(frozen=True)
    class TimeRange:
        key: str
        range: list[str]

    ordered_years = reversed(years) if "-year" in order_by else years
    ordered_months = reversed(months) if "-month" in order_by else months
    if "year" in order_by[0]:  # type: ignore[operator]
        ordered = [
            TimeRange(key="year", range=ordered_years),  # type: ignore[arg-type]
            TimeRange(key="month", range=ordered_months),  # type: ignore[arg-type]
        ]
    else:
        ordered = [
            TimeRange(key="month", range=ordered_months),  # type: ignore[arg-type]
            TimeRange(key="year", range=ordered_years),  # type: ignore[arg-type]
        ]

    batch_index = -1
    for range1 in ordered[0].range:
        key1 = ordered[0].key
        for range2 in ordered[1].range:
            key2 = ordered[1].key
            batch_index += 1
            metadata = batches[batch_index].metadata
            assert metadata[key1] == range1
            assert metadata[key2] == range2


def bad_base_directory_config() -> tuple[pathlib.Path, re.Pattern, TestConnectionError]:
    base_directory = pathlib.Path("/this/path/is/not/here")
    regex = re.compile(r"yellow_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2}).csv")
    test_connection_error = TestConnectionError(
        f"Path: {base_directory.resolve()} does not exist."
    )
    return base_directory, regex, test_connection_error


def bad_regex_config() -> tuple[pathlib.Path, re.Pattern, TestConnectionError]:
    relative_path = pathlib.Path(
        "..", "..", "test_sets", "taxi_yellow_tripdata_samples"
    )
    base_directory = (
        pathlib.Path(__file__).parent.joinpath(relative_path).resolve(strict=True)
    )
    regex = re.compile(r"green_tripdata_sample_(?P<year>\d{4})-(?P<month>\d{2}).csv")
    test_connection_error = TestConnectionError(
        f"No file at path: {base_directory.resolve()} matched the regex: {regex.pattern}"
    )
    return base_directory, regex, test_connection_error


@pytest.fixture(params=[bad_base_directory_config, bad_regex_config])
def datasource_test_connection_error_messages(
    pandas_datasource: PandasDatasource, request
) -> tuple[PandasDatasource, TestConnectionError]:
    base_directory, regex, test_connection_error = request.param()
    csv_asset = CSVAsset(  # type: ignore[call-arg]
        name="csv_asset",
        base_directory=base_directory,
        regex=regex,
    )
    pandas_datasource.assets = {"csv_asset": csv_asset}
    return pandas_datasource, test_connection_error


@pytest.mark.unit
def test_test_connection_failures(
    datasource_test_connection_error_messages: tuple[
        PandasDatasource, TestConnectionError
    ]
):
    (
        pandas_datasource,
        test_connection_error,
    ) = datasource_test_connection_error_messages

    with pytest.raises(type(test_connection_error)) as e:
        pandas_datasource.test_connection()
    assert str(e.value) == str(test_connection_error)
