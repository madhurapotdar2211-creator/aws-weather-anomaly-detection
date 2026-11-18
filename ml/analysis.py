"""Automated exploratory chart generation."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from config.config import CHARTS_PATH

class WeatherAnalysis:
    """Generate the required PNG charts from an engineered DataFrame."""
    def __init__(self, dataframe=None, input_file=None, output_dir=None):
        self.df = dataframe
        self.input_file = input_file
        self.output_dir = Path(output_dir or CHARTS_PATH)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_dataset(self):
        """Load and normalize the analysis input when needed."""
        if self.df is None:
            if self.input_file is None:
                raise ValueError("A DataFrame or input workbook is required.")
            self.df = pd.read_excel(self.input_file, engine="openpyxl")
        self.df = self.df.copy()
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        return self.df

    def _save(self, filename, title, plotter):
        """Render one chart and save it as a high-resolution PNG."""
        fig, axis = plt.subplots(figsize=(9, 5))
        plotter(axis)
        axis.set_title(title)
        fig.tight_layout()
        path = self.output_dir / filename
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def generate_charts(self):
        """Create and return all required analysis chart paths."""
        frame = self.load_dataset()
        paths = []
        for column, label in [("temperature", "Temperature"), ("humidity", "Humidity"), ("pressure", "Pressure"), ("rainfall", "Rainfall")]:
            paths.append(self._save(f"{column}_histogram.png", f"{label} Distribution", lambda ax, c=column, l=label: ax.hist(frame[c].dropna(), bins=30, color="#2563eb", alpha=.8) or ax.set_xlabel(l)))
        def station(ax):
            for station, group in frame.groupby("station_id"):
                ax.plot(group.timestamp, group.temperature, label=str(station))
            ax.legend(loc="best", fontsize=7)
            ax.set_xlabel("Timestamp")
            ax.set_ylabel("Temperature")
        paths.append(self._save("station_wise_graph.png", "Station-wise Temperature", station))
        paths.append(self._save("anomaly_distribution.png", "Anomaly Distribution", lambda ax: frame["is_anomaly"].value_counts().sort_index().plot.bar(ax=ax, color=["#16a34a", "#dc2626"])))
        def correlation(ax):
            matrix = frame.select_dtypes("number").corr()
            image = ax.imshow(matrix, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=90)
            ax.set_yticks(range(len(matrix.columns)), matrix.columns)
            plt.colorbar(image, ax=ax)
        paths.append(self._save("correlation_matrix.png", "Correlation Matrix", correlation))
        monthly = frame.set_index("timestamp").resample("MS")[["temperature", "humidity", "pressure", "rainfall"]].mean()
        paths.append(self._save("monthly_weather_trend.png", "Monthly Weather Trend", lambda ax: monthly.plot(ax=ax)))
        trend = frame.sort_values("timestamp").set_index("timestamp")[["temperature", "humidity", "pressure"]].rolling(24, min_periods=1).mean()
        paths.append(self._save("sensor_trend.png", "Rolling Sensor Trend", lambda ax: trend.plot(ax=ax)))
        return paths
