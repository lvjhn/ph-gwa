from core.text.agmv import AGMV 
import pandas as pd

agmv = AGMV(
    model_name ="glove-twitter-25",
    dims = 25,
    averaging = "sentence",
    use_mock = True,
    no_stopwords = True
)

sentences = pd.Series([
    "It must be five o'clock somewhere. "
    "When he had to picnic on the beach, he purposely put sand in other people's food. "
    "That is an appealing treasure map that I can't read.",
    # --- #
    "He had a hidden stash underneath the floorboards in the back room of the house. "
    "The lyrics of the song sounded like fingernails on a chalkboard. "
    "You're good at English when you know the difference between a man eating chicken and a man-eating chicken.",
    # --- #
    "The reservoir water level continued to lower while we enjoyed our long shower. "
    "The most exciting eureka moment I've had was when I realized that the instructions on food packets were just guidelines. "
    "I'd rather be a bird than a fish.",
     "It must be five o'clock somewhere. "
    "When he had to picnic on the beach, he purposely put sand in other people's food. "
    "That is an appealing treasure map that I can't read.",
    # --- #
    "He had a hidden stash underneath the floorboards in the back room of the house. "
    "The lyrics of the song sounded like fingernails on a chalkboard. "
    "You're good at English when you know the difference between a man eating chicken and a man-eating chicken.",
    # --- #
    "The reservoir water level continued to lower while we enjoyed our long shower. "
    "The most exciting eureka moment I've had was when I realized that the instructions on food packets were just guidelines. "
    "I'd rather be a bird than a fish.",
     "It must be five o'clock somewhere. "
    "When he had to picnic on the beach, he purposely put sand in other people's food. "
    "That is an appealing treasure map that I can't read.",
    # --- #
    "He had a hidden stash underneath the floorboards in the back room of the house. "
    "The lyrics of the song sounded like fingernails on a chalkboard. "
    "You're good at English when you know the difference between a man eating chicken and a man-eating chicken.",
    # --- #
    "The reservoir water level continued to lower while we enjoyed our long shower. "
    "The most exciting eureka moment I've had was when I realized that the instructions on food packets were just guidelines. "
    "I'd rather be a bird than a fish.",
     "It must be five o'clock somewhere. "
    "When he had to picnic on the beach, he purposely put sand in other people's food. "
    "That is an appealing treasure map that I can't read.",
    # --- #
    "He had a hidden stash underneath the floorboards in the back room of the house. "
    "The lyrics of the song sounded like fingernails on a chalkboard. "
    "You're good at English when you know the difference between a man eating chicken and a man-eating chicken.",
    # --- #
    "The reservoir water level continued to lower while we enjoyed our long shower. "
    "The most exciting eureka moment I've had was when I realized that the instructions on food packets were just guidelines. "
    "I'd rather be a bird than a fish.",
    "It must be five o'clock somewhere. "
    "When he had to picnic on the beach, he purposely put sand in other people's food. "
    "That is an appealing treasure map that I can't read.",
    # --- #
    "He had a hidden stash underneath the floorboards in the back room of the house. "
    "The lyrics of the song sounded like fingernails on a chalkboard. "
    "You're good at English when you know the difference between a man eating chicken and a man-eating chicken.",
    # --- #
    "The reservoir water level continued to lower while we enjoyed our long shower. "
    "The most exciting eureka moment I've had was when I realized that the instructions on food packets were just guidelines. "
    "I'd rather be a bird than a fish.",
     
])

vectors = agmv.transform(sentences)

print(vectors.shape)