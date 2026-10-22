import { useState } from "react";
import "./App.css";

function App() {

    const [loanAmount, setLoanAmount] = useState("");
    const [interestRate, setInterestRate] = useState("");
    const [tenure, setTenure] = useState("");

    const [result, setResult] = useState(null);


    const calculateEMI = async (e) => {

        e.preventDefault();

        const response = await fetch(
            "http://localhost:5000/calculate-emi",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    loanAmount: Number(loanAmount),
                    interestRate: Number(interestRate),
                    tenure: Number(tenure)
                })
            }
        );

        const data = await response.json();

        setResult(data);
    };


    return (

        <div className="container">

            <h1>Loan EMI Calculator</h1>


            <form onSubmit={calculateEMI}>

                <input
                    type="number"
                    placeholder="Loan Amount"
                    value={loanAmount}
                    onChange={(e) =>
                        setLoanAmount(e.target.value)
                    }
                />


                <input
                    type="number"
                    placeholder="Interest Rate (%)"
                    value={interestRate}
                    onChange={(e) =>
                        setInterestRate(e.target.value)
                    }
                />


                <input
                    type="number"
                    placeholder="Loan Tenure (Months)"
                    value={tenure}
                    onChange={(e) =>
                        setTenure(e.target.value)
                    }
                />


                <button type="submit">
                    Calculate EMI
                </button>

            </form>


            {/* Result */}

            {result && (

                <div className="result">

                    <h2>Loan Details</h2>

                    <p>
                        Monthly EMI:
                        <strong> ₹{result.emi}</strong>
                    </p>

                    <p>
                        Total Interest:
                        <strong> ₹{result.totalInterest}</strong>
                    </p>

                    <p>
                        Total Repayment:
                        <strong> ₹{result.totalRepayment}</strong>
                    </p>

                </div>

            )}

        </div>

    );
}

export default App;
