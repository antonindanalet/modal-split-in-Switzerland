# coding=latin-1

import pandas as pd
import numpy as np
from pathlib import Path
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std
from utils_mtmc.get_mtmc_files import *
from utils_mtmc.codage import *


def run_residency_principle_by_bfs_numbers(list_of_commune_numbers):
    print('Computing modal split by commune number...')
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2015, group_of_modes=False, percentage=False)
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2015, group_of_modes=False, percentage=True)
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2015, group_of_modes=True, percentage=False)
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2015, group_of_modes=True, percentage=True)
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2010, group_of_modes=False, percentage=False)
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2010, group_of_modes=False, percentage=True)
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2010, group_of_modes=True, percentage=False)
    get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year=2010, group_of_modes=True, percentage=True)


def run_residency_principle_by_agglomeration():
    print('Computing modal split by agglomeration with MTMC data 2015...')
    get_modal_split_by_agglo(mrmt_year=2015, agglo_def=2012, group_of_modes=False, percentage=False)
    get_modal_split_by_agglo(mrmt_year=2015, agglo_def=2012, group_of_modes=True, percentage=False)
    get_modal_split_by_agglo(mrmt_year=2015, agglo_def=2012, group_of_modes=True, percentage=True)
    get_modal_split_by_agglo(mrmt_year=2015, agglo_def=2012, group_of_modes=False, percentage=True)
    get_modal_split_by_agglo(mrmt_year=2015, agglo_def=2000, group_of_modes=False, percentage=False)
    get_modal_split_by_agglo(mrmt_year=2015, agglo_def=2000, group_of_modes=True, percentage=False)
    get_modal_split_by_agglo(mrmt_year=2015, agglo_def=2000, group_of_modes=True, percentage=True)
    print('Computing modal split by agglomeration with MTMC data 2010...')
    get_modal_split_by_agglo(mrmt_year=2010, agglo_def=2000, group_of_modes=False, percentage=False)
    get_modal_split_by_agglo(mrmt_year=2010, agglo_def=2000, group_of_modes=False, percentage=True)
    get_modal_split_by_agglo(mrmt_year=2010, agglo_def=2000, group_of_modes=True, percentage=False)
    get_modal_split_by_agglo(mrmt_year=2010, agglo_def=2000, group_of_modes=True, percentage=True)


