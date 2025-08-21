const express = require("express");
const app = express();

app.use(express.json());

app.post("/", (req, res) => {
    const {
        grower_id,
        fruit_id,
        varietal_id,
        batch_id,
        process_stage,
        process_date
    } = req.body;

    if (!grower_id || !fruit_id || !varietal_id || !batch_id || !process_stage || !process_date) {
        return res.status(400).json({ error: "Missing required field(s)." });
    }

    try {
        const date = new Date(process_date);
        if (isNaN(date.getTime())) throw new Error("Invalid date format");

        const yymmdd = date.toISOString().slice(2, 10).replace(/-/g, '');
        const tracking_id = `${grower_id}.${fruit_id}.${varietal_id}.${batch_id}.${process_stage}.${yymmdd}`;

        return res.status(200).json({
            tracking_id,
            status: "success"
        });
    } catch (err) {
        return res.status(400).json({ error: err.message });
    }
});

module.exports = app;