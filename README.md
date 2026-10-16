# Final Project

## Emotion Detection with Watson NLP

Author: Dinh Minh

This Flask application submits text to the IBM Watson NLP emotion service and
returns scores for anger, disgust, fear, joy, sadness, and the dominant emotion.
It handles blank input and upstream HTTP 400 responses as invalid text, and
reports service connection errors without inventing predictions.

### Installation and execution

```bash
python3 -m pip install -r requirements.txt
python3 server.py
```

Open port 5000 in the IBM Skills Network lab or visit http://localhost:5000.

### Live Watson verification (requires the Skills Network service)

```bash
python3 -c "from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector('I am very angry'))"
python3 test_emotion_detection.py
```

### Local checks

```bash
python3 -m unittest discover -s tests -v
python3 -m pylint server.py
```

The tests in `tests/` use explicitly mocked HTTP responses to verify parsing and
error handling. They are separate from the five live Watson tests in
`test_emotion_detection.py` and are not evidence of successful Watson prediction.

### Verification status (2026-10-16)

Watson's service hostname resolves to private network addresses from this machine,
and connection attempts time out. Successful prediction output, five live test
passes, and a successful deployment screenshot must be captured in a reachable
Skills Network lab. No simulated prediction output is included as submission
evidence. The source retains the original IBM repository history.
