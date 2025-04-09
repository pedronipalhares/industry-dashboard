# Industry Dashboard Dataset Downloader

A Streamlit web application that provides easy access to download various industry-related datasets. The app presents all available datasets in a clean, tabular format with individual download buttons for each dataset.

## Features

- 📊 Clean and intuitive user interface
- 📑 Table view of all available datasets
- ⚡ Quick download buttons for each dataset
- 🔍 Alphabetically sorted dataset list
- �� Responsive design
- 📈 Interactive data visualizations using Plotly
- 🔄 Real-time data updates

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

3. Browse through the available datasets in the table
4. Click the download button next to any dataset to download it as a CSV file
5. Explore interactive visualizations for each dataset

## Project Structure

```
industry-dashboard/
├── app.py              # Main Streamlit application
├── data/               # Dataset storage directory
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Available Datasets

The application provides access to various industry-related datasets, including:
- Agricultural commodity prices
- Currency exchange rates
- Economic indicators
- Production data
- Market prices
- And more...

All datasets are sourced from reliable public APIs and databases, ensuring data accuracy and reliability.

## Requirements

- Python 3.9 or higher
- Streamlit 1.32.0
- Pandas 2.2.1
- Plotly 5.18.0

## Contributing

Feel free to submit issues and enhancement requests! 

## License

This project is licensed under the MIT License - see the LICENSE file for details. 