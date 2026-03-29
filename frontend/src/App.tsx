import { useState, useEffect, useRef } from 'react'
import './App.css'
import confetti from 'canvas-confetti'
import { 
  Trophy, 
  Timer, 
  Flame, 
  XCircle, 
  CheckCircle2, 
  ChevronRight, 
  RotateCcw, 
  Sparkles,
  Layout,
  Code2,
  FileJson,
  Palette,
  Terminal,
  AlertTriangle
} from 'lucide-react'

interface Option {
  id: string;
  text: string;
}

interface Question {
  id: number;
  topic: string;
  question: string;
  options: Option[];
  correct_option_id: string;
  explanation: string;
}

interface QuizResult {
  score: number;
  total: number;
  details: any[];
}

const topicIcons: Record<string, any> = {
  'HTML': <Code2 className="topic-icon-img" />,
  'Python': <Terminal className="topic-icon-img" />,
  'CSS': <Palette className="topic-icon-img" />,
  'JavaScript': <FileJson className="topic-icon-img" />,
  'All': <Layout className="topic-icon-img" />
}

const topicColors: Record<string, string> = {
  'HTML': '#ff9800',
  'CSS': '#2196f3',
  'Python': '#4caf50',
  'JavaScript': '#fbc02d',
  'All': '#9c27b0'
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  console.log("App component rendering...");
  return <QuizApp />;
}

