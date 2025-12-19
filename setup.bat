@echo off
echo ================================
echo 🚀 Setting up Streamlit App
echo ================================

REM ---- 1. Create virtual environment if not exists ----
if not exist env (
    echo 📦 Creating virtual environment...
    python -m venv env
) else (
    echo ✅ Virtual environment already exists
)

REM ---- 2. Activate virtual environment ----
call env\Scripts\activate

REM ---- 3. Upgrade pip ----
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM ---- 4. Install required packages ----
echo 📥 Installing dependencies...
pip install streamlit pandas pyarrow

REM ---- 5. Run Streamlit app ----
echo ▶️ Starting Streamlit app...
streamlit run polapp.py

pause