def get_modal_split_by_bfs_numbers(list_of_commune_numbers, mtmc_year, group_of_modes, percentage):
    if mtmc_year == 2015:
        folder_path_output = Path('../data/output/2015/')
        identification_columns = ['HHNR']
    elif mtmc_year == 2010:
        folder_path_output = Path('../data/output/2010/')
        identification_columns = ['HHNR', 'ZIELPNR']
    else:
        raise Exception("Year not well defined! It must be 2010 or 2015.")
    if group_of_modes:
        list_of_modes = ['Mobilité douce', 'Transport individuel motorisé', 'Transports publics', 'Autres']
        column_name_for_mode = 'group_of_modes'
    else:
        if mtmc_year == 2015:
            list_of_modes = ['A pied', 'Vélo (incl. vélo électrique)', 'Deux-roues motorisé', 'Voiture',
                             'Transports publics routiers', 'Train', 'Autres']
        elif mtmc_year == 2010:
            list_of_modes = ['A pied', 'Vélo (incl. vélo électrique)', 'Deux-roues motorisé', 'Voiture',
                             'Transports publics routiers', 'Train', 'Autres']
        else:
            raise Exception("Year not well defined! It must be 2010 or 2015.")
        column_name_for_mode = 'mode_simple'
    folder_path_output = folder_path_output / 'bfs_numbers\\'
    if percentage:
        columns = ['Numéro de commune BFS', 'Echantillon']
    else:
        columns = ['Numéro de commune BFS', 'Echantillon', 'Total', 'Total (+/-)']
    for mode_simple in list_of_modes:
        columns.extend([mode_simple, mode_simple + ' (+/-)'])
    df_for_csv = pd.DataFrame(columns=columns)
    df_zp = get_zp(year=mtmc_year, selected_columns=identification_columns + ['WP'])  # get the full list of HHNR
    if mtmc_year == 2015:
        df_etappen = get_etappen(mtmc_year,
                                 selected_columns=identification_columns + ['E_Ausland', 'pseudo', 'rdist',
                                                                            'f51300'])
        df_hh = get_hh(year=mtmc_year, selected_columns=['HHNR', 'W_BFS'])
    elif mtmc_year == 2010:
        df_etappen = get_etappen(mtmc_year,
                                 selected_columns=identification_columns + ['E_Ausland', 'pseudo', 'rdist',
                                                                            'f51300'])
        df_hh = get_hh(year=mtmc_year, selected_columns=['HHNR', 'W_BFS'])
    else:
        raise Exception("Year not well defined! It must be 2010 or 2015.")
    df_etappen = df_etappen[df_etappen.E_Ausland == 2]  # remove ausland trips
    del df_etappen['E_Ausland']
    df_etappen = df_etappen[df_etappen.pseudo == 1]  # remove pseudo etappen
    del df_etappen['pseudo']
    if mtmc_year == 2015:
        df_etappen['mode_simple'] = df_etappen['f51300'].map(dict_detailed_mode2main_mode_2015)
    elif mtmc_year == 2010:
        df_etappen['mode_simple'] = df_etappen['f51300'].map(dict_detailed_mode2main_mode_2010)
    del df_etappen['f51300']
    if group_of_modes:
        if mtmc_year == 2015:
            df_etappen['group_of_modes'] = df_etappen['mode_simple'].map(dict_main_mode2group_of_modes_2015)
        elif mtmc_year == 2010:
            df_etappen['group_of_modes'] = df_etappen['mode_simple'].map(dict_main_mode2group_of_modes_2010)
        del df_etappen['mode_simple']
    ''' Add non-mobile HHNR/ZP '''
    df_etappen = pd.merge(df_etappen, df_zp[identification_columns],
                          left_on=identification_columns, right_on=identification_columns, how='right')
    df_etappen['rdist'].fillna(0, inplace=True)  # replace NAN by 0
    df_etappen[column_name_for_mode].fillna('Autres', inplace=True)  # replace NAN by 'Autres
    ''' Include non-mobiles '''
    df_etappen = pd.merge(df_etappen, df_hh, left_on='HHNR', right_on='HHNR', how='left')
    # Filter: keep only the communes of interest
    df_etappen = df_etappen[df_etappen['W_BFS'].isin(list_of_commune_numbers)]
    # Results for list of communes
    dict_total_km, sample = compute_distances_and_confidence_interval_total(df_etappen, df_zp,
                                                                            identification_columns)
    dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_etappen, df_zp,
                                                                    percentage=percentage,
                                                                    identification_columns=identification_columns,
                                                                    group_of_modes=group_of_modes,
                                                                    list_of_modes=list_of_modes)
    dict_km_per_mode['Echantillon'] = sample
    list_of_bfs_numbers_as_text = ', '.join(str(bfs_numbers) for bfs_numbers in list_of_commune_numbers)
    dict_km_per_mode['Numéro de commune BFS'] = list_of_bfs_numbers_as_text
    if percentage is False:
        dict_km_per_mode.update(dict_total_km)
    df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
    for mode_simple in list_of_modes:
        df_for_csv[mode_simple].fillna(0, inplace=True)
        df_for_csv[mode_simple + ' (+/-)'].fillna('-', inplace=True)
    # File names
    if group_of_modes:
        if percentage:
            new_file_name = 'Parts_modes_de_transport_pourcentage_' + str(mtmc_year) + '.csv'
        else:
            new_file_name = 'Parts_modes_de_transport_distance_' + str(mtmc_year) + '.csv'
    else:
        if percentage:
            new_file_name = 'Parts_moyens_de_transport_pourcentage_' + str(mtmc_year) + '.csv'
        else:
            new_file_name = 'Parts_moyens_de_transport_distance_' + str(mtmc_year) + '.csv'
    # Save in folder output
    df_for_csv.to_csv(folder_path_output / 'FR' / new_file_name, index=False, sep=';', encoding='iso-8859-1')

    # Save in German
    # File names and headers in German
    if group_of_modes:
        if percentage:
            list_of_headers_in_german = ['BFS Gemeindenummer', 'Stichprobe',
                                         'Langsamverkehr', 'Langsamverkehr (+/-)',
                                         'motorisierter Individualverkehr', 'motorisierter Individualverkehr (+/-)',
                                         'öffentlicher Verkehr', 'öffentlicher Verkehr (+/-)',
                                         'übrige', 'übrige (+/-)']
            new_file_name = 'Anteil_Verkehrsmodus_Prozent_' + str(mtmc_year) + '.csv'
        else:
            list_of_headers_in_german = ['BFS Gemeindenummer', 'Stichprobe', 'Total', 'Total (+/-)',
                                         'Langsamverkehr', 'Langsamverkehr (+/-)',
                                         'motorisierter Individualverkehr', 'motorisierter Individualverkehr (+/-)',
                                         'öffentlicher Verkehr', 'öffentlicher Verkehr (+/-)',
                                         'übrige', 'übrige (+/-)']
            new_file_name = 'Anteil_Verkehrsmodus_Distanz_' + str(mtmc_year) + '.csv'
    else:
        if percentage:
            list_of_headers_in_german = ['BFS Gemeindenummer', 'Stichprobe',
                                         'zu Fuss', 'zu Fuss (+/-)',
                                         'Velo (inkl. E-Bike)', 'Velo (inkl. E-Bike) (+/-)',
                                         'motorisierte Zweiräder', 'motorisierte Zweiräder (+/-)',
                                         'Auto', 'Auto (+/-)',
                                         'öffentlicher Strassenverkehr', 'öffentlicher Strassenverkehr (+/-)',
                                         'Eisenbahn', 'Eisenbahn (+/-)',
                                         'übrige', 'übrige (+/-)']
            new_file_name = 'Anteil_Verkehrsmittel_Prozent_' + str(mtmc_year) + '.csv'
        else:
            list_of_headers_in_german = ['BFS Gemeindenummer', 'Stichprobe', 'Total', 'Total (+/-)',
                                         'zu Fuss', 'zu Fuss (+/-)',
                                         'Velo (inkl. E-Bike)', 'Velo (inkl. E-Bike) (+/-)',
                                         'motorisierte Zweiräder', 'motorisierte Zweiräder (+/-)',
                                         'Auto', 'Auto (+/-)',
                                         'öffentlicher Strassenverkehr', 'öffentlicher Strassenverkehr (+/-)',
                                         'Eisenbahn', 'Eisenbahn (+/-)',
                                         'übrige', 'übrige (+/-)']
            new_file_name = 'Anteil_Verkehrsmittel_Distanz_' + str(mtmc_year) + '.csv'
    # Save in folder output
    df_for_csv.to_csv(folder_path_output / 'DE' / new_file_name, index=False, sep=',', encoding='iso-8859-1',
                      header=list_of_headers_in_german)


