import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from ibsg import filter


@pytest.mark.parametrize(
    "bers,selected_postcodes,counties,expected_output",
    [
        (
            pd.DataFrame({"countyname": ["DUBLIN 11", "CO. GALWAY", "CO. CORK"]}),
            ["Dublin 11"],
            ["Dublin", "Galway", "Cork"],
            pd.DataFrame({"countyname": ["DUBLIN 11"]}),
        ),
        (
            pd.DataFrame({"countyname": ["Dublin", "Galway", "Cork"]}),
            ["Dublin", "Galway", "Cork"],
            ["Dublin", "Galway", "Cork"],
            pd.DataFrame(
                {
                    "countyname": ["Dublin", "Galway", "Cork"],
                }
            ),
        ),
    ],
)
def test_filter_by_substrings(
    bers, selected_postcodes, counties, expected_output, monkeypatch
):
    def _mock_multiselect(*args, **kwargs):
        return selected_postcodes

    monkeypatch.setattr("app.st.multiselect", _mock_multiselect)
    output = filter.filter_by_substrings(
        df=bers, column_name="countyname", all_substrings=counties
    )
    assert_frame_equal(output, expected_output)
