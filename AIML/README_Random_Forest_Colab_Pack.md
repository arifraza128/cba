# Random Forest Fruit and Vehicle Classification — Colab Pack

## Files included
- `Random_Forest_Fruit_and_Vehicle_Classification.ipynb` — complete notebook for both classification tasks.
- `dataset_1_fruit_image_features.csv` — 2,400-row fruit feature dataset.
- `dataset_2_vehicle_image_features.csv` — 2,400-row vehicle feature dataset.

## Run in Google Colab
1. Download and unzip this pack on your computer.
2. Open `Random_Forest_Fruit_and_Vehicle_Classification.ipynb` in Google Colab (`File > Upload notebook`).
3. Run the notebook cells from top to bottom.
4. When the upload prompt appears, select both CSV files from the unzipped folder.
5. At the end, download `random_forest_classification_outputs.zip`. It contains the two trained model bundles and the metrics CSV.

## Important notes
- The `image_id` column is excluded from training; `label` is the prediction target.
- The notebook uses an 80/20 stratified split, 5-fold Stratified Cross-Validation, RandomizedSearchCV, class-wise evaluation, confusion matrices, feature importances, and joblib model export.
- The supplied data are synthetic tabular image features, not raw images. The notebook predicts from numeric feature rows and does not directly classify image files.
- Accuracy of 100% is not guaranteed on unseen or real-world camera images. Do not use the test set for training or hyperparameter tuning.
