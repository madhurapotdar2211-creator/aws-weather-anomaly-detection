"""PDF report generation from pipeline outputs and saved charts."""
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from config.config import CHARTS_PATH, REPORT_PATH

class ReportService:
    """Build a self-contained PDF summary for portfolio and operational use."""
    def generate(self, dataframe, anomaly_result=None, risk_result=None):
        """Generate dataset summary, model metrics, predictions, charts, and timestamp."""
        target = REPORT_PATH / f"weather_report_{datetime.now():%Y%m%d_%H%M%S}.pdf"
        with PdfPages(target) as pdf:
            figure = plt.figure(figsize=(8.27, 11.69))
            figure.text(.08, .95, "AWS Weather Anomaly & Disaster Risk Report", fontsize=18, weight="bold")
            anomaly_count = int(dataframe["is_anomaly"].sum()) if "is_anomaly" in dataframe else 0
            summary = [
                f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}",
                f"Rows analysed: {len(dataframe):,}",
                f"Stations: {dataframe.station_id.nunique():,}",
                f"Date range: {dataframe.timestamp.min()} to {dataframe.timestamp.max()}",
                f"Source anomalies: {anomaly_count:,}",
                f"Best anomaly model: {(anomaly_result or {}).get('best_model', 'Not trained')}",
                f"Best risk model: {(risk_result or {}).get('best_model', 'Not trained')}",
            ]
            figure.text(.08, .87, "\n".join(summary), fontsize=11, va="top")
            pdf.savefig(figure, bbox_inches="tight")
            plt.close(figure)
            for result, title in ((anomaly_result, "Anomaly model metrics"), (risk_result, "Disaster risk model metrics")):
                if result is None or "metrics" not in result:
                    continue
                figure, axis = plt.subplots(figsize=(11, 6))
                axis.axis("off")
                axis.set_title(title)
                visible = result["metrics"].drop(columns=["confusion_matrix"], errors="ignore")
                table = axis.table(cellText=visible.round(4).astype(str).values, colLabels=visible.columns, loc="center")
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 1.6)
                pdf.savefig(figure, bbox_inches="tight")
                plt.close(figure)
            for chart in sorted(CHARTS_PATH.glob("*.png")):
                figure, axis = plt.subplots(figsize=(11, 7))
                axis.imshow(plt.imread(chart))
                axis.axis("off")
                axis.set_title(chart.stem.replace("_", " ").title())
                pdf.savefig(figure, bbox_inches="tight")
                plt.close(figure)
        return target
