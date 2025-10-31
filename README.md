# ⚔️ Turn-Based Combat Simulator  
*A Python RPG combat engine for tactical battles and status effect tracking.*

--
## 🧠 Overview

**Turn-Based Combat Simulator** is a **Python-powered battle engine** that lets you simulate RPG-style combat between multiple characters — each with unique stats, weapons, and special abilities.

It features:
- 🎯 Dynamic damage and hit rolls  
- 💥 Status effects like *Bleed*, *Crack*, and *Disarm*  
- 🛡️ Armour-based HP scaling  
- 🎮 A simple text-driven interface  

---

## 🗂️ Project Structure

combat_simulator/
│
├── main.py # Main game loop and logic
├── weapons.json # Weapon definitions and stats
├── characters.json # Character data and attributes
└── README.md # Project documentation

## ⚙️ Features

✅ **Character System**  
- Custom character creation via JSON  
- Automatic HP adjustment based on armour type  
- Supports dual weapons  

✅ **Weapon System**  
- Loadable weapons with different hit chances and effects  
- Defines attack dice, ability type, and effect duration  

✅ **Effect Engine**  
- Bleed, Crack, Disarm, Impale, and Disorient  
- Automatic round-by-round duration tracking  

✅ **CLI Interface**  
- Player-guided combat simulation  
- Input validation for rolls and damage  
- Dynamic status updates every round  

---
🕹️ How to Run
1️⃣ Clone the repository
git clone https://github.com/<your-username>/combat-simulator.git
cd combat-simulator

2️⃣ Ensure Python 3 is installed
python --version

3️⃣ Run the program
python main.py

4️⃣ Play the game

Follow the prompts:

Choose an attacker

Pick weapon 1 or 2

Roll a d20, enter damage, and an effect roll

Watch effects and HP auto-update each round

🩸 Combat Effects
🧩 Effect	💥 Description
Bleed	Loses 1 HP per round for a set duration.
Disorient	Target becomes disadvantaged.
Crack	Takes bonus damage based on armour and last hit.
Impale	Target cannot move until the effect ends.
Disarm	Prevents weapon use temporarily.

🧮 Armour Bonuses
Armour Type	HP Bonus
🩻 Light Armour	+10% HP
🛡️ Medium Armour	+25% HP
🪓 Heavy Armour	+50% HP

🌱 Future Roadmap

🎲 Add critical hit mechanics
💾 Save/load combat states
🧭 Add AI-controlled characters
🖥️ Optional GUI or web dashboard
🔮 More status effects and dice automation

📜 License

This project is licensed under the MIT License.
You’re free to use, modify, and share it with credit.

👨‍💻 Author

Joshua de Klerk
📍 South Africa
💾 GitHub: https://github.com/J-DeKlerk


⭐ If you enjoy this project, consider giving it a star on GitHub!
