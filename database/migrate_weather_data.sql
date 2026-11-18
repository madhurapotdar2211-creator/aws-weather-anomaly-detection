USE weather_monitoring;

ALTER TABLE weather_data
    ADD COLUMN is_anomaly TINYINT NOT NULL DEFAULT 0,
    ADD COLUMN anomaly_prediction TINYINT NULL,
    ADD COLUMN disaster_risk VARCHAR(40) NULL;
