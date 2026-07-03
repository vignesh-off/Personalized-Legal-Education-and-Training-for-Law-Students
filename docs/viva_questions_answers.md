# Viva Questions and Answers

## Machine Learning & Preprocessing (Q1-Q8)
**Q1: Why did you choose Random Forest for predicting student mastery?**
**A:** Random Forest handles tabular data well, naturally captures non-linear relationships (like the tradeoff between score and attempts), prevents overfitting via ensemble bagging, and requires minimal hyperparameter tuning for a robust baseline.

**Q2: What features did you use to train the ML model?**
**A:** The model uses four primary features: Assessment Score (0-100), Time Spent (minutes), Number of Attempts, and Module Difficulty Level (1-5).

**Q3: Why is preprocessing necessary, and how did you scale your features?**
**A:** Features like score (0-100) and attempts (1-10) are on vastly different scales, which can skew distance-based or gradient-based algorithms (though RF is somewhat immune, scaling is best practice). We used `StandardScaler` to transform features to have zero mean and unit variance.

**Q4: How did you generate the dataset for your model?**
**A:** We created a synthetic dataset using `numpy.random` to generate feature values and formulated a heuristic mathematical rule (Score - 2*Attempts + 5*Difficulty) to assign logical ground-truth labels (Beginner, Intermediate, Expert) for training.

**Q5: How do you evaluate the Random Forest model's performance?**
**A:** We split the data into training (80%) and testing (20%) sets and evaluate it using a Classification Report, which outputs Precision, Recall, F1-Score, and overall Accuracy.

**Q6: What is a Random Forest?**
**A:** It is an ensemble learning method that constructs a multitude of decision trees during training and outputs the mode of the classes for classification tasks, reducing the variance of individual trees.

**Q7: How did you save the trained ML model for the backend API?**
**A:** We serialized the trained model and the fitted scaler using the `joblib` library, saving them as `model.joblib` and `scaler.joblib` to be loaded into memory at server startup.

**Q8: Can the model predict risk level directly?**
**A:** No, the ML model predicts mastery. Risk level is calculated separately using a rule-based logic tier that evaluates the raw score, attempts, and difficulty thresholds, creating a hybrid AI logic pipeline.

## Deep Learning (DL) Fallback (Q9-Q12)
**Q9: What is the purpose of the DL module in your project?**
**A:** It acts as a secondary, comparative prediction engine to verify the ML output. It represents a neural-network-based approach returning both a classification and a confidence score.

**Q10: Why did you simulate the DL module instead of training PyTorch/TensorFlow?**
**A:** To keep the project lightweight, strictly offline, and demo-ready without requiring heavy GPU frameworks or long training times, while still demonstrating the architectural capability of a hybrid ensemble.

**Q11: How is the DL confidence score generated?**
**A:** It assigns a base confidence based on the score tier and applies penalty modifiers if the student took excessive attempts or if the difficulty level was unusually high, simulating confidence degradation.

**Q12: How does the frontend handle conflicting ML and DL predictions?**
**A:** The frontend includes logic to compare both outputs. If they agree, it displays a high-confidence consensus. If they differ, it issues a "Needs Review" warning and defaults to a conservative recommendation.

## Natural Language Processing (NLP) (Q13-Q17)
**Q13: How does the NLP module evaluate legal essays?**
**A:** It utilizes keyword extraction and concept detection by matching the student's text against a dictionary of vital legal terms for the specific topic (e.g., "mens rea" for Criminal Law).

**Q14: How is the essay score calculated?**
**A:** The score is calculated proportionally based on the number of expected keywords successfully detected in the essay, padded with a base score, and capped at 100.

**Q15: What happens if an essay is too short?**
**A:** The NLP module checks the string length. If it is less than 10 characters, it instantly scores a 0 and returns feedback stating the text is too short to evaluate.

**Q16: How does the NLP module generate feedback?**
**A:** It performs missing concept analysis. If concepts are missed, it dynamically populates the feedback string indicating which found concepts were correct and urging the student to review the missing definitions.

**Q17: What are the limitations of your current NLP approach?**
**A:** It is a rule-based exact-matching system. It doesn't understand context, semantics, or synonyms (e.g., "breaking a contract" vs. "breach"). A transformer model like BERT would be required for true semantic understanding.

## Small Language Model (SLM) Tutor (Q18-Q21)
**Q18: What is the function of the SLM module?**
**A:** It acts as an instant AI Legal Tutor, allowing students to ask conceptual legal questions and receive immediate definitions.

**Q19: How is the SLM implemented in this offline demo?**
**A:** It is implemented as a lightweight, dictionary/template-based simulation. It parses the incoming query for known keywords and returns pre-written conceptual definitions.

**Q20: Why use an SLM over a large model like GPT-4 here?**
**A:** SLMs are highly efficient, can run offline, ensure data privacy, and have near-zero latency, which is ideal for a localized, self-contained educational platform.

**Q21: How would you upgrade the SLM in the future?**
**A:** By integrating a quantized, locally hosted model (like Llama 3 8B or Mistral) using Ollama, which would allow for true generative conversation while remaining offline.

## Generative AI (GenAI) Scenarios (Q22-Q25)
**Q22: What role does GenAI play in this platform?**
**A:** It dynamically generates personalized, topic-specific legal scenarios and probing questions to help students practice concepts they are struggling with.

**Q23: How does the system know which scenario to generate?**
**A:** It reads the student's predicted "weak_topic" (or current topic) from the ML module and maps it to the scenario generator.

**Q24: Is the current GenAI module creating text from scratch?**
**A:** No, to ensure the demo is offline and API-key free, it uses a simulated template engine that returns complex pre-authored scenarios based on the topic.

**Q25: How would you implement real GenAI?**
**A:** By connecting the backend to the OpenAI API or Google Gemini API, passing a prompt like "Generate a complex tort law scenario regarding negligence," and streaming the response to the user.

## Agentic AI Intervention (Q26-Q29)
**Q26: What is an Agentic AI in the context of your platform?**
**A:** It is an autonomous background system that proactively audits a student's profile, detects high risk, and takes (or recommends) pedagogical action without explicit user prompting.

**Q27: What actions does your agent take?**
**A:** It flags the struggling student, recommends an action (like assigning a GenAI scenario), and automatically drafts a personalized intervention email for the professor.

**Q28: How is this different from a standard function?**
**A:** Standard functions react to explicit user clicks. Agents simulate autonomous monitoring and proactive decision-making based on continuous state evaluation.

**Q29: Who has access to trigger or view the Agentic Audit?**
**A:** Only Administrators and Teachers can view the agentic alerts, as it pertains to student intervention and monitoring.

## Backend (FastAPI) & Database (SQLite) (Q30-Q35)
**Q30: Why use FastAPI for the backend instead of Flask or Django?**
**A:** FastAPI is asynchronous, incredibly fast, provides automatic OpenAPI/Swagger documentation, and natively uses Pydantic for strict data validation, making API development robust.

**Q31: What is Pydantic and how is it used?**
**A:** Pydantic is a data validation library. We use it to define `schemas.py`, ensuring incoming JSON payloads have the exact data types (e.g., score must be a float, attempts an int) before processing.

**Q32: How is data persisted in your application?**
**A:** We use SQLite, a lightweight, file-based relational database. The `app/database.py` file initializes `students.db` and handles SQL `INSERT` commands.

**Q33: What happens to the database when the server restarts?**
**A:** SQLite stores data in a persistent local file (`students.db`), so historical predictions and analytics remain available across server restarts.

**Q34: How did you solve the NumPy data type issue with SQLite?**
**A:** Scikit-learn predictions return NumPy arrays containing NumPy strings. SQLite expects native Python strings. We cast the output using `str(prediction[0])` before DB insertion to prevent typing crashes.

**Q35: What is the lifespan context manager in FastAPI used for here?**
**A:** It ensures that the database is initialized (`init_db()`) and the ML models (`joblib.load`) are loaded into memory exactly once when the server starts up, before accepting any requests.

## Frontend (Streamlit) & RBAC (Q36-Q40)
**Q36: Why Streamlit for the frontend?**
**A:** Streamlit allows for rapid development of data-centric web applications entirely in Python. It integrates seamlessly with Pandas and Plotly for real-time analytics dashboards.

**Q37: How did you implement Role-Based Access Control (RBAC)?**
**A:** We use Streamlit's `st.session_state` to store the logged-in user's role (Student, Teacher, Admin). Conditional `if/else` logic renders different tabs and data based on that role.

**Q38: Why is the Student role restricted in the Analytics dashboard?**
**A:** For privacy. The Student role automatically passes their `student_id` to the data filter, preventing them from viewing the cohort-wide data that Teachers and Admins can see.

**Q39: How are the analytics visualized?**
**A:** We use Plotly Express to generate interactive donut charts (for Risk Distribution), bar charts (for Mastery Attainment), and line charts with moving averages (for Longitudinal Score Trends).

**Q40: How does the frontend handle API failures or timeouts?**
**A:** It uses `try-except` blocks with defined `timeout` parameters. If the FastAPI backend is down or the DL model times out, the frontend catches the error and executes a local fallback heuristic so the UI doesn't crash.
