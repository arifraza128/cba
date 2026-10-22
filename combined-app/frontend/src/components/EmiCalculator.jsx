import { useState } from "react";

function EmiCalculator({ showToast }) {
  const [loanAmount, setLoanAmount] = useState("");
  const [interestRate, setInterestRate] = useState("");
  const [tenure, setTenure] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateEMI = async (e) => {
    e.preventDefault();

    if (!loanAmount || !interestRate || !tenure) {
      if (showToast) showToast("Please fill in all inputs", "error");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/calculate-emi", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          loanAmount: Number(loanAmount),
          interestRate: Number(interestRate),
          tenure: Number(tenure),
        }),
      });

      if (!response.ok) throw new Error("Failed to calculate");

      const data = await response.json();
      setResult(data);
      if (showToast) showToast("EMI calculated successfully!", "success");
    } catch (error) {
      console.error(error);
      if (showToast) showToast("Calculation server failed.", "error");
    } finally {
      setLoading(false);
    }
  };

  const clearForm = () => {
    setLoanAmount("");
    setInterestRate("");
    setTenure("");
    setResult(null);
  };

  return (
    <div className="module-container">
      <div className="module-header">
        <h2>🧮 Loan EMI Calculator</h2>
        <p>Estimate your monthly payments, total interest, and complete loan payoff schedule</p>
      </div>

      <div className="module-grid">
        {/* Input Form */}
        <div className="card form-card">
          <h3>Loan Parameters</h3>
          <form onSubmit={calculateEMI} className="modern-form">
            <div className="input-group">
              <label>Loan Amount (₹)</label>
              <input
                type="number"
                placeholder="e.g. 500000"
                value={loanAmount}
                onChange={(e) => setLoanAmount(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>Interest Rate (Annual %)</label>
              <input
                type="number"
                step="0.01"
                placeholder="e.g. 8.5"
                value={interestRate}
                onChange={(e) => setInterestRate(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>Tenure (Months)</label>
              <input
                type="number"
                placeholder="e.g. 24"
                value={tenure}
                onChange={(e) => setTenure(e.target.value)}
              />
            </div>

            <div className="form-actions-row">
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? "Calculating..." : "🧮 Compute EMI"}
              </button>
              <button type="button" className="btn btn-secondary" onClick={clearForm}>
                Clear
              </button>
            </div>
          </form>
        </div>

        {/* Results Showcase */}
        <div className="card list-card">
          <h3>Calculated Breakdown</h3>
          {!result ? (
            <div className="empty-state">
              <span>📊</span>
              <p>Enter the loan details and click calculate to view the repayment breakdown.</p>
            </div>
          ) : (
            <div className="emi-result-content">
              <div className="result-main-card">
                <span className="result-label">Monthly EMI</span>
                <span className="result-val text-teal">₹{Number(result.emi).toLocaleString()}</span>
              </div>

              <div className="result-breakdown-grid">
                <div className="breakdown-item">
                  <span className="breakdown-label">Principal Amount</span>
                  <span className="breakdown-val">₹{Number(loanAmount).toLocaleString()}</span>
                </div>
                <div className="breakdown-item">
                  <span className="breakdown-label">Total Interest</span>
                  <span className="breakdown-val text-amber">₹{Number(result.totalInterest).toLocaleString()}</span>
                </div>
                <div className="breakdown-item">
                  <span className="breakdown-label">Total Repayment</span>
                  <span className="breakdown-val text-indigo">₹{Number(result.totalRepayment).toLocaleString()}</span>
                </div>
              </div>

              {/* Progress visual showing Principal vs Interest Ratio */}
              {Number(result.totalRepayment) > 0 && (
                <div className="ratio-container">
                  <h4>Repayment Breakdown Ratio</h4>
                  <div className="progress-bar-bg flex-progress">
                    <div
                      className="progress-bar-fill bg-indigo"
                      style={{
                        width: `${(Number(loanAmount) / Number(result.totalRepayment)) * 100}%`,
                      }}
                      title="Principal"
                    ></div>
                    <div
                      className="progress-bar-fill bg-amber"
                      style={{
                        width: `${(Number(result.totalInterest) / Number(result.totalRepayment)) * 100}%`,
                      }}
                      title="Interest"
                    ></div>
                  </div>
                  <div className="ratio-legend">
                    <span className="legend-dot bg-indigo">Principal ({( (Number(loanAmount) / Number(result.totalRepayment)) * 100 ).toFixed(0)}%)</span>
                    <span className="legend-dot bg-amber">Interest ({( (Number(result.totalInterest) / Number(result.totalRepayment)) * 100 ).toFixed(0)}%)</span>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default EmiCalculator;
