# Modal shares in Switzerland
This code computes the modal shares in Switzerland:
- in general for the whole Switzerland and for subcategories of Switzerland (by agglomeration, by categories of agglomerations, in and out of agglomerations)
     - <a href="https://github.com/antonindanalet/modal-split-in-Switzerland/tree/master/data/output/2015/agglo2012">for 2015 with a definition of agglomerations of 2012</a>,
     - <a href="https://github.com/antonindanalet/modal-split-in-Switzerland/tree/master/data/output/2015/agglo2000">for 2015 with a definition of agglomerations of 2000</a>,
     - <a href="https://github.com/antonindanalet/modal-split-in-Switzerland/tree/master/data/output/2010/agglo2000">for 2010 with a definition of agglomerations of 2000</a>.
- by a user defined list of communes, with the example of the agglomeration of Zurich here, for <a href="https://github.com/antonindanalet/modal-split-in-Switzerland/tree/master/data/output/2010/bfs_numbers">2010</a> and 2015.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for reproducing the result and understanding how it has been generated.

### Prerequisites
To run the code itself, you need python 3, and pandas.

For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this form in <a href="https://www.are.admin.ch/are/de/home/verkehr-und-infrastruktur/grundlagen-und-daten/mzmv/datenzugang.html">German</a>, <a href="https://www.are.admin.ch/are/fr/home/transports-et-infrastructures/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/trasporti-e-infrastrutture/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code
Please copy the files etappen.csv, haushalte.csv and zielpersonen.csv of 2010 and 2015 that you receive from the Federal Statistical Office in the folders <a href="https://github.com/antonindanalet/modal-split-in-Switzerland/tree/master/data/input/2010/mtmc10">data/input/2010/mtmc10</a> and <a href="https://github.com/antonindanalet/modal-split-in-Switzerland/tree/master/data/input/2015/mtmc15">data/input/2015/mtmc15</a>. Then run <a href="https://github.com/antonindanalet/modal-split-in-Switzerland/blob/master/src/run_modal_split_in_Switzerland.py">run_modal_split_in_Switzerland.py</a>.

DO NOT commit or share in any way the CSV-files etappen.csv, haushalte.csv or zielpersonen.csv! These are personal data.

### Contact
Please don't hesitate to contact me if you have questions or comments about this code: antonin.danalet@are.admin.ch
