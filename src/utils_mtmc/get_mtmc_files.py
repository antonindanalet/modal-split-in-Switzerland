import pandas as pd
import numpy as np
from pathlib import Path


folder_path_2015 = Path('../data/input/2015/mtmc15')
folder_path_2010 = Path('../data/input/2010/mtmc10')
folder_path_2005 = Path('../data/input/2005/mtmc05')


def get_zp(year, selected_columns=None):
    if year == 2010:
        with open(folder_path_2010 / 'zielpersonen.csv', 'r', encoding='latin1') as zielpersonen_file:
            if selected_columns is None:
                df_zp = pd.read_csv(zielpersonen_file,
                                    delimiter=';',
                                    dtype={'HHNR': int,
                                           'ZIELPNR': int,
                                           'WP': np.longdouble,
                                           'gesl': int,
                                           'nation': int})
            else:
                df_zp = pd.read_csv(zielpersonen_file,
                                    delimiter=';',
                                    dtype={'HHNR': int,
                                           'ZIELPNR': int,
                                           'WP': np.longdouble,
                                           'gesl': int,
                                           'nation': int},
                                    usecols=selected_columns)
    elif year == 2015:
        with open(folder_path_2015 / 'zielpersonen.csv', 'r', encoding='latin1') as zielpersonen_file:
            if selected_columns is None:
                df_zp = pd.read_csv(zielpersonen_file)
            else:
                df_zp = pd.read_csv(zielpersonen_file,
                                    dtype={'HHNR': int},
                                    usecols=selected_columns)
    elif year == 2005:
        with open(folder_path_2005 / 'zielpersonen.dat', 'r') as zielpersonen_file:
            if selected_columns is None:
                df_zp = pd.read_csv(zielpersonen_file,
                                    sep='\t')
            else:
                df_zp = pd.read_csv(zielpersonen_file,
                                    dtype={'HHNR': int},
                                    usecols=selected_columns,
                                    sep='\t')
    else:
        raise Exception("Cannot get data for other years than 2005, 2010 and 2015! (zp)")
    return df_zp


def get_hh(year, selected_columns=None):
    if year == 2015:
        with open(folder_path_2015 / 'haushalte.csv', 'r', encoding='latin1') as haushalte_file:
            df_hh = pd.read_csv(haushalte_file,
                                dtype={'HHNR': int},
                                usecols=selected_columns)
    elif year == 2010:
        with open(folder_path_2010 / 'haushalte.csv', 'r', encoding='latin1') as haushalte_file:
            df_hh = pd.read_csv(haushalte_file,
                                sep=';',
                                dtype={'HHNR': int},
                                usecols=selected_columns)
    elif year == 2005:
        with open(folder_path_2005 / 'Haushalte.dat', 'r') as haushalte_file:
            df_hh = pd.read_csv(haushalte_file,
                                sep='\t',
                                dtype={'HHNR': int},
                                usecols=selected_columns)
    else:
        raise Exception("Cannot get data for other years than 2010 and 2015! (hh)")
    return df_hh


def get_etappen(year, selected_columns=None):
    if year == 2015:
        with open(folder_path_2015 / 'etappen.csv', 'r', encoding='latin1') as etappen_file:
            df_etappen = pd.read_csv(etappen_file,
                                     dtype={'HHNR': int,
                                            'W_AGGLO_GROESSE2012': int},
                                     usecols=selected_columns)
    elif year == 2010:
        with open(folder_path_2010 / 'etappen.csv', 'r', encoding='latin1') as etappen_file:
            df_etappen = pd.read_csv(etappen_file,
                                     sep=';',
                                     dtype={'HHNR': int},
                                     usecols=selected_columns)
    elif year == 2005:
        with open(folder_path_2005 / 'etappen.dat', 'r') as etappen_file:
            df_etappen = pd.read_csv(etappen_file,
                                     sep='\t',
                                     na_values=' ',
                                     dtype={'HHNR': int,
                                            'ZIELPNR': int,
                                            'E_AUSLAND': int,
                                            'PSEUDO': int,
                                            'F510': int,
                                            'rdist': float},
                                     usecols=selected_columns)
    else:
        raise Exception("Cannot get data for other years than 2010 and 2015! (etappen)")
    return df_etappen
