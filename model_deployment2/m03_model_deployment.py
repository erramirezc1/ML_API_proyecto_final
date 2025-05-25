import pandas as pd
import joblib
import sys
import os

def predict_probabilidad(plot):
    """
    Predice la probabilidad de popularidad de una canción basada en sus características.

    Args:
        plot (str): Descripción o letra de la canción.

    Returns:
        dict: Diccionario con las probabilidades por género.
    """
    # Cargar el modelo, vectorizador, escalador y columnas
    try:
        clf_tfidf = joblib.load(os.path.join(os.path.dirname(__file__), 'model.pkl'))
        tfidf_vect = joblib.load(os.path.join(os.path.dirname(__file__), 'vectorizer.pkl'))
        cols = joblib.load(os.path.join(os.path.dirname(__file__), 'cols.pkl'))
    except Exception as e:
        print(f"Error al cargar los artefactos: {e}")
        return None

    try:
        plot = str(plot)
    except Exception:
        print("Advertencia: plot no es un string válido.")
        return None

    try:
        # Transformar el texto usando el vectorizador ya entrenado
        input_vect = tfidf_vect.transform([plot])

        # Realizar la predicción de probabilidades de género
        prediccion_genero = clf_tfidf.predict_proba(input_vect)

        # Crear un diccionario con las probabilidades por género
        probabilidades = {col: float(prob) for col, prob in zip(cols, prediccion_genero[0])}

    except Exception as e:
        print(f"Error al predecir la probabilidad: {e}")
        return None

    return probabilidades
