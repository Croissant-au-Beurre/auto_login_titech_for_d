from typing import Optional
import pandas as pd

class MatrixCodeData:
    def __init__(self, coordinates_dict:dict):
        self.__matrix_code: Optional[pd.DataFrame] = None
        self.__matrix_code = self.load_matrix_code(coordinates_dict)

    @property
    def matrix_code(self) -> list:
        """
        动态密码
        :return:
        """
        return self.__matrix_code

    def load_matrix_code(self, coordinates_dict:dict) -> list:
        df = pd.read_csv('matrix.csv')

        codes = []
        for index, item in coordinates_dict.items():
            row_index = item[1] - 1
            column_index = item[0]
            code = df.loc[row_index, column_index]
            codes.append(code)

        return codes
