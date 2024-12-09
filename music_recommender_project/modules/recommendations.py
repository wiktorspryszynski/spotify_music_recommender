import joblib
import pandas

merged_df = joblib.load('music_recommender_project\modules\merged_dataset.pkl')
model = joblib.load('music_recommender_project\modules\music_recommender_model.pkl')

