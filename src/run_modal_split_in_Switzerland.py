from residency_principle import run_residency_principle_by_agglomeration, run_residency_principle_by_commune_numbers, \
    run_proportion_of_distances_in_agglomerations, get_modalsplit_in_agglomerations_2005_2015, get_modalsplit_in_agglomerations_2015_2021


def run_modal_split_in_switzerland():
    """ This function computes:
     - the results presented in chapter 2 of the report "Modal shares in agglomerations" (ARE,
    2018). It presents only results computed with the residency principle (where people live) and not with the
    territoriality principle (where people travel);
     - the modal share for any group of Swiss communes, defined below.
    :return: Nothing. The function generates several CSV files in data/output. The files are ordered by year, then by
     spatial decomposition (agglomeration with definition 2000, agglomeration with definition 2012, or list of communes)
    """
    run_residency_principle_by_agglomeration()
    # Compute the modal split for a list of BFS/OFS/FSO commune numbers;
    # Here the example of the agglomeration of Zurich:
    list_of_commune_numbers = [261, 52, 54, 62, 66, 69, 131, 133, 135, 136, 137, 139, 141, 151, 152, 154, 160, 161, 191,
                               194, 197, 199, 200, 243, 244, 245, 246, 247, 249, 250, 251, 4023, 2, 5, 51, 53, 56, 57,
                               60, 68, 72, 89, 90, 92, 96, 121, 138, 142, 155, 156, 158, 159, 174, 198, 1322, 1323,
                               4030, 4040, 4048, 4062, 4063, 4075, 4081, 4083, 1, 3, 4, 8, 9, 10, 11, 12, 13, 14, 23,
                               55, 58, 59, 61, 63, 64, 65, 67, 70, 71, 81, 82, 83, 84, 85, 86, 87, 88, 91, 93, 94, 95,
                               97, 98, 99, 100, 101, 102, 111, 112, 115, 116, 117, 119, 132, 134, 140, 153, 157, 172,
                               173, 175, 176, 177, 178, 180, 182, 192, 193, 195, 196, 213, 215, 224, 241, 242, 248,
                               1321, 2933, 2938, 4022, 4031, 4061, 4066, 4067, 4071, 4073, 4074, 4079, 4084, 4226, 4238,
                               4306, 4308, 4318, 4319]
    run_residency_principle_by_commune_numbers(list_of_commune_numbers, year=2010)
    run_residency_principle_by_commune_numbers(list_of_commune_numbers, year=2015)
    # Computes the proportion of distances and population in and out of agglomerations
    run_proportion_of_distances_in_agglomerations()
    # Computes the modal shares 2005, 2010 and 2015 for people living in agglomerations (definition 2000)
    get_modalsplit_in_agglomerations_2005_2015(percentage=True)
    # Computes the modal shares 2015 and 2021 for people living in agglomerations (definition 2012)
    get_modalsplit_in_agglomerations_2015_2021(percentage=True)


if __name__ == '__main__':
    run_modal_split_in_switzerland()
