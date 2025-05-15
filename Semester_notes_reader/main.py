import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Optional: adjust speaking rate and voice
engine.setProperty('rate', 160)  # Speed in words per minute
engine.setProperty('volume', 1.0)  # Volume: 0.0 to 1.0

# You can also change voice here (male/female) if needed
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Try voices[0] or voices[1]

# Paste your entire Unit 1 text here as a string
text = """
Unit 1: Overview of Data Mining & Predictive Analytics.

Data Mining is the process of discovering meaningful patterns, trends, and relationships in large datasets 
using statistical, machine learning, and visualization techniques.

Predictive Analytics uses models built on historical data to forecast future events.

Two main types: Descriptive (what happened?) and Predictive (what will happen?).

Scope: used in finance, healthcare, marketing, manufacturing.
Not suitable when data is too small, low quality, or needs real-time decisions.

Data Science is an interdisciplinary field combining:
Computer Science, Statistics, Domain Knowledge, Data Engineering, and Visualization.

Pitfalls in Big Data:
Big Bad Data – noisy, redundant, low-quality data.
Local Sparsity – in high-dimensional space, data is spread out and distance metrics become unreliable.
Big Isn’t Always Better – more data may just mean more noise.

Careers: Data Analyst, Data Scientist, Machine Learning Engineer, BI Specialist, Analytics Consultant.

UNHMS Analytics Program offers advanced machine learning and analytics courses.

Important terms:
Data Mining – discovering useful patterns in data.
Predictive Model – function that maps inputs to outputs, like f(X) → Y.

Example projects:
- Market-Basket Analysis: What items are often bought together.
- Credit Scoring: Predict loan default.

Pitfalls: Ignoring seasonality, biased data, noisy signals.

Remember:
- Data Mining = pattern discovery.
- Predictive Analytics = forecasting future.
- Watch out for: bad data, sparsity, and bias.
"""

# Read aloud
engine.say(text)
engine.runAndWait()
