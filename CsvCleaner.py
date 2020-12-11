import pandas as pd
from pandas.errors import EmptyDataError


def clean_data_generator(file_name):
    try:
        csv_data = pd.read_csv(str(file_name) + ".csv")
        clean_data = csv_data['Yandex'].unique()
        clean_dataframe = pd.DataFrame(clean_data, columns=['Yandex'])
        clean_dataframe.to_csv(file_name + "_clean.csv", mode='a', index=False, header=True)
        print("Number of Clean Data:" + str(len(clean_dataframe)) + "\nNumber of First Data:" + str(
            len(csv_data)) + "\nPercentage of Clean Data:" + str((len(clean_dataframe) / len(csv_data)) * 100))
    except (KeyError, EmptyDataError):
        print("Probably yandex realize you!")
