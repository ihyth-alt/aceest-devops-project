from flask import Flask, jsonify, request

app = Flask(__name__)

# ── Program data (from ACEest app) ──────────────────────────────────────────
PROGRAMS = {
    "Fat Loss (FL)": {
        "calorie_factor": 22,
        "workout": (
            "Mon: Back Squat 5x5 + Core\n"
            "Tue: EMOM 20min Assault Bike\n"
            "Wed: Bench Press + 21-15-9\n"
            "Thu: Deadlift + Box Jumps\n"
            "Fri: Zone 2 Cardio 30min"
        ),
        "diet": (
            "Breakfast: Egg Whites + Oats\n"
            "Lunch: Grilled Chicken + Brown Rice\n"
            "Dinner: Fish Curry + Millet Roti\n"
            "Target: ~2000 kcal"
        ),
    },
    "Muscle Gain (MG)": {
        "calorie_factor": 35,
        "workout": (
            "Mon: Squat 5x5\n"
            "Tue: Bench 5x5\n"
            "Wed: Deadlift 4x6\n"
            "Thu: Front Squat 4x8\n"
            "Fri: Incline Press 4x10\n"
            "Sat: Barbell Rows 4x10"
        ),
        "diet": (
            "Breakfast: Eggs + Peanut Butter Oats\n"
            "Lunch: Chicken Biryani\n"
            "Dinner: Mutton Curry + Rice\n"
            "Target: ~3200 kcal"
        ),
    },
    "Beginner (BG)": {
        "calorie_factor": 26,
        "workout": (
            "Full Body Circuit:\n"
            "- Air Squats\n"
            "- Ring Rows\n"
            "- Push-ups\n"
            "Focus: Technique & Consistency"
        ),
        "diet": (
            "Balanced Tamil Meals\n"
            "Idli / Dosa / Rice + Dal\n"
            "Protein Target: 120g/day"
        ),
    },
}

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    """Health check / welcome endpoint."""
    return jsonify({
        "message": "ACEest Fitness & Gym API",
        "status": "running",
        "version": "1.0"
    })


@app.route("/programs")
def get_programs():
    """Return list of available fitness programs."""
    return jsonify({"programs": list(PROGRAMS.keys())})


@app.route("/programs/<program_name>")
def get_program_detail(program_name):
    """Return workout and diet details for a specific program."""
    if program_name not in PROGRAMS:
        return jsonify({"error": "Program not found"}), 404
    return jsonify({"program": program_name, "details": PROGRAMS[program_name]})


@app.route("/calculate", methods=["POST"])
def calculate_calories():
    """
    Calculate estimated daily calories.
    Expects JSON: { "program": "Fat Loss (FL)", "weight": 70 }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    program = data.get("program")
    weight = data.get("weight")

    if not program:
        return jsonify({"error": "program is required"}), 400
    if program not in PROGRAMS:
        return jsonify({"error": f"Invalid program. Choose from: {list(PROGRAMS.keys())}"}), 400
    if weight is None:
        return jsonify({"error": "weight is required"}), 400

    try:
        weight = float(weight)
    except (ValueError, TypeError):
        return jsonify({"error": "weight must be a number"}), 400

    if weight <= 0:
        return jsonify({"error": "weight must be greater than 0"}), 400

    factor = PROGRAMS[program]["calorie_factor"]
    calories = int(weight * factor)

    return jsonify({
        "program": program,
        "weight_kg": weight,
        "estimated_calories": calories,
        "calorie_factor": factor
    })


@app.route("/clients", methods=["POST"])
def add_client():
    """
    Register a new client.
    Expects JSON: { "name": "Arjun", "age": 25, "weight": 72, "program": "Fat Loss (FL)" }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    name = data.get("name")
    age = data.get("age")
    weight = data.get("weight")
    program = data.get("program")

    if not name or not program:
        return jsonify({"error": "name and program are required"}), 400
    if program not in PROGRAMS:
        return jsonify({"error": "Invalid program"}), 400

    try:
        weight = float(weight) if weight else 0
        age = int(age) if age else 0
    except (ValueError, TypeError):
        return jsonify({"error": "age and weight must be numbers"}), 400

    calories = int(weight * PROGRAMS[program]["calorie_factor"]) if weight > 0 else 0

    client = {
        "name": name,
        "age": age,
        "weight_kg": weight,
        "program": program,
        "estimated_calories": calories
    }

    return jsonify({"message": "Client registered successfully", "client": client}), 201


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
