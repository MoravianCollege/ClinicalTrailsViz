import pandas as pd

ex_dict = {
    'number': [200, 100, 300],
    'category': ['Foo', 'Foo', 'Other']
}

# create a list of strings
columns = ['number', 'category']

index = ['row1', 'row2', 'row3']

df = pd.DataFrame(ex_dict, columns=columns, index=index)

print(df)