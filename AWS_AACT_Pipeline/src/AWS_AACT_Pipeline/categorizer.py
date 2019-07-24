import os
import numpy as np
import json
import re


class Categorizer(object):

    def __init__(self):
        self.obj = None
        self.nan_filler = "Other"

    def read_file_conditions(self, filename):
        # Get file location
        file_path = os.path.dirname(os.path.abspath(__file__))
        parent = os.path.dirname(os.path.dirname(file_path))
        data_path = os.path.join(parent, "json_keys/" + filename)

        with open(data_path, 'r') as file:
            data = file.read()
        self.obj = json.loads(data)

    def check_conditions(self, name):
        result = self.nan_filler
        is_condition_met = False
        for label in self.obj:
            for comparison in self.obj[label]:
                if re.search(comparison, str(name)) is not None:
                    result = label
                    is_condition_met = True
                    break
            if is_condition_met:
                break
        return result

    def categorize(self, original_col, new_column_name, df):
        func = np.vectorize(self.check_conditions)
        condition_type = func(df[original_col])
        df[new_column_name] = condition_type

        # print value counts so the user can see the categorization numbers for the new column
        print("Value counts for " + new_column_name + ": ")
        print(df[new_column_name].value_counts())
