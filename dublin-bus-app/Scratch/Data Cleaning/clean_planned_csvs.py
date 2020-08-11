import glob
import pandas as pd
import numpy as np
	
def convert_number_to_digit(number):
    nums = {"Twenty": "2--",
            "Thirty": "3--",
            "Forty": "4--",
            "Fifty": "5--",
            "Sixty": "6--",
            "Seventy": "7--",
            "Eighty": "8--",
            "Ninety": "9--",
            "Ten": "10",
            "Eleven": "11",
            "Twelve": "12",
            "Thirteen": "13",
            "Fourteen": "14",
            "Fifteen": "15",
            "Sixteen": "16",
            "Seventeen": "17",
            "Eighteen": "18",
            "Nineteen": "19",
            "O": "0",
            "0ne": "1",
            "Two": "2",
            "Three": "3",
            "Four": "4",
            "Five": "5",
            "Six": "6",
            "Seven": "7",
            "Eight": "8",
            "Nine": "9"
            }

    for num in nums:
        number = number.replace(num, nums[num])
    idx = number.find("--")

    if idx == -1:
        pass
    elif (idx + 2) >= len(number):
        number = number.replace("--", "0")
    elif number[idx + 2] in "ABCDFEGHIJKLMNOPQRSTUVWXYZ":
        number = number.replace("--", "0")
    else:
        number = number.replace("--", "")
    return number




for filepath in glob.iglob('C:\\Users\\cls15\Desktop\\routes\\Master-Route-Files\\*.csv'):
    f = (filepath.split("\\")[-1])
    print(f"Reading csv {f}")
    df = pd.read_csv(filepath)

    new_file_name = convert_number_to_digit(f.split("_")[0])

    for column in df.columns:
        if column not in ["DAYOFSERVICE", "TRIPID", "PROGRNUMBER", "PLANNEDTIME_ARR", "LINEID", "ROUTEID"]:
            df = df.drop([column], axis=1)
    path = f"C:\\Users\\cls15\Desktop\\routes\\redone\\{new_file_name}.csv"
    print(f"Saving as {new_file_name}.csv")
    df.to_csv(path, index=False)

