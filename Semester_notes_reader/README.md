**Unit 1: Overview of Data Mining & Predictive Analytics**

---

### 1. Exam‑Focused Explanation of Key Concepts

**Data Mining** is the process of discovering meaningful patterns, trends, and relationships in large datasets using statistical, machine learning, and visualization techniques.

* **Predictive Analytics** leverages models built on historical data to forecast future events or behaviors.
* The two phases: **Descriptive** (what happened?) and **Predictive** (what will happen?).

**Scope & Boundaries**

* Applicable in domains with structured or semi‑structured data: finance, healthcare, marketing, retail, manufacturing.
* **Not** suitable when:

  * Data volumes are tiny (insufficient statistical power).
  * Data quality is extremely poor (unreliable signals).
  * Real‑time low‑latency requirements exceed batch or near‑line mining capabilities.

**Data Science as an Emerging Interdisciplinary Field**

* Integrates: Computer Science (algorithms), Statistics (inference), Domain Expertise (context), Data Engineering (ETL), and Visualization.
* Bridges the gap between raw data and actionable insights.

**Pitfalls in Mining "Big Data"**

* **"Big bad data"**: large volumes of noisy, redundant, or irrelevant data.
* **Local sparsity**: high dimensionality causes data to be sparse in feature space; distances become less informative.
* **"Big isn't always enough"**: more data can worsen noise, amplify bias, and increase computation cost without adding signal.

**Career Opportunities & UNHMS Analytics Program**

* Roles: Data Analyst, Data Scientist, Machine Learning Engineer, Business Intelligence Specialist, Analytics Consultant.
* UNHMS Analytics: a flagship master’s program offering training in advanced analytics, machine learning, and data management (see \[university website] for details).

---

### 2. Important Definitions & Diagrams

* **Data Mining**: “The nontrivial process of identifying valid, novel, potentially useful, and understandable patterns in data.”
* **Predictive Model**: a function f(X) → Y that estimates outcomes Y from inputs X.

**Conceptual Diagram: Data Mining Workflow**

```
Raw Data → Data Cleaning → Feature Engineering → Model Building → Evaluation → Deployment → Monitoring
```

*Caption:* High‑level pipeline of a typical predictive analytics project.

---

### 3. Real‑World Examples & Pitfalls

* **Retail Market‑Basket Analysis**: Discover which products co‑occur at checkout (e.g., bread & butter). Pitfall: ignoring seasonal effects can lead to spurious associations.
* **Credit Scoring**: Use historical borrower data to predict default risk. Pitfall: biased training data can embed discriminatory practices.

---

### 4. "Must‑Remember" Revision Notes

* Data Mining = Discovery + Predictive Analytics = Forecasting.
* {•} Scope: finance, healthcare, marketing; {•} Not: tiny/noisy data, real‑time streaming.
* Interdisciplinary: CS + Stats + Domain + Engineering + Viz.
* Pitfall buzzwords: "big bad data", local sparsity, noise vs. signal.
* Careers: Analyst → Data Scientist → ML Engineer; UNHMS offers advanced certification.

---

### 5. Theory Questions & Model Answers

1. **Define data mining and differentiate it from predictive analytics.**
   *Answer:* Data mining is the extraction of patterns and knowledge from large datasets; predictive analytics uses these patterns to build models that forecast future outcomes.

2. **List three domains where data mining is most applicable and two scenarios where it is not.**
   *Answer:* Applicable in finance, healthcare, marketing; not in extremely small datasets or low‑latency streaming without suitable infrastructure.

3. **Explain the interdisciplinary nature of data science.**
   *Answer:* It combines computer science (algorithms), statistics (inference), domain expertise, data engineering (ETL), and visualization to turn data into insights.

4. **What is "big bad data" and why is it problematic?**
   *Answer:* Large volumes of poor‑quality data that obscure true signals, leading to inaccurate models.

5. **Describe local sparsity and its effect on distance‑based methods.**
   *Answer:* In high‑dimensional spaces, data points become sparse, making Euclidean distances less meaningful and degrading k‑NN performance.

6. **Why might "bigger" datasets sometimes degrade model performance? Give two reasons.**
   *Answer:* More noise and redundancy amplify overfitting and bias; increases computation cost without adding new information.

7. **Outline five career paths in data mining.**
   *Answer:* Data Analyst, Data Scientist, BI Specialist, ML Engineer, Analytics Consultant.

8. **Sketch and describe the main stages in a predictive analytics workflow.**
   *Answer:* See pipeline diagram: data cleaning → feature engineering → model building → evaluation → deployment → monitoring.

9. **What are the key benefits of pursuing the UNHMS Analytics program?**
   *Answer:* Advanced coursework in ML, access to industry projects, mentorship, and placement support.

10. **Give an example of a real‑world data mining project and highlight one pitfall.**
    *Answer:* Market‑basket analysis in retail; pitfall is seasonal confounding if holiday spikes are mistaken for permanent associations.

---

*Please review and when you’re ready, say* **"Next topic"** *to move on to Unit 2.*
