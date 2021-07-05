import datetime
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import streamlit as st

from ibsg import postcodes
from ibsg import small_areas


def main():
    st.header("🏠 Irish Building Stock Generator 🏠")
    st.markdown(
        """
        Generate a standardised building stock at postcode or small area level.

        - To use the open-access postcode BERs enter your email address below to enable
        this application to make an authenticated query to the SEAI at:
        https://ndber.seai.ie/BERResearchTool/Register/Register.aspx
        - To compress your closed-access small area BER dataset to a `zip` file of
        under 200MB or to open the output file `csv.gz` you might need to install
        [7zip](https://www.7-zip.org/)

       
        If you have any problems or questions:
        - Chat with us on [Gitter](https://gitter.im/energy-modelling-ireland/ibsg)
        - Or raise an issue on our [Github](https://github.com/energy-modelling-ireland/ibsg) 
        """
    )

    small_area_bers_zipfile = st.file_uploader(
        "Upload Small Area BERs",
        type="zip",
    )
    email_address = st.text_input("Enter your email address")

    if small_area_bers_zipfile:
        small_area_bers = small_areas.main(small_area_bers_zipfile)
        download_as_csv(small_area_bers, category="small_area")
    if email_address:
        postcode_bers = postcodes.main(email_address)
        download_as_csv(postcode_bers, category="postcode")


def _create_csv_download_link(df: pd.DataFrame, filename: str):
    # workaround from streamlit/streamlit#400
    STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / "static"
    DOWNLOADS_PATH = STREAMLIT_STATIC_PATH / "downloads"
    if not DOWNLOADS_PATH.is_dir():
        DOWNLOADS_PATH.mkdir()
    filepath = (DOWNLOADS_PATH / filename).with_suffix(".csv.gz")
    df.to_csv(filepath, index=False, compression="gzip")
    st.markdown(f"[{filepath.name}](downloads/{filepath.name})")


def download_as_csv(df, category: str):
    save_to_csv_selected = st.button("Save to csv.gz?")
    if save_to_csv_selected:
        _create_csv_download_link(
            df=df,
            filename=f"{category}_bers_{datetime.date.today()}",
        )


if __name__ == "__main__":
    main()
