async function RunSentimentAnalysis() {
  const input = document.getElementById("textToAnalyze").value;
  const output = document.getElementById("system_response");
  output.textContent = "Analyzing...";
  try {
    const response = await fetch(
      "/emotionDetector?textToAnalyze=" + encodeURIComponent(input)
    );
    output.textContent = await response.text();
  } catch (error) {
    output.textContent = "Unable to connect. Please try again.";
  }
}
