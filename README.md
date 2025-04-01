# MLB Pitcher Analysis

A Python script to analyze MLB pitcher data using the PyBaseball library. This script creates visualizations for:
- Pitch usage evolution over time
- Pitch velocity trends
- Spin rate trends

## Setup

1. Clone the repository:
```bash
git clone https://github.com/adaminnyc/pybaseball-pitching-trends.git
cd pybaseball-pitching-trends
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

If using venv follow these steps.

Clone the repository:
```bash
git clone https://github.com/adaminnyc/pybaseball-pitching-trends.git
cd pybaseball-pitching-trends
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Usage ##

Run the script with:
```bash
python app.py
```

The script will prompt for a pitcher's name and season and will then generate three plots showing different aspects of the pitcher's performance during the 2024 MLB season:
1. A line plot showing the evolution of pitch type usage by month
2. A line plot showing pitch velocity trends
3. A line plot showing spin rate trends

## Data Source
Data is fetched using the PyBaseball library, which sources its data from Baseball Savant.