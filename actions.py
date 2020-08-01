from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
indices, count_matrix = pickle.load( open( "save2.p", "rb" ) )
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
def get_recommendations(idx, cosine_sim):
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    movie_indices = [ i[0] for i in sim_scores]
    name =[]
    for i in movie_indices:
        name.append([key  for (key, value) in indices.items() if value == i])
    return name


class ActionGiveSimilarMovie(Action):

    def name(self) -> Text:
        return "action_give_similar_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        movie = tracker.get_slot("movie")
        print(movie)
        idx = indices[movie]
        if(idx):
            l = get_recommendations(idx, cosine_sim2)
        else:
            l=None

        if l is None:
            output = "Could not find a movie"
        else:
            output = f'You can watch {l[0][0]} OR {l[1][0]}'
        dispatcher.utter_message(text=output)

        return []
