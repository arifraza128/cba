const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());


// EMI API
app.post("/calculate-emi", (req, res) => {

    const { loanAmount, interestRate, tenure } = req.body;

    // Convert yearly interest rate to monthly
    const monthlyRate = interestRate / 12 / 100;

    // EMI formula
    const emi =
        loanAmount *
        monthlyRate *
        Math.pow(1 + monthlyRate, tenure) /
        (Math.pow(1 + monthlyRate, tenure) - 1);

    // Total repayment
    const totalRepayment = emi * tenure;

    // Total interest
    const totalInterest = totalRepayment - loanAmount;


    res.json({
        emi: emi.toFixed(2),
        totalInterest: totalInterest.toFixed(2),
        totalRepayment: totalRepayment.toFixed(2)
    });

});


app.listen(5000, () => {
    console.log("Server running on port 5000");
});
