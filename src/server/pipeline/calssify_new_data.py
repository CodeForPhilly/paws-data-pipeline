import pandas as pd
import re
import os
import io
import datetime

from datasource_manager import DATASOURCE_MAPPING, SOURCE_NORMALIZATION_MAPPING
from flask import current_app
from config import CURRENT_SOURCE_FILES_PATH
from datetime import datetime
from models import Base


def start(pdp_contacts_df, normalized_data):
    result = {
        "new": pd.DataFrame(columns=pdp_contacts_df.columns),
        "updated": pd.DataFrame(columns=pdp_contacts_df.columns)
    }

    partial_merge = normalized_data.merge(pdp_contacts_df, how="outer", indicator="_indication",
                                          left_on=["source_id", "source_type"], right_on=["source_id", "source_type"])

    result["new"] = partial_merge[partial_merge["_indication"] == "left_only"]

    overlapping_rows = partial_merge[partial_merge["_indication"] == "both"]

    return result