def compute_distances_and_confidence_interval_total(df_etappen, df_zp, identification_columns, full_sample=False):
    dict_results = {}
    # Get the distance (rdist) by person
    table = pd.pivot_table(df_etappen, values='rdist', index=identification_columns, aggfunc=np.sum)
    if full_sample:
        table = table.reindex(df_zp['HHNR'])
        table.fillna(0, inplace=True)
    # Add the weight to the pivot table
    result = pd.merge(table, df_zp, left_index=True, right_on=identification_columns)
    dict_column_weighted_avg_and_std, sample = get_weighted_avg_and_std(result, weights='WP')
    dict_results['Total'] = dict_column_weighted_avg_and_std['rdist'][0]
    dict_results['Total (+/-)'] = dict_column_weighted_avg_and_std['rdist'][1]
    return dict_results, sample


def compute_distances_and_conf_interval_per_mode(df_etappen, df_zp, identification_columns, percentage,
                                                 list_of_modes,
                                                 group_of_modes=False,
                                                 full_sample=False):
    if percentage and list_of_modes == []:  # Percentage, without definition of list of modes!
        raise Exception('Warning: Try to compute percentage without a clear definition of the list of modes!',
                        list_of_modes)
    dict_of_results = {}
    if group_of_modes:
        table = pd.pivot_table(df_etappen, values='rdist', index=identification_columns, columns=['group_of_modes'],
                               aggfunc=np.sum)
    else:
        table = pd.pivot_table(df_etappen, values='rdist', index=identification_columns, columns=['mode_simple'],
                               aggfunc=np.sum)
    if full_sample:
        table = table.reindex(df_zp['HHNR'])
    table.fillna(0, inplace=True)
    # Add the weight to the pivot table
    result = pd.merge(table, df_zp, left_index=True, right_on=identification_columns, how='left')
    dict_column_weighted_avg_and_std, sample = get_weighted_avg_and_std(result, percentage=percentage, weights='WP',
                                                                        list_of_columns=list_of_modes)
    if group_of_modes:
        for group_of_mode in list_of_modes:
            if group_of_mode in dict_column_weighted_avg_and_std:
                dict_of_results[group_of_mode] = dict_column_weighted_avg_and_std[group_of_mode][0]
                dict_of_results[group_of_mode + ' (+/-)'] = dict_column_weighted_avg_and_std[group_of_mode][1]
    else:
        for mode_simple in list_of_modes:
            if mode_simple in dict_column_weighted_avg_and_std:
                dict_of_results[mode_simple] = dict_column_weighted_avg_and_std[mode_simple][0]
                dict_of_results[mode_simple + ' (+/-)'] = dict_column_weighted_avg_and_std[mode_simple][1]
    return dict_of_results


