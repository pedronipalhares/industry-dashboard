# Industry Dashboard

A comprehensive Streamlit web application that provides interactive visualizations and analysis of various industry-related datasets. The app presents data across multiple categories with interactive charts and filters.

## Features

- 📊 Clean and intuitive user interface
- 📈 Interactive data visualizations using Steamlit
- 🔍 Filterable data views
- 📑 Multiple industry categories (Beef, Chicken, Beverages, etc.)
- 🌍 Country-specific data analysis
- 🔄 Real-time data updates
- 📱 Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pedronipalhares/industry-dashboard.git
cd industry-dashboard
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. The app will open in your default web browser at `http://localhost:8501`

3. Navigate through the different pages using the sidebar
4. Explore interactive visualizations for each industry category
5. Use filters to focus on specific time periods or regions

## Project Structure

```
industry-dashboard/
├── app.py                # Main Streamlit application
├── pages/                # Streamlit pages
│   ├── 1_Home.py         # Home page
│   ├── 2_Beef.py         # Beef industry analysis
│   ├── 3_Chicken.py      # Chicken industry analysis
│   ├── 4_Sugar.py        # Sugar industry analysis
│   ├── 5_Beverages.py    # Beverages industry analysis
│   └── ...               # Other industry pages
├── datasets/             # Dataset storage directory
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Available Industry Categories

The application provides analysis for various industry categories, including:
- Beef (prices, cattle herd, costs)
- Chicken (prices, broiler costs, feed costs)
- Sugar (prices, production, exports)
- Beverages (capacity utilization, prices)
- And more...

Each category includes country-specific data with interactive visualizations.

## Data Sources

All datasets are sourced from reliable public APIs and databases, ensuring data accuracy and reliability. The data is regularly updated to provide the most current information.

## Requirements

- Python 3.9 or higher
- Streamlit 1.32.0
- Pandas 2.2.1
- Plotly 5.18.0

## Contributing

Feel free to submit issues and enhancement requests! 

## License

This project is licensed under the MIT License - see the LICENSE file for details. 