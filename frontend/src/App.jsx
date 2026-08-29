import { useState } from "react";

function App() {
const [screen, setScreen] = useState("home");
const [questionIndex, setQuestionIndex] = useState(0);
const [answer, setAnswer] = useState("");
const [submitted, setSubmitted] = useState(false);

const questions = [
  {
    interviewer: "HR Interviewer",
    role: "Behavioral & Communication",
    avatar: "👩‍💼",
    question: "Tell me about yourself and your background."
  },
  {
    interviewer: "HR Interviewer",
    role: "Behavioral & Communication",
    avatar: "👩‍💼",
    question: "What is one challenge you faced and how did you overcome it?"
  },
  {
    interviewer: "Technical Interviewer",
    role: "Technical Knowledge",
    avatar: "👨‍💻",
    question: "What is the difference between an array and a linked list?"
  },
  {
    interviewer: "Technical Interviewer",
    role: "Problem Solving",
    avatar: "👨‍💻",
    question: "How would you approach solving a problem you have never seen before?"
  },
  {
    interviewer: "Product Manager",
    role: "Product Thinking",
    avatar: "👨‍💼",
    question: "How would you improve a product that users are complaining about?"
  }
];

const currentQuestion = questions[questionIndex];

  if (screen === "setup") {
    return (
      <div className="setup-page">
        <div className="setup-container">

          <button
            className="back-button"
            onClick={() => setScreen("home")}
          >
            ← Back
          </button>

          <div className="setup-header">
            <div className="badge">
              ✦ Interview Setup
            </div>

            <h1>
              Let's prepare your
              <span> interview.</span>
            </h1>

            <p>
              Configure your interview before meeting
              your EVA AI panel.
            </p>
          </div>

          <div className="setup-card">

            <div className="setup-group">
              <label>Job Role</label>

              <select>
                <option>Software Engineer</option>
                <option>Frontend Developer</option>
                <option>Backend Developer</option>
                <option>Full Stack Developer</option>
                <option>Data Analyst</option>
                <option>Product Manager</option>
              </select>
            </div>

            <div className="setup-group">
              <label>Experience Level</label>

              <select>
                <option>Fresher</option>
                <option>0 - 2 Years</option>
                <option>2 - 5 Years</option>
                <option>5+ Years</option>
              </select>
            </div>

            <div className="setup-group">
              <label>Interview Focus</label>

              <div className="focus-options">

                <button className="focus-option selected">
                  <span>🎯</span>
                  <div>
                    <strong>Full Interview</strong>
                    <small>HR + Technical + Product</small>
                  </div>
                </button>

                <button className="focus-option">
                  <span>💻</span>
                  <div>
                    <strong>Technical</strong>
                    <small>Technical skills & problem solving</small>
                  </div>
                </button>

                <button className="focus-option">
                  <span>👩‍💼</span>
                  <div>
                    <strong>HR</strong>
                    <small>Communication & behavioral skills</small>
                  </div>
                </button>

              </div>
            </div>

            <div className="setup-group">
              <label>Interview Duration</label>

              <div className="duration-options">
                <button className="duration selected">
                  10 min
                </button>

                <button className="duration">
                  20 min
                </button>

                <button className="duration">
                  30 min
                </button>
              </div>
            </div>

            <button
              className="primary-button setup-start"
              onClick={() => setScreen("interview")}
            >
              🎙️ Start EVA Interview →
            </button>

          </div>

          <div className="setup-note">
            💡 EVA will adapt the interview based on your answers.
          </div>

        </div>
      </div>
    );
  }

  if (screen === "interview") {
    const handleSubmit = () => {
      if (answer.trim() === "") {
        return;
      }

      setSubmitted(true);
    };

    const handleNext = () => {
      if (questionIndex < questions.length - 1) {
        setQuestionIndex(questionIndex + 1);
        setAnswer("");
        setSubmitted(false);
      } else {
        setScreen("home");
        setQuestionIndex(0);
        setAnswer("");
        setSubmitted(false);
      }
    };

    return (
      <div className="interview-page">

        {/* Top Bar */}
        <div className="interview-topbar">

          <div className="logo">
            <span className="logo-icon">E</span>
            <span>EVA</span>
          </div>

          <div className="interview-status">
            <span className="status-dot"></span>
            Interview in progress
          </div>

          <button
            className="nav-button"
            onClick={() => setScreen("home")}
          >
            Exit Interview
          </button>

        </div>

        {/* Interview Area */}
        <div className="interview-container">

          <div className="question-section">

            <span className="question-label">
              CURRENT INTERVIEWER
            </span>

            <div className="current-interviewer">

              <div className="large-avatar">
                {currentQuestion.avatar}
              </div>

              <div>
                <h2>{currentQuestion.interviewer}</h2>
                <p>{currentQuestion.role}</p>
              </div>

            </div>

            {/* Question */}
            <div className="question-card">

              <span>
                Question {questionIndex + 1} of {questions.length}
              </span>

              <h1>
                {currentQuestion.question}
              </h1>

              <p>
                Take a moment to think about your answer.
                Speak naturally and clearly.
              </p>

            </div>

            {/* Answer */}
            <div className="answer-area">

              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Type your answer here..."
                disabled={submitted}
              />

              {!submitted ? (
                <button
                  className="primary-button submit-button"
                  onClick={handleSubmit}
                >
                  Submit Answer →
                </button>
              ) : (
                <div className="feedback-box">

                  <div className="feedback-title">
                    🧠 EVA Quick Analysis
                  </div>

                  <p>
                    Good attempt! EVA has recorded your response
                    and is ready to continue the interview.
                  </p>

                  <button
                    className="primary-button"
                    onClick={handleNext}
                  >
                    {questionIndex < questions.length - 1
                      ? "Next Question →"
                      : "Finish Interview →"}
                  </button>

                </div>
              )}

            </div>

            <p className="voice-hint">
              🎙️ Voice interaction will be connected in the next stage.
            </p>

          </div>

          {/* AI Panel */}
          <div className="live-panel">

            <div className="panel-header">
              <span>AI Interview Panel</span>
              <span className="live-badge">LIVE</span>
            </div>

            <div className="interviewer-card active">

              <div className="avatar">
                👩‍💼
              </div>

              <div className="interviewer-info">
                <h3>HR Interviewer</h3>
                <p>
                  {currentQuestion.interviewer === "HR Interviewer"
                    ? "Currently interviewing"
                    : "Listening"}
                </p>
              </div>

            </div>

            <div className="interviewer-card">

              <div className="avatar">
                👨‍💻
              </div>

              <div className="interviewer-info">
                <h3>Technical Interviewer</h3>
                <p>
                  {currentQuestion.interviewer === "Technical Interviewer"
                    ? "Currently interviewing"
                    : "Listening"}
                </p>
              </div>

            </div>

            <div className="interviewer-card">

              <div className="avatar">
                👨‍💼
              </div>

              <div className="interviewer-info">
                <h3>Product Manager</h3>
                <p>
                  {currentQuestion.interviewer === "Product Manager"
                    ? "Currently interviewing"
                    : "Listening"}
                </p>
              </div>

            </div>

            <div className="context-box">

              <span>🧠</span>

              <div>
                <strong>Shared Context</strong>

                <p>
                  All interviewers understand the
                  conversation so far.
                </p>
              </div>

            </div>

          </div>

        </div>

      </div>
    );
  }

  return (
    <div className="app-shell">

      {/* Navigation */}
      <nav className="navbar">

        <div className="logo">
          <span className="logo-icon">E</span>
          <span>EVA</span>
        </div>

        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#panel">AI Panel</a>
          <a href="#about">About</a>
        </div>

        <button
          className="nav-button"
          onClick={() => setScreen("setup")}
        >
          Get Started
        </button>

      </nav>

      {/* Hero */}
      <main>

        <section className="hero">

          <div className="hero-content">

            <div className="badge">
              ✦ AI-Powered Interview Experience
            </div>

            <h1>
              Meet Your
              <span> AI Interview Panel</span>
            </h1>

            <p>
              EVA creates a realistic interview experience
              where multiple AI interviewers understand your
              answers, adapt their questions, and evaluate
              your performance.
            </p>

            <div className="hero-buttons">

              <button
                className="primary-button"
                onClick={() => setScreen("setup")}
              >
                🎙️ Start Interview
              </button>

              <button className="secondary-button">
                Explore EVA →
              </button>

            </div>

            <div className="hero-stats">

              <div>
                <strong>3</strong>
                <span>AI Interviewers</span>
              </div>

              <div>
                <strong>AI</strong>
                <span>Adaptive Questions</span>
              </div>

              <div>
                <strong>360°</strong>
                <span>Evaluation</span>
              </div>

            </div>

          </div>

          {/* AI Panel Preview */}
          <div className="hero-panel">

            <div className="panel-header">

              <div>
                <span className="status-dot"></span>
                EVA Interview Panel
              </div>

              <span className="live-badge">
                LIVE
              </span>

            </div>

            <div className="interviewer-card active">

              <div className="avatar">
                👩‍💼
              </div>

              <div className="interviewer-info">
                <h3>HR Interviewer</h3>
                <p>Behavioral & Communication</p>
              </div>

              <span className="speaking">
                Speaking...
              </span>

            </div>

            <div className="interviewer-card">

              <div className="avatar">
                👨‍💻
              </div>

              <div className="interviewer-info">
                <h3>Technical Interviewer</h3>
                <p>Technical Knowledge</p>
              </div>

            </div>

            <div className="interviewer-card">

              <div className="avatar">
                👨‍💼
              </div>

              <div className="interviewer-info">
                <h3>Product Manager</h3>
                <p>Product Thinking</p>
              </div>

            </div>

            <div className="panel-message">

              <span>💡</span>

              <p>
                Interviewers share your conversation context
                and adapt questions based on your responses.
              </p>

            </div>

          </div>

        </section>

        {/* Features */}
        <section
          className="features-section"
          id="features"
        >

          <div className="section-heading">

            <span>WHY EVA?</span>

            <h2>
              More than a typical
              <span> AI interview bot.</span>
            </h2>

            <p>
              EVA transforms fixed question-and-answer
              practice into an adaptive, multi-perspective
              interview.
            </p>

          </div>

          <div className="features-grid">

            <div className="feature-card">
              <div className="feature-icon">🤖</div>

              <h3>Multi-AI Panel</h3>

              <p>
                HR, Technical and Product interviewers
                provide different perspectives.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🧠</div>

              <h3>Adaptive Questions</h3>

              <p>
                Questions change according to the candidate's
                previous responses and performance.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🔄</div>

              <h3>Dynamic Follow-ups</h3>

              <p>
                EVA explores vague, incomplete or contradictory
                answers instead of simply moving forward.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📊</div>

              <h3>Evidence-Based Feedback</h3>

              <p>
                Performance feedback is connected directly
                to the candidate's interview responses.
              </p>
            </div>

          </div>

        </section>

        {/* AI Panel */}
        <section
          className="panel-section"
          id="panel"
        >

          <div className="section-heading">

            <span>
              ONE CANDIDATE. MULTIPLE PERSPECTIVES.
            </span>

            <h2>
              Meet the EVA
              <span> AI Panel</span>
            </h2>

            <p>
              Each interviewer focuses on a different aspect
              of the candidate while sharing the same
              conversation context.
            </p>

          </div>

          <div className="roles-grid">

            <div className="role-card">

              <div className="large-avatar">
                👩‍💼
              </div>

              <h3>HR Interviewer</h3>

              <p>
                Evaluates communication, behavior,
                confidence and clarity.
              </p>

              <span>Behavioral</span>

            </div>

            <div className="role-card">

              <div className="large-avatar">
                👨‍💻
              </div>

              <h3>Technical Interviewer</h3>

              <p>
                Evaluates technical knowledge,
                reasoning and problem-solving.
              </p>

              <span>Technical</span>

            </div>

            <div className="role-card">

              <div className="large-avatar">
                👨‍💼
              </div>

              <h3>Product Manager</h3>

              <p>
                Evaluates product thinking,
                decision-making and user perspective.
              </p>

              <span>Product</span>

            </div>

          </div>

        </section>

        {/* About */}
        <section
          className="about-section"
          id="about"
        >

          <div>

            <span>THE EVA FLOW</span>

            <h2>
              Voice → Understand → Adapt → Evaluate → Improve
            </h2>

          </div>

          <div className="flow">

            <div>
              🎙️
              <span>Speak</span>
            </div>

            <div>
              🧠
              <span>Analyze</span>
            </div>

            <div>
              🔄
              <span>Adapt</span>
            </div>

            <div>
              📋
              <span>Evaluate</span>
            </div>

          </div>

        </section>

      </main>

      {/* Footer */}
      <footer>

        <div className="logo">
          <span className="logo-icon">E</span>
          <span>EVA</span>
        </div>

        <p>
          Enhanced Voice-based AI Interviewer
        </p>

        <span>
          Team EchoSphere • Hackathon 2026
        </span>

      </footer>

    </div>
  );
}

export default App;