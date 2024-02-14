# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
LOGGER = get_logger(__name__)

secret_file_path = st.secrets["connections"]["snowflake"]["private_key_file_path"]
with open(secret_file_path, "rb") as key:
  p_key = serialization.load_pem_private_key(
    key.read(),
    password=None,
    backend=default_backend()
  )

  pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
  )

conn = st.connection("snowflake", private_key=pkb)
conn.cursor().execute('use database FREE_DATASET_GZTSZAS2KFB')
query = conn.query("""
SELECT date, variable_name, value
FROM cybersyn.canada_statcan_timeseries
WHERE variable_name IN ('Current and capital accounts: Household saving rate, Seasonally adjusted at annual rates',
                    	'Core CPI: All-items excluding eight of the most volatile components and the effect of indirect taxes, seasonally adjusted')
  AND date >= '2010-01-01'
  AND geo_id = 'country/CAN';
""");
st.dataframe(query)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
