# 🧠 Rubik’s Cube Solver – AI + Flask Web App

![banner](https://raw.githubusercontent.com/AnaghaMahajan2004/rubiks-cube-solver/main/screenshots/banner.png)

This is an AI-powered web application that captures a real Rubik’s Cube using your camera or image upload, predicts its color configuration using a trained CNN model, computes the optimal solution using the Kociemba algorithm, and then shows a beautiful 3D animated solution step-by-step using twisty-player.

> ✅ Built using **Flask, OpenCV, TensorFlow, and cubing.js**  
> ✅ Created as part of my **AI/ML Internship Application**

---

## 🔍 What It Does

- 📸 **Takes input images** of cube faces (via upload form)
- 🧠 **CNN model** classifies color of each facelet (image classification)
- 📦 **Generates cube string** from all six faces
- 🧮 **Uses Kociemba algorithm** to compute the shortest solving sequence
- 🧊 **Visualizes the cube in 3D** using [twisty-player](https://cubing.js.org)
- ➡️ **Click “Next”** to go through each move one-by-one

---

## 📸 Demo Screenshots

| Uploading Faces | 3x3 Cube Solving (Step-by-step) |
|-----------------|----------------------------------|
| ![upload](https://raw.githubusercontent.com/yourusername/rubiks-cube-solver/main/screenshots/upload.png) | ![solve](https://raw.githubusercontent.com/yourusername/rubiks-cube-solver/main/screenshots/solve.gif) |

---

## 💡 How It Works (Simplified Flow)
📷 Image Upload
⬇️
🎯 OpenCV Preprocessing
⬇️
🧠 CNN Color Classifier (Keras)
⬇️
🧩 Valid Cube String Construction
⬇️
🤖 Kociemba Algorithm (Python Lib)
⬇️
🧊 3D Cube + Step-by-Step Animation (cubing.js)



---

## 🧰 Tech Stack

| Part | Technology |
|------|------------|
| Backend | Python, Flask |
| ML | TensorFlow (CNN), OpenCV |
| Cube Solving | Kociemba Solver |
| Frontend | HTML, CSS, JS, twisty-player (cubing.js) |
| Deployment-ready | GitHub + Flask |
| Future Stack | YOLOv8, Thistlethwaite, Korf, React, Three.js |

---

## 🚀 Future Enhancements

- ✅ Support for **2x2, 4x4, 5x5** cubes
- ✅ Add **pyraminx**, **megaminx** solving
- ✅ Convert frontend to **React + Three.js**
- ✅ Use **YOLOv8** to detect cube faces from live webcam
- ✅ Add auto-play, previous button, downloadable GIFs of solving

---

## 📦 Requirements

To run this project locally:

```bash
git clone https://github.com/yourusername/rubiks-cube-solver.git
cd rubiks-cube-solver
python -m venv venv
venv\Scripts\activate      # use `source venv/bin/activate` on Linux/Mac
pip install -r requirements.txt
python app.py


---

## 📝 What to Replace

| Placeholder | Replace with |
|------------|--------------|
| `yourusername` | Your actual GitHub username |
| `Your Name` | Your full name |
| `Your College Name` | Your college’s name |
| `upload.png` / `solve.gif` | Your screenshots (placed in `screenshots/` folder) |
| `your-profile` | Your LinkedIn profile URL |

---



