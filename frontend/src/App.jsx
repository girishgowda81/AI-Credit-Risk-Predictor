import React, { useState, useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';
import { Doughnut, Line } from 'react-chartjs-2';
import {
    Shield,
    LayoutDashboard,
    History,
    Settings,
    User,
    AlertTriangle,
    CheckCircle,
    Info,
    ChevronRight,
    Loader2
} from 'lucide-react';

Chart.register(...registerables);

const App = () => {
    const [activeTab, setActiveTab] = useState('dashboard');
    const [loading, setLoading] = useState(false);
    const [prediction, setPrediction] = useState(null);
    const [history, setHistory] = useState([]);
    const [formData, setFormData] = useState({
        fullName: 'John Doe',
        age: 30,
        gender: 'Male',
        income: 50000,
        creditScore: 700,
        loanAmount: 15000,
        prevDefaults: 0,
        dti: 0.25,
        tenure: '36',
        housing: 'Own'
    });

    useEffect(() => {
        if (activeTab === 'history') {
            fetchHistory();
        }
    }, [activeTab]);

    const fetchHistory = async () => {
        try {
            const apiBase = import.meta.env.VITE_API_URL || '';
            const response = await fetch(`${apiBase}/api/history`);
            const data = await response.json();
            setHistory(data);
        } catch (error) {
            console.error('Error fetching history:', error);
        }
    };

    const handleInputChange = (e) => {
        const { id, value } = e.target;
        setFormData(prev => ({ ...prev, [id]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const applicationData = {
            borrower: {
                full_name: formData.fullName,
                age: parseInt(formData.age),
                gender: formData.gender,
                income: parseFloat(formData.income),
                employment_duration: parseInt(formData.age) * 12 - 240,
                housing_status: formData.housing
            },
            loan_amount: parseFloat(formData.loanAmount),
            loan_purpose: "Personal",
            tenure: parseInt(formData.tenure),
            interest_rate: 0.12,
            credit_score: parseInt(formData.creditScore),
            previous_defaults: parseInt(formData.prevDefaults),
            debt_to_income_ratio: parseFloat(formData.dti)
        };

        try {
            const apiBase = import.meta.env.VITE_API_URL || '';
            const response = await fetch(`${apiBase}/api/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(applicationData)
            });
            const data = await response.json();
            setPrediction(data);
            // Wait a bit for scroll as the card appears
            setTimeout(() => {
                document.getElementById('result-card')?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the prediction server.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <aside className="sidebar">
                <div className="logo">
                    <Shield className="logo-icon" size={28} />
                    <h1>NexaLend AI</h1>
                </div>
                <nav>
                    <button
                        className={activeTab === 'dashboard' ? 'active' : ''}
                        onClick={() => setActiveTab('dashboard')}
                    >
                        <LayoutDashboard size={20} className="nav-icon" /> Dashboard
                    </button>
                    <button
                        className={activeTab === 'history' ? 'active' : ''}
                        onClick={() => setActiveTab('history')}
                    >
                        <History size={20} className="nav-icon" /> History
                    </button>
                    <button
                        className={activeTab === 'settings' ? 'active' : ''}
                        onClick={() => setActiveTab('settings')}
                    >
                        <Settings size={20} className="nav-icon" /> Settings
                    </button>
                </nav>
            </aside>

            <main className="main-content">
                <header>
                    <div className="user-profile">
                        <span>Admin Officer</span>
                        <div className="avatar">
                            <User size={20} />
                        </div>
                    </div>
                </header>

                {activeTab === 'dashboard' && (
                    <div className="view">
                        <div className="dashboard-grid">
                            <section className="card form-section">
                                <h2>New Loan Application</h2>
                                <form onSubmit={handleSubmit}>
                                    <div className="form-group-row">
                                        <div className="form-group">
                                            <label>Full Name</label>
                                            <input type="text" id="fullName" value={formData.fullName} onChange={handleInputChange} required />
                                        </div>
                                        <div className="form-group">
                                            <label>Age</label>
                                            <input type="number" id="age" value={formData.age} onChange={handleInputChange} required />
                                        </div>
                                    </div>

                                    <div className="form-group-row">
                                        <div className="form-group">
                                            <label>Gender</label>
                                            <select id="gender" value={formData.gender} onChange={handleInputChange}>
                                                <option value="Male">Male</option>
                                                <option value="Female">Female</option>
                                            </select>
                                        </div>
                                        <div className="form-group">
                                            <label>Annual Income ($)</label>
                                            <input type="number" id="income" value={formData.income} onChange={handleInputChange} required />
                                        </div>
                                    </div>

                                    <div className="form-group-row">
                                        <div className="form-group">
                                            <label>Credit Score</label>
                                            <input type="number" id="creditScore" value={formData.creditScore} onChange={handleInputChange} min="300" max="850" required />
                                        </div>
                                        <div className="form-group">
                                            <label>Loan Amount ($)</label>
                                            <input type="number" id="loanAmount" value={formData.loanAmount} onChange={handleInputChange} required />
                                        </div>
                                    </div>

                                    <div className="form-group-row">
                                        <div className="form-group">
                                            <label>Previous Defaults</label>
                                            <input type="number" id="prevDefaults" value={formData.prevDefaults} onChange={handleInputChange} required />
                                        </div>
                                        <div className="form-group">
                                            <label>Debt-to-Income Ratio</label>
                                            <input type="number" id="dti" step="0.01" value={formData.dti} onChange={handleInputChange} required />
                                        </div>
                                    </div>

                                    <div className="form-group-row">
                                        <div className="form-group">
                                            <label>Tenure (Months)</label>
                                            <select id="tenure" value={formData.tenure} onChange={handleInputChange}>
                                                <option value="12">12 Months</option>
                                                <option value="24">24 Months</option>
                                                <option value="36">36 Months</option>
                                                <option value="48">48 Months</option>
                                                <option value="60">60 Months</option>
                                            </select>
                                        </div>
                                        <div className="form-group">
                                            <label>Housing</label>
                                            <select id="housing" value={formData.housing} onChange={handleInputChange}>
                                                <option value="Own">Own</option>
                                                <option value="Rent">Rent</option>
                                                <option value="Mortgage">Mortgage</option>
                                            </select>
                                        </div>
                                    </div>

                                    <button type="submit" className="submit-btn" disabled={loading}>
                                        {loading ? <><Loader2 className="animate-spin" size={18} /> Analyzing...</> : 'Assess Risk Score'}
                                    </button>
                                </form>
                            </section>

                            {prediction && (
                                <section className="card result-section" id="result-card">
                                    <h2>Assessment Result</h2>
                                    <div className="risk-meter-container">
                                        <div className="meter-wrapper">
                                            <Doughnut
                                                data={{
                                                    datasets: [{
                                                        data: [prediction.probability * 100, 100 - (prediction.probability * 100)],
                                                        backgroundColor: [
                                                            prediction.probability < 0.3 ? '#10B981' : prediction.probability < 0.7 ? '#F59E0B' : '#EF4444',
                                                            '#1e293b'
                                                        ],
                                                        borderWidth: 0,
                                                        circumference: 180,
                                                        rotation: 270,
                                                        borderRadius: 10
                                                    }]
                                                }}
                                                options={{
                                                    cutout: '85%',
                                                    plugins: { legend: { display: false }, tooltip: { enabled: false } },
                                                    maintainAspectRatio: false
                                                }}
                                            />
                                            <div className="risk-label-centered">
                                                <span>{prediction.risk_level} RISK</span>
                                                <h3>{(prediction.probability * 100).toFixed(1)}%</h3>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="result-details">
                                        <div className="detail-item">
                                            <span className="label">Recommendation:</span>
                                            <span className={`value ${prediction.recommendation.toLowerCase().replace(' ', '')}`}>
                                                {prediction.recommendation}
                                            </span>
                                        </div>
                                        <div className="detail-item">
                                            <span className="label">Predicted Default:</span>
                                            <span className="value" style={{ color: prediction.prediction ? '#ef4444' : '#10b981' }}>
                                                {prediction.prediction ? 'YES' : 'NO'}
                                            </span>
                                        </div>
                                    </div>

                                    <h3>Explanatory Factors</h3>
                                    <div className="explanation-list">
                                        {prediction.explanation.map((item, idx) => (
                                            <div key={idx} className="exp-item">
                                                <div className="exp-name">{item.feature.replace('num__', '').replace('cat__', '')}</div>
                                                <div className="exp-bar-container">
                                                    <div
                                                        className={`exp-bar ${item.impact > 0 ? 'pos' : 'neg'}`}
                                                        style={{ width: `${Math.min(Math.abs(item.impact) * 500, 100)}%` }}
                                                    />
                                                </div>
                                                <div className="exp-val">{item.impact > 0 ? '+' : '-'}{Math.abs(item.impact).toFixed(2)}</div>
                                            </div>
                                        ))}
                                    </div>
                                </section>
                            )}

                            <section className="card metrics-section">
                                <h2>Model Performance</h2>
                                <div className="metrics-row">
                                    <div className="metric-card">
                                        <span className="m-label">AUC-ROC</span>
                                        <span className="m-value">0.945</span>
                                    </div>
                                    <div className="metric-card">
                                        <span className="m-label">Accuracy</span>
                                        <span className="m-value">89.2%</span>
                                    </div>
                                </div>
                                <div className="chart-wrapper">
                                    <Line
                                        data={{
                                            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                                            datasets: [{
                                                label: 'Accuracy',
                                                data: [0.82, 0.85, 0.87, 0.88, 0.89, 0.89],
                                                borderColor: '#818CF8',
                                                backgroundColor: 'rgba(129, 140, 248, 0.1)',
                                                fill: true,
                                                tension: 0.4
                                            }]
                                        }}
                                        options={{
                                            plugins: { legend: { display: false } },
                                            scales: {
                                                y: {
                                                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                                                    ticks: { color: '#94a3b8' }
                                                },
                                                x: {
                                                    grid: { display: false },
                                                    ticks: { color: '#94a3b8' }
                                                }
                                            },
                                            maintainAspectRatio: false
                                        }}
                                    />
                                </div>
                            </section>
                        </div>
                    </div>
                )}

                {activeTab === 'history' && (
                    <div className="view">
                        <div className="card">
                            <h2>Prediction History</h2>
                            <div className="history-table-wrapper">
                                <table className="history-table">
                                    <thead>
                                        <tr>
                                            <th>Date</th>
                                            <th>Application ID</th>
                                            <th>Risk Level</th>
                                            <th>Probability</th>
                                            <th>Prediction</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {history.map(item => (
                                            <tr key={item.id}>
                                                <td>{new Date(item.created_at).toLocaleDateString()}</td>
                                                <td>APP-{item.application_id}</td>
                                                <td><span className={`badge ${item.risk_level.toLowerCase()}`}>{item.risk_level}</span></td>
                                                <td>{(item.probability * 100).toFixed(1)}%</td>
                                                <td style={{ color: item.prediction ? '#ef4444' : '#10b981', fontWeight: 600 }}>
                                                    {item.prediction ? 'DEFAULT' : 'CLEAN'}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'settings' && (
                    <div className="view">
                        <div className="card">
                            <h2>System Settings</h2>
                            <div className="settings-grid">
                                <div className="setting-item">
                                    <label>Model Version</label>
                                    <input type="text" value="v1.0.3 (XGBoost Engine)" disabled />
                                </div>
                                <div className="setting-item">
                                    <label>Decision Threshold</label>
                                    <input type="range" min="0" max="1" step="0.05" defaultValue="0.75" />
                                </div>
                                <div className="setting-item">
                                    <label>Notification Email</label>
                                    <input type="email" placeholder="admin@nexalend.ai" />
                                </div>
                                <button className="save-btn">Update Config</button>
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
};

export default App;