function QuizApp() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [result, setResult] = useState<QuizResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [quizStarted, setQuizStarted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Setup states
  const [topics, setTopics] = useState<string[]>([]);
  const [selectedTopic, setSelectedTopic] = useState('All');
  const [questionCount, setQuestionCount] = useState(5);
  
  // Gameplay states
  const [streak, setStreak] = useState(0);
  const [maxStreak, setMaxStreak] = useState(0);
  
  // Timer states
  const [timeLeft, setTimeLeft] = useState(30 * 60);
  const timerRef = useRef<any>(null);

  // AI states
  const [aiLoading, setAiLoading] = useState<number | null>(null);
  const [aiExplanations, setAiExplanations] = useState<Record<number, string>>({});

  useEffect(() => {
    console.log("Fetching topics...");
    fetch(`${API_BASE_URL}/topics`)
      .then(res => res.json())
      .then(data => {
        console.log("Topics fetched:", data);
        setTopics(['All', ...data]);
      })
      .catch(err => {
        console.error("Failed to fetch topics:", err);
        setError("Could not connect to the backend. Please ensure it is running.");
      });
  }, []);

  useEffect(() => {
    if (quizStarted && !result && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    } else if (timeLeft === 0 && !result && quizStarted) {
      submitQuiz();
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [quizStarted, result, timeLeft]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const startQuiz = () => {
    setLoading(true);
    setError(null);
    console.log(`Starting quiz for ${selectedTopic} with ${questionCount} questions`);
    fetch(`${API_BASE_URL}/questions?topic=${selectedTopic}&count=${questionCount}`)
      .then(res => {
        if (!res.ok) throw new Error("Backend responded with an error");
        return res.json();
      })
      .then(data => {
        console.log("Questions fetched:", data);
        if (!Array.isArray(data) || data.length === 0) {
          throw new Error("No questions found for this selection.");
        }
        setQuestions(data);
        setQuizStarted(true);
        setLoading(false);
        setTimeLeft(30 * 60);
        setAnswers({});
        setCurrentIndex(0);
        setResult(null);
        setAiExplanations({});
        setStreak(0);
        setMaxStreak(0);
      })
      .catch(err => {
        console.error("Failed to fetch questions:", err);
        setError(err.message || "Failed to start the quiz. Please try again.");
        setLoading(false);
      });
  };

  const quitQuiz = () => {
    if (window.confirm("Quit current session?")) {
      setQuizStarted(false);
      setQuestions([]);
      setResult(null);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  const handleOptionSelect = (optionId: string) => {
    if (!questions[currentIndex]) return;
    if (answers[questions[currentIndex].id]) return;

    const isCorrect = optionId === questions[currentIndex].correct_option_id;
    
    if (isCorrect) {
      const newStreak = streak + 1;
      setStreak(newStreak);
      if (newStreak > maxStreak) setMaxStreak(newStreak);
      if (newStreak % 5 === 0) {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
      }
    } else {
      setStreak(0);
    }

    setAnswers({
      ...answers,
      [questions[currentIndex].id]: optionId
    });
  };

  const submitQuiz = () => {
    const submission = questions.map(q => ({
      question_id: q.id,
      selected_option_id: answers[q.id] || ''
    }));

    fetch(`${API_BASE_URL}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(submission)
    })
      .then(res => res.json())
      .then(data => {
        setResult(data);
        if (data.score === data.total && data.total > 0) {
          confetti({
            particleCount: 200,
            spread: 160,
            origin: { y: 0.6 }
          });
        }
        if (timerRef.current) clearInterval(timerRef.current);
      })
      .catch(err => {
        console.error("Failed to submit quiz:", err);
        setError("Failed to submit results. Check your connection.");
      });
  };

  const askAI = (questionId: number, userAnsId: string) => {
    setAiLoading(questionId);
    fetch(`${API_BASE_URL}/ai-explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: questionId, user_answer_id: userAnsId })
    })
      .then(res => res.json())
      .then(data => {
        setAiExplanations(prev => ({ ...prev, [questionId]: data.ai_response }));
        setAiLoading(null);
      })
      .catch(err => {
        console.error("AI failed:", err);
        setAiLoading(null);
      });
  };

  const nextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const prevQuestion = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  // ERROR VIEW
  if (error) {
    return (
      <div className="error-container animate-in">
        <div className="card error-card">
          <AlertTriangle size={48} className="error-icon" />
          <h2>Something went wrong</h2>
          <p>{error}</p>
          <button className="mega-retry-btn" onClick={() => window.location.reload()}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // LOADING VIEW
  if (loading) return (
    <div className="loader-container">
      <div className="glass-loader">
        <div className="spinner"></div>
        <p>Curating your personalized challenge...</p>
      </div>
    </div>
  );

  // RESULT VIEW
  if (result) {
    return (
      <div className="result-container animate-in">
        <div className="card result-card">
          <div className="result-header-modern">
            <div className="result-titles">
              <h2>Mission Accomplished!</h2>
              <p>Here's how you performed today</p>
            </div>
            <div className="score-badge-v2">
              <div className="score-v2-main">{result.score}</div>
              <div className="score-v2-sub">/ {result.total}</div>
            </div>
          </div>

          <div className="stats-strip">
            <div className="stat-box">
              <div className="stat-val">{(result.score / result.total * 100).toFixed(0)}%</div>
              <div className="stat-lbl">Accuracy</div>
            </div>
            <div className="stat-box">
              <div className="stat-val">{maxStreak}</div>
              <div className="stat-lbl">Best Streak</div>
            </div>
            <div className="stat-box">
              <div className="stat-val">{formatTime(30 * 60 - timeLeft)}</div>
              <div className="stat-lbl">Time Taken</div>
            </div>
          </div>

          <div className="summary-list">
            {result.details.map((detail, index) => {
              const qTopicColor = topicColors[detail.topic] || topicColors['All'];
              return (
                <div key={index} className={`summary-item-v2 ${detail.is_correct ? 'correct' : 'incorrect'}`}>
                  <div className="summary-q-header">
                    <h4><span className="q-number" style={{ backgroundColor: qTopicColor, color: 'white' }}>#{index + 1}</span> {detail.question_text}</h4>
                    <button 
                      className="ai-btn-v2" 
                      onClick={() => askAI(detail.question_id, detail.selected_option_id)}
                      disabled={aiLoading === detail.question_id}
                    >
                      {aiLoading === detail.question_id ? 'Analyzing...' : <><Sparkles size={14} /> AI Deep Dive</>}
                    </button>
                  </div>

                  {aiExplanations[detail.question_id] && (
                    <div className="ai-chat-bubble">
                      <div className="ai-avatar"><Sparkles size={16} /></div>
                      <p>{aiExplanations[detail.question_id]}</p>
                    </div>
                  )}

                  <div className="summary-options-v2">
                    {detail.options.map((opt: any) => {
                      let state = '';
                      if (opt.id === detail.correct_option_id) state = 'correct';
                      if (opt.id === detail.selected_option_id && !detail.is_correct) state = 'wrong';
                      
                      return (
                        <div key={opt.id} className={`summary-option-v2 ${state}`}>
                          <div className="opt-text">{opt.text}</div>
                          {state === 'correct' && <CheckCircle2 size={16} className="state-icon" />}
                          {state === 'wrong' && <XCircle size={16} className="state-icon" />}
                        </div>
                      );
                    })}
                  </div>
                  <div className="explanation-v2" style={{ borderLeft: `4px solid ${qTopicColor}` }}>
                    <div className="exp-icon">💡</div>
                    <p>{detail.explanation}</p>
                  </div>
                </div>
              );
            })}
          </div>
          
          <button className="mega-retry-btn" onClick={() => window.location.reload()}>
            <RotateCcw size={20} /> Try New Topic
          </button>
        </div>
      </div>
    );
  }

  // SETUP VIEW
  if (!quizStarted) {
    return (
      <div className="setup-container">
        <div className="card setup-card animate-in">
          <div className="logo-section">
            <div className="logo-icon"><Trophy size={40} /></div>
            <h1>Quiz Master AI</h1>
            <p className="subtitle">The ultimate developer testing ground</p>
          </div>
          
          <div className="setup-grid">
            <div className="setup-group">
              <label>Field of Study</label>
              <div className="topic-selector">
                {topics.map(t => (
                  <button 
                    key={t} 
                    className={`topic-chip ${selectedTopic === t ? 'active' : ''} topic-${t.toLowerCase()}`}
                    onClick={() => setSelectedTopic(t)}
                  >
                    {topicIcons[t] || topicIcons['All']}
                    <span>{t}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="setup-group">
              <label>Challenge Length: <strong>{questionCount}</strong> questions</label>
              <input 
                type="range" 
                min="5" 
                max="50" 
                step="5"
                value={questionCount} 
                onChange={(e) => setQuestionCount(parseInt(e.target.value))} 
                className="modern-slider"
              />
              <div className="slider-labels">
                <span>Quick</span>
                <span>Standard</span>
                <span>Master</span>
              </div>
            </div>
          </div>

          <div className="setup-footer">
            <div className="info-badge"><Timer size={16} /> 30m Limit</div>
            <div className="info-badge"><Sparkles size={16} /> AI Tutor Active</div>
          </div>

          <button className="mega-start-btn" onClick={startQuiz}>
            Start Challenge <ChevronRight size={20} />
          </button>
        </div>
      </div>
    );
  }

  // QUIZ VIEW
  const currentQuestion = questions[currentIndex];
  if (!currentQuestion) {
    return (
      <div className="loader-container">
        <div className="glass-loader">
          <p>Loading questions...</p>
          <button className="mega-retry-btn" onClick={() => window.location.reload()}>Reset</button>
        </div>
      </div>
    );
  }

  const selectedOption = answers[currentQuestion.id];
  const activeColor = topicColors[currentQuestion.topic] || topicColors['All'];

  return (
    <div className="quiz-container animate-in">
      <div className="card quiz-card-v2">
        <div className="quiz-navbar">
          <div className="nav-left">
            <div className={`timer-v2 ${timeLeft < 60 ? 'critical' : ''}`}>
              <Timer size={18} /> {formatTime(timeLeft)}
            </div>
            <div className="streak-v2">
              <Flame size={18} className={streak > 0 ? 'flame-active' : ''} /> {streak}
            </div>
          </div>
          <button className="quit-btn-v2" onClick={quitQuiz}>Quit Session</button>
        </div>

        <div className="quiz-progress-v2">
          <div className="progress-text">
            <span style={{ color: activeColor }}>{currentQuestion.topic} Mastery</span>
            <span>{currentIndex + 1} of {questions.length}</span>
          </div>
          <div className="progress-bar-v2">
            <div 
              className="progress-fill-v2" 
              style={{ 
                width: `${((currentIndex + 1) / questions.length) * 100}%`,
                background: `linear-gradient(90deg, ${activeColor}, var(--success))`
              }}
            ></div>
          </div>
        </div>

        <h3 className="question-v2">{currentQuestion.question}</h3>
        
        <div className="options-grid-v2">
          {currentQuestion.options.map(option => {
            let feedback = '';
            if (selectedOption) {
              if (option.id === currentQuestion.correct_option_id) feedback = 'correct';
              else if (option.id === selectedOption) feedback = 'incorrect';
            }

            return (
              <button
                key={option.id}
                className={`option-card-v2 ${selectedOption === option.id ? 'selected' : ''} ${feedback}`}
                onClick={() => handleOptionSelect(option.id)}
                disabled={!!selectedOption}
                style={{
                    borderColor: selectedOption === option.id ? activeColor : undefined,
                    backgroundColor: selectedOption === option.id && !feedback ? `${activeColor}15` : undefined
                }}>
                <div className="opt-marker" style={{ 
                    backgroundColor: selectedOption === option.id ? activeColor : undefined,
                    color: selectedOption === option.id ? 'white' : undefined
                }}>
                    {option.id.toUpperCase()}
                </div>
                <div className="opt-label">{option.text}</div>
                {feedback === 'correct' && <CheckCircle2 size={20} className="feedback-icon" />}
                {feedback === 'incorrect' && <XCircle size={20} className="feedback-icon" />}
              </button>
            );
          })}
        </div>

        {selectedOption && (
          <div className="instant-feedback-v2 animate-slide-up" style={{ borderLeft: `4px solid ${activeColor}` }}>
            <div className={`feedback-header ${selectedOption === currentQuestion.correct_option_id ? 'success' : 'fail'}`}>
              {selectedOption === currentQuestion.correct_option_id ? <CheckCircle2 size={20} /> : <XCircle size={20} />}
              <span>{selectedOption === currentQuestion.correct_option_id ? 'Excellent Work!' : 'Not Quite Right'}</span>
            </div>
            <p className="feedback-body">{currentQuestion.explanation}</p>
          </div>
        )}

        <div className="quiz-footer-v2">
          <button 
            className="footer-nav-btn" 
            onClick={prevQuestion} 
            disabled={currentIndex === 0 || !!selectedOption}
          >
            Previous
          </button>
          
          {currentIndex === questions.length - 1 ? (
            <button 
                className="footer-submit-btn" 
                onClick={submitQuiz} 
                disabled={!selectedOption}
                style={{ backgroundColor: activeColor }}
            >
              Finish & Reveal <ChevronRight size={18} />
            </button>
          ) : (
            <button 
                className="footer-nav-btn next" 
                onClick={nextQuestion} 
                disabled={!selectedOption}
                style={{ backgroundColor: selectedOption ? activeColor : undefined }}
            >
              Next Question <ChevronRight size={18} />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
