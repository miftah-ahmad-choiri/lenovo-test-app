import pandas as pd


def read_excel_info(file_path):

    lower_name = (
        file_path.lower()
    )

    try:

        if lower_name.endswith(
            ".csv"
        ):

            df = pd.read_csv(
                file_path
            )

        else:

            df = pd.read_excel(
                file_path
            )

        return {
            "rows":
                len(df),

            "columns":
                df.columns.tolist()
        }

    except Exception as e:

        return {
            "error":
                str(e)
        }