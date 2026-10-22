const express = require("express");
const mongoose = require("mongoose");

const app = express();

app.use(express.json());

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    age: {
        type: Number
    },
    email: {
        type: String
    }
});

const User = mongoose.model("User", userSchema);

const seedUsers = async () => {
    try {
        const count = await User.countDocuments();
        if (count === 0) {
            await User.create([
                { name: "Alice Johnson", age: 28, email: "alice@example.com" },
                { name: "Bob Smith", age: 34, email: "bob@example.com" }
            ]);
            console.log("Database seeded with sample users.");
        }
    } catch (error) {
        console.error("Error seeding users:", error);
    }
};

mongoose
    .connect("mongodb://127.0.0.1:27017/cbajuly")
    .then(async () => {
        console.log("MongoDB connected successfully..");
        await seedUsers();
    })
    .catch((error) => {
        console.log("Error in connection..", error);
    });

app.get("/", (req, res) => {
    res.send("MongoDB API is working!");
});

app.post("/users", async (req, res) => {
    try {
        const user = new User({
            name: req.body.name,
            age: req.body.age,
            email: req.body.email
        });

        const savedUser = await user.save();

        res.status(201).json(savedUser);
    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
});

app.get("/users", async (req, res) => {
    try {
        const users = await User.find();

        res.status(200).json(users);
    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
});

app.get("/users/:id", async (req, res) => {
    try {
        const user = await User.findById(req.params.id);

        if (!user) {
            return res.status(404).json({
                message: "User not found"
            });
        }

        res.status(200).json(user);
    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
});

app.put("/users/:id", async (req, res) => {
    try {
        const user = await User.findByIdAndUpdate(
            req.params.id,
            req.body,
            {
                new: true,
                runValidators: true
            }
        );

        if (!user) {
            return res.status(404).json({
                message: "User not found"
            });
        }

        res.status(200).json(user);
    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
});

app.delete("/users/:id", async (req, res) => {
    try {
        const user = await User.findByIdAndDelete(req.params.id);

        if (!user) {
            return res.status(404).json({
                message: "User not found"
            });
        }

        res.status(200).json({
            message: "User deleted successfully",
            user: user
        });
    } catch (error) {
        res.status(500).json({
            message: error.message
        });
    }
});

app.listen(5001, () => {
    console.log("Server running on port 5001");
});
