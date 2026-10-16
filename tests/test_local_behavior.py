"""Local contract tests with explicit HTTP fixtures; not live Watson evidence."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import emotion_detector
from server import app


class LocalBehaviorTests(unittest.TestCase):
    """Check parsing, request shape, and user-visible error handling."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_scores_and_dominant_emotion(self, post):
        """Parse the real service response shape without mutating its scores."""
        scores = dict(anger=0.8, disgust=0.04, fear=0.05, joy=0.01, sadness=0.1)
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }
        result = emotion_detector("I am angry")
        self.assertEqual(result, {**scores, "dominant_emotion": "anger"})
        self.assertEqual(post.call_args.kwargs["json"], {
            "raw_document": {"text": "I am angry"}
        })

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_none(self, post):
        """A rejected input must have six None values."""
        post.return_value = Mock(status_code=400)
        result = emotion_detector("")
        self.assertEqual(len(result), 6)
        self.assertTrue(all(value is None for value in result.values()))

    def test_blank_input_never_calls_watson(self):
        """Whitespace produces a useful error without a remote request."""
        with patch("server.emotion_detector") as detector:
            response = app.test_client().get("/emotionDetector?textToAnalyze=%20")
        detector.assert_not_called()
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")

    @patch("server.emotion_detector", side_effect=requests.Timeout("unavailable"))
    def test_unavailable_service_is_not_a_prediction(self, _detector):
        """Remote failure is HTTP 503, never a fabricated emotion."""
        response = app.test_client().get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.status_code, 503)
        self.assertIn("unavailable", response.get_data(as_text=True))

    @patch("server.emotion_detector", return_value={"dominant_emotion": None})
    def test_rejected_input_message(self, _detector):
        """The server translates the HTTP 400 result to the expected message."""
        response = app.test_client().get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")

    def test_home_page(self):
        """The actual Flask template is available."""
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("NLP - Emotion Detection", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
