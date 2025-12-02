Dear Professor Kim and Jackie,

This file contains all the Jupyter, Python and csv files used for this project. Feel free to check every file, although some of them are a bit outdated and are not extremely relevant to the final results. Here is a quick summary of our files:

## Datasets folder

- `mlb_game_data_2025.csv` Contains all the post-game data from every game in the 2025 season.
- `mlb_game_data_2025v2.csv` Contains the same info as the previous file, but duplicates were removed.
- `mlb_game_data_2025v2_with_rolling40.csv` Contains the data of implementing rolling average throughout the season.
- `mlb_game_data_2025v2_with_rolling40_filtered.csv` Same as the previous file, but we filtered the first games of the season since they were not used to train our data.
- `mlb_playoff_games_2025.csv` Dataset containing all the playoff games, but without applying the rolling average.
- `mlb_team_averages_2025.csv` Average of the stats for each team home and away throughout the whole season, which we originally used to populate the post-season features.
- `mlb_vqc_features.csv` It contains the processed data that we used to train all our models.
- `postseason_test_data.csv` Dataset of the playoff games after we applied the rolling average.
- `postseason_test_processed.csv` processed data from the previous file, used to test our trained classifiers.

## Results folder

The MLPC/QSVM/SVM/VQC_Results folders contain the predictions for each one of the 47 playoff games for every single trained classifier in different .csv files. For example in the VQC_Results folder, you will find 48 csv files corresponding to the 48 trained VQCs.

Here are other relevant files you might want to check:

### mlpc/qsvm/svm/vqc_final

By running every cell in these files, you will begin training all the different classifiers, and storing their predictions in csv files.

### vqc_table

By running every cell in this file, you will generate a DataFrame that will show the accuracy % of each one of the 48 VQCs, sorted from most accurate to least.

### rolling_average

By running every cell in this file, you will generate the `mlb_game_data_2025v2_with_rolling40.csv` dataset.

## Other files

The rest of the files were used to either 

1. Learn how to extract data from the MLB API and pick the right features 
2. Learn about the different classifier models we used for this project.

We hope you enjoyed our project, it was very fun and challenging!

Thanks for a wonderful term,
Danesh and Jonathan


Github link: https://github.com/DaneshMorales/QML_project
