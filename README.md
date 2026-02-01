# 🏠 Airbnb Analytics Dashboard

A premium, enterprise-grade analytics platform for Airbnb data visualization, built with Streamlit and Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Stunning Dark Theme**: "Airbnb Luxe Dark" with glassmorphism effects and gradient accents
- **12 Unique Visualizations**: 6 guest-focused + 6 host-focused charts
- **Interactive Filtering**: Real-time updates across all charts
- **Responsive Design**: 2-column grid layout with animated transitions
- **Data Export**: Download filtered data as CSV
- **Docker Ready**: One-command deployment

## 📊 Dashboard Views

### 🛫 Guest View
| Chart | Description |
|-------|-------------|
| Radar Chart | Top 5 cities comparison across 6 metrics |
| Contour Plot | Price vs Rating correlation density |
| Circular Gauge | Overall satisfaction score (0-100%) |
| Stacked Area | Booking trends by room type over time |
| Violin Plot | Price distribution by region |
| Geographic Map | Global city distribution with pricing |

### 🏠 Host View
| Chart | Description |
|-------|-------------|
| Nightingale Rose | Revenue breakdown by region |
| Hexbin Plot | Reviews vs Sales correlation |
| Treemap | Revenue hierarchy (Area > City > Room Type) |
| Bump Chart | City rankings over time periods |
| Radial Histogram | Sales distribution (days/year) |
| Network Graph | Multi-city host connections |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Airbnb dataset CSV file

### Setup

1. **Clone/Download the project**
   ```bash
   cd "Air Bnb"
   ```

2. **Place your data file**
   ```bash
   # Ensure the CSV is in the data folder:
   data/Airbnb_site_hotel_new.csv
   ```

3. **Build and run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Open the dashboard**
   ```
   http://localhost:8501
   ```

## 🐳 Docker Commands

```bash
# Build and start the dashboard
docker-compose up --build

# Run in background (detached mode)
docker-compose up -d

# Stop the dashboard
docker-compose down

# View logs
docker-compose logs -f

# Rebuild without cache
docker-compose build --no-cache

# Restart the service
docker-compose restart
```

## 📁 Project Structure

```
Air Bnb/
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
├── data/
│   └── Airbnb_site_hotel_new.csv  # Dataset (place here)
├── utils/
│   ├── __init__.py
│   └── data_processor.py   # Data cleaning utilities
├── dashboard.py            # Main Streamlit application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore          # Docker ignore patterns
└── README.md              # This file
```

## 📑 Dataset Requirements

### Expected Columns (23 total)
| Column | Type | Description |
|--------|------|-------------|
| id | int | Listing ID |
| name | str | Listing name |
| host_id | int | Host identifier |
| host_name | str | Host name |
| city | str | City name (11 cities) |
| price | str | Price (may have commas) |
| reply time | int | Host reply time |
| guest favourite | int | Guest favourite flag (0/1) |
| host since | int | Days since host registration |
| host Certification | int | Certification status (0/1) |
| room_type | int | Room type code (1-4) |
| host total listings count | int | Total host listings |
| consumer | str | Rating (European format, e.g., "6,81") |
| total reviewers number | int | Review count |
| accommodates | int | Guest capacity |
| bathrooms | str | Bathroom count (European format) |
| bedrooms | int | Bedroom count |
| beds | int | Bed count |
| listing number | int | Listing number |
| host response rate | str | Response rate (European format) |
| host acceptance rate | str | Acceptance rate (European format) |
| sales | int | Sales days (0-365) |
| area | str | Region (North America, Europe, Asia) |

### Data Cleaning Applied
- Price: String → Float (removes formatting)
- Bathrooms: European decimal ("1,5" → 1.5)
- Consumer rating: European decimal ("6,81" → 6.81)
- Response/Acceptance rates: European decimal → Float
- Room types: Integer → Decoded string
- Revenue estimate: Calculated (price × sales)

## 🎨 Theme Configuration

The dashboard uses a custom "Airbnb Luxe Dark" theme:

| Element | Color |
|---------|-------|
| Background | Deep navy #0f172a → #1e293b |
| Cards | Slate #1e293b (glassmorphism) |
| Guest Accent | Teal #06b6d4 |
| Host Accent | Coral #f97316 |
| Highlights | Purple #a855f7 |
| Text | White #f8fafc / Gray #cbd5e1 |

## 🔧 Configuration

### Streamlit Config (`.streamlit/config.toml`)
```toml
[theme]
primaryColor = "#06b6d4"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#f8fafc"

[server]
port = 8501
address = "0.0.0.0"
```

### Environment Variables
- `PYTHONUNBUFFERED=1` - For real-time logging

## 🛠️ Development

### Local Development (without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard.py
```

### Hot Reload
The Docker setup includes volume mounts for hot-reload during development:
- `./dashboard.py` → `/app/dashboard.py`
- `./utils/` → `/app/utils/`
- `./data/` → `/app/data/`

## 📈 Performance

- Uses `@st.cache_data` for data loading
- Efficient data filtering with pandas
- Optimized chart rendering with Plotly

## 🔒 Health Check

The Docker container includes a health check:
```bash
curl --fail http://localhost:8501/_stcore/health
```

## 🐛 Troubleshooting

### Dashboard not loading
1. Check if data file exists: `data/Airbnb_site_hotel_new.csv`
2. Verify Docker is running: `docker ps`
3. Check logs: `docker-compose logs -f`

### Port already in use
```bash
# Kill process on port 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
ports:
  - "8502:8501"
```

### Data not loading
- Ensure CSV encoding is UTF-8
- Check column names match expected format
- Verify data types are correct

## 📜 License

MIT License - Feel free to use and modify.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

Built with ❤️ using Streamlit, Plotly, and Docker
