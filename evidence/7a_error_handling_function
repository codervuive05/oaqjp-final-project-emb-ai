"""Predict emotion scores using the IBM Watson NLP service."""

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


def emotion_detector(text_to_analyze):
    """Return five emotion scores and their maximum, or None for HTTP 400."""
    response = requests.post(
        URL, json={"raw_document": {"text": text_to_analyze}},
        headers=HEADERS, timeout=30
    )
    if response.status_code == 400:
        return dict.fromkeys(
            ("anger", "disgust", "fear", "joy", "sadness", "dominant_emotion")
        )
    response.raise_for_status()
    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {name: scores[name] for name in
              ("anger", "disgust", "fear", "joy", "sadness")}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