def get_modal_split_by_agglo(mrmt_year, agglo_def, group_of_modes, percentage):
    if mrmt_year == 2015:
        folder_path_output = Path('../data/output/2015/')
        identification_columns = ['HHNR']
    elif mrmt_year == 2010:
        folder_path_output = Path('../data/output/2010/')
        identification_columns = ['HHNR', 'ZIELPNR']
    else:
        raise Exception('Year of the MTMC not well defined! It should be 2010 or 2015.')
    if group_of_modes:
        list_of_modes = ['Mobilité douce', 'Transport individuel motorisé', 'Transports publics', 'Autres']
        column_name_for_mode = 'group_of_modes'
    else:
        if mrmt_year == 2015:
            list_of_modes = ['A pied', 'Vélo (incl. vélo électrique)', 'Deux-roues motorisé', 'Voiture',
                             'Transports publics routiers', 'Train', 'Autres']
        elif mrmt_year == 2010:
            list_of_modes = ['A pied', 'Vélo', 'Deux-roues motorisé', 'Voiture',
                             'Transports publics routiers', 'Train', 'Autres']
        else:
            raise Exception('Year of the MTMC not well defined! It should be 2010 or 2015.')
        column_name_for_mode = 'mode_simple'
    if agglo_def == 2000:
        folder_path_output = folder_path_output / 'agglo2000\\'
        if mrmt_year == 2015:
            name_of_the_agglomeration_variable = 'W_AGGLO2000'
        elif mrmt_year == 2010:
            name_of_the_agglomeration_variable = 'W_AGGLO'
        else:
            raise Exception('Year of the MTMC not well defined! It should be 2010 or 2015.')
    elif agglo_def == 2012:
        name_of_the_agglomeration_variable = 'W_AGGLO2012'
        folder_path_output = folder_path_output / 'agglo2012\\'
    else:
        raise Exception('Definition of agglomeration is not well defined! It can be only 2000 or 2012.')
    if percentage:
        columns = ['Agglomération', 'Echantillon']
    else:
        columns = ['Agglomération', 'Echantillon', 'Total', 'Total (+/-)']
    for mode_simple in list_of_modes:
        columns.extend([mode_simple, mode_simple + ' (+/-)'])
    df_for_csv = pd.DataFrame(columns=columns)
    df_zp = get_zp(year=mrmt_year, selected_columns=identification_columns + ['WP'])  # Get the full list of HHNR
    if mrmt_year == 2015:
        df_etappen = get_etappen(mrmt_year,
                                 selected_columns=identification_columns + ['E_Ausland', 'pseudo', 'rdist', 'f51300',
                                                                            'W_AGGLO_GROESSE2012'])
        df_hh = get_hh(year=mrmt_year, selected_columns=['HHNR', name_of_the_agglomeration_variable, 'W_BFS',
                                                         'W_AGGLO_GROESSE2012', 'W_AGGLO_GROESSE2000',
                                                         'W_staedt_char_2012'])
    elif mrmt_year == 2010:
        df_etappen = get_etappen(mrmt_year,
                                 selected_columns=identification_columns + ['E_Ausland', 'pseudo', 'rdist', 'f51300'])
        if agglo_def == 2000:
            df_hh = get_hh(year=mrmt_year, selected_columns=['HHNR', name_of_the_agglomeration_variable, 'W_BFS'])
        elif agglo_def == 2012:
            raise Exception('Not possible or by cheating')
        else:
            raise Exception('Year of the MTMC not well defined! It should be 2010 or 2015.')
    else:
        raise Exception('Year of the MTMC not well defined! It should be 2010 or 2015.')
    df_etappen = df_etappen[df_etappen.E_Ausland == 2]  # Remove trips abroad
    del df_etappen['E_Ausland']
    df_etappen = df_etappen[df_etappen.pseudo == 1]  # Remove pseudo trip legs
    del df_etappen['pseudo']
    if mrmt_year == 2015:
        df_etappen['mode_simple'] = df_etappen['f51300'].map(dict_detailed_mode2main_mode_2015)
    elif mrmt_year == 2010:
        df_etappen['mode_simple'] = df_etappen['f51300'].map(dict_detailed_mode2main_mode_2010)
    del df_etappen['f51300']
    if group_of_modes:
        if mrmt_year == 2015:
            df_etappen['group_of_modes'] = df_etappen['mode_simple'].map(dict_main_mode2group_of_modes_2015)
        elif mrmt_year == 2010:
            df_etappen['group_of_modes'] = df_etappen['mode_simple'].map(dict_main_mode2group_of_modes_2010)
        del df_etappen['mode_simple']
    # Get agglo classes (small, medium, large)
    if agglo_def == 2000:
        folder_path_input = Path('../data/input/' + str(mrmt_year) + '/')
        csv_file_name = 'Agglos_Klassen_' + str(mrmt_year) + '.csv'
        with open(folder_path_input / csv_file_name, 'r') as agglo_classes_file:
            df_agglo_classes = pd.read_csv(agglo_classes_file, sep=';')
            df_agglo_classes = df_agglo_classes[['Agglo_Klasse_ARE', 'Agglo00_No']]
    # Get the list of agglomerations
    list_of_agglomeration_numbers = df_hh[name_of_the_agglomeration_variable].unique()
    list_of_agglomeration_numbers = [x for x in list_of_agglomeration_numbers if (x != 0) & (x != -97)]
    ''' Add non-mobile HHNR/ZP '''
    df_etappen = pd.merge(df_etappen, df_zp[identification_columns],
                          left_on=identification_columns, right_on=identification_columns, how='right')
    df_etappen['rdist'].fillna(0, inplace=True)  # Replace NAN by 0
    df_etappen[column_name_for_mode].fillna('Autres', inplace=True)  # Replace NAN by 'Autres'
    ''' Add agglo info - including for non-mobiles '''
    if mrmt_year == 2015:
        del df_etappen['W_AGGLO_GROESSE2012']  # To avoid having two
    df_etappen = pd.merge(df_etappen, df_hh, left_on='HHNR', right_on='HHNR', how='left')
    if agglo_def == 2000:
        df_etappen = pd.merge(df_etappen, df_agglo_classes,
                              right_on='Agglo00_No', left_on=name_of_the_agglomeration_variable, how='left')
        # Test that all agglomerations have a class
        if len(df_etappen[(df_etappen['Agglo_Klasse_ARE'].isnull()) &
                          (df_etappen[name_of_the_agglomeration_variable] != 0)]) > 0:
            raise Exception('At least one agglomeration has no class (K, M or L)!')
    # Results for Switzerland
    dict_total_km, sample = compute_distances_and_confidence_interval_total(df_etappen, df_zp,
                                                                            identification_columns)
    dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_etappen, df_zp,
                                                                    percentage=percentage,
                                                                    identification_columns=identification_columns,
                                                                    group_of_modes=group_of_modes,
                                                                    list_of_modes=list_of_modes)
    dict_km_per_mode['Echantillon'] = sample
    dict_km_per_mode['Agglomération'] = 'Suisse'
    if percentage is False:
        dict_km_per_mode.update(dict_total_km)
    df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
    for agglo_nb in list_of_agglomeration_numbers:
        df_temp = df_etappen[df_etappen[name_of_the_agglomeration_variable] == agglo_nb]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp,
                                                                                identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        if agglo_def == 2012:
            if agglo_nb < 10000:
                dict_km_per_mode['Agglomération'] = 'Agglomération ' + dict_nb_agglo_bfs[agglo_nb]
            else:
                dict_km_per_mode['Agglomération'] = 'Centre hors des agglomération ' + \
                                                    dict_nb_centre_hors_agglo_bfs[agglo_nb]
        else:
            dict_km_per_mode['Agglomération'] = 'Agglomération ' + str(agglo_nb)
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
    if agglo_def == 2012:
        df_gemeinetyp = get_gemeindetyp()
        df_etappen = pd.merge(df_etappen, df_gemeinetyp, left_on='W_BFS', right_on='Gem_No', how='left')
        # For all agglomerations
        df_temp = df_etappen[df_etappen['W_AGGLO_GROESSE2012'] != 0]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = 'Toutes les agglomérations'
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        ''' Decompose population as in the MTMC report '''
        # More than 250'000 inhabitants
        df_temp = df_etappen[(df_etappen['W_AGGLO_GROESSE2012'] == 1) | (df_etappen['W_AGGLO_GROESSE2012'] == 2)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Agglomérations de 250'000 habitants et plus"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Between 50'000 and 249'999 inhabitants
        df_temp = df_etappen[(df_etappen['W_AGGLO_GROESSE2012'] == 3) | (df_etappen['W_AGGLO_GROESSE2012'] == 4)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "de 50'000 à 249'000 habitants"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Less than 50'000 inhabitants
        df_temp = df_etappen[(df_etappen['W_AGGLO_GROESSE2012'] == 5)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "de moins de 50'000 habitants"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        ''' Decompose pop as in report Agglo '''
        # More than 500'000 inhabitants
        df_temp = df_etappen[(df_etappen['W_AGGLO_GROESSE2012'] == 1)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Agglomérations de 500'000 habitants et plus"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Between 250'000 and 500'000 inhabitants
        df_temp = df_etappen[df_etappen['W_AGGLO_GROESSE2012'] == 2]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "de 250'000 à 499'999 habitants"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Between 100'000 and 249'999 inhabitants
        df_temp = df_etappen[df_etappen['W_AGGLO_GROESSE2012'] == 3]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "de 100'000 à 249'000 habitants"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Between 50'000 and 99'999 inhabitants
        df_temp = df_etappen[df_etappen['W_AGGLO_GROESSE2012'] == 4]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "de 50'000 à 99'000 habitants"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Less than 50'000 inhabitants
        df_temp = df_etappen[(df_etappen['W_AGGLO_GROESSE2012'] == 5)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "de moins de 50'000 habitants"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)

        # Outside of agglomerations
        df_temp = df_etappen[df_etappen['W_AGGLO_GROESSE2012'] == 0]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = 'Communes hors des agglomérations'
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        ''' Espace a caractere urbain '''
        # Rural communes
        df_temp = df_etappen[df_etappen['W_staedt_char_2012'] == 0]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = 'Communes rurales sans caractère urbain'
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Agglomerationskerngemeinde (Kernstadt)
        df_temp = df_etappen[df_etappen['W_staedt_char_2012'] == 1]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Communes-centres d'agglomération (villes-centres)"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Agglomerationskerngemeinde (Hauptkern)
        df_temp = df_etappen[df_etappen['W_staedt_char_2012'] == 2]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Communes-centres d'agglomération (centres principaux)"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Agglomerationskerngemeinde (Nebenkern)
        df_temp = df_etappen[df_etappen['W_staedt_char_2012'] == 3]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Communes-centres d'agglomération (centres secondaires)"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Agglomerationsgürtelgemeinde
        df_temp = df_etappen[df_etappen['W_staedt_char_2012'] == 4]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Communes de la couronne d'agglomération"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Mehrfach orientierte Gemeinde
        df_temp = df_etappen[df_etappen['W_staedt_char_2012'] == 5]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Communes multi-orientée"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Kerngemeinde ausserhalb Agglomerationen
        df_temp = df_etappen[df_etappen['W_staedt_char_2012'] == 6]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "Communes-centres hors agglomération"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        ''' Typologie 3 categories de l'espace à caractère urbain '''
        # Espace sous influence des centres urbains: couronnes + multi-orientées
        df_temp = df_etappen[(df_etappen['W_staedt_char_2012'] == 4) | (df_etappen['W_staedt_char_2012'] == 5)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "ECU: Espace sous influence des centres urbains"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Centres urbains: villes-centres d'agglo + communes-centres hors agglo
        df_temp = df_etappen[(df_etappen['W_staedt_char_2012'] == 1) | (df_etappen['W_staedt_char_2012'] == 2) |
                             (df_etappen['W_staedt_char_2012'] == 3) | (df_etappen['W_staedt_char_2012'] == 6)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "ECU: Espace des centres urbains"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        ''' Typologie des communes 2012 (9 types) '''
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 11]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune urbaine d'une grande agglomération"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 12]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune urbaine d'une agglomération moyenne"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 13]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune urbaine d'une petite ou hors agglomération"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 21]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune périurbaine de forte densité"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 22]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune périurbaine de moyenne densité"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 23]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune périurbaine de faible densité"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 31]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune d'un centre rural"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 32]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune rurale en situation centrale"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        #
        df_temp = df_etappen[df_etappen['TypBFS12_9_No'] == 33]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = "TC9: Commune rurale périphérique"
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
    elif agglo_def == 2000:
        # According to agglomeration size (definition ARE)
        list_of_agglomeration_sizes = ['K', 'M', 'G']
        # Per agglomeration size
        for agglo_size in list_of_agglomeration_sizes:
            df_temp = df_etappen[df_etappen['Agglo_Klasse_ARE'] == agglo_size]
            dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp,
                                                                                    identification_columns)
            dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                            percentage=percentage,
                                                                            identification_columns=identification_columns,
                                                                            group_of_modes=group_of_modes,
                                                                            list_of_modes=list_of_modes)
            dict_km_per_mode['Echantillon'] = sample
            dict_km_per_mode['Agglomération'] = 'Agglomération de taille ' + agglo_size
            if percentage is False:
                dict_km_per_mode.update(dict_total_km)
            df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # For all agglomerations
        df_temp = df_etappen[df_etappen['Agglo_Klasse_ARE'].isin(list_of_agglomeration_sizes)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = 'Toutes les agglomérations'
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Out of the agglomerations
        df_temp = df_etappen[df_etappen['Agglo_Klasse_ARE'].isnull()]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = 'Hors agglomérations'
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Villes isolées
        list_isolated_cities = [306, 329, 1301, 3851, 6136]
        for number_commune_BFS in list_isolated_cities:
            df_temp = df_etappen[df_etappen['W_BFS'] == number_commune_BFS]
            dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp,
                                                                                    identification_columns)
            dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                            percentage=percentage,
                                                                            identification_columns=identification_columns,
                                                                            group_of_modes=group_of_modes,
                                                                            list_of_modes=list_of_modes)
            dict_km_per_mode['Echantillon'] = sample
            dict_km_per_mode['Agglomération'] = 'Ville isolée (commune BFS) ' + str(number_commune_BFS)
            if percentage is False:
                dict_km_per_mode.update(dict_total_km)
            df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
        # Pour toutes les villes isolées
        df_temp = df_etappen[df_etappen['W_BFS'].isin(list_isolated_cities)]
        dict_total_km, sample = compute_distances_and_confidence_interval_total(df_temp, df_zp, identification_columns)
        dict_km_per_mode = compute_distances_and_conf_interval_per_mode(df_temp, df_zp,
                                                                        percentage=percentage,
                                                                        identification_columns=identification_columns,
                                                                        group_of_modes=group_of_modes,
                                                                        list_of_modes=list_of_modes)
        dict_km_per_mode['Echantillon'] = sample
        dict_km_per_mode['Agglomération'] = 'Toutes les ville isolées'
        if percentage is False:
            dict_km_per_mode.update(dict_total_km)
        df_for_csv = df_for_csv.append(dict_km_per_mode, ignore_index=True)
    for mode_simple in list_of_modes:
        df_for_csv[mode_simple].fillna(0, inplace=True)
        df_for_csv[mode_simple + ' (+/-)'].fillna('-', inplace=True)

    # File names
    if group_of_modes:
        if percentage:
            new_file_name = 'Parts_modes_de_transport_pourcentage_' + str(mrmt_year) + '_' + str(agglo_def) + '.csv'
        else:
            new_file_name = 'Parts_modes_de_transport_' + str(mrmt_year) + '_' + str(agglo_def) + '.csv'
    else:
        if percentage:
            new_file_name = 'Parts_moyen_de_transport_pourcentage_' + str(mrmt_year) + '_' + str(agglo_def) + '.csv'
        else:
            new_file_name = 'Parts_moyen_de_transport_' + str(mrmt_year) + '_' + str(agglo_def) + '.csv'
    # Save in folder output
    df_for_csv.to_csv(folder_path_output / new_file_name, index=False, sep=',', encoding='iso-8859-1')


def get_gemeindetyp():
    path_to_file = Path('../data/input/2015/GdeTypo12_9_2017_2_2015.csv')
    with open(path_to_file, 'r') as csv_file:
        df_gemeindetyp = pd.read_csv(csv_file, sep=';', usecols=['Gem_No', 'TypBFS12_9_No'])
    return df_gemeindetyp
