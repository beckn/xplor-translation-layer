## File for the Translation Service
import json
import sys
sys.path.append('.')
from utils import *


@log_function_data
def rec_sys_input(input_data:  dict, type: str) -> dict:

    if type == "job":
        df = extract_job_data_to_df(input_data)
        sorted_df = df.sort_values(by=['Salary information', 'quantity.available.count'], ascending=[False, False])
        return sorted_df
    elif type == "course":
        df = extract_course_data_to_df(input_data)
        sorted_df = df.sort_values(by=['rating', 'price.value'], ascending=[False, True])
        return sorted_df
    elif type == "scholarship":
        df = extract_scholarship_data_to_df(input_data)
        return df
    elif type == "ondc":
        df = extract_ondc_to_df(input_data)
        sorted_df = df.sort_values(by=['rating'], ascending=[False])
        return sorted_df
    else:
        return "Error Occured. Please check input format !"
    





