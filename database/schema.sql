USE weather_monitoring;

CREATE TABLE weather_station (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    installation_date DATE,
    status ENUM('Active','Inactive') DEFAULT 'Active'
);

CREATE TABLE weather_data (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT,
    timestamp DATETIME,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    wind_speed FLOAT,
    wind_direction FLOAT,
    rainfall FLOAT,
    solar_radiation FLOAT,
    is_anomaly TINYINT DEFAULT 0,
    anomaly_prediction TINYINT,
    disaster_risk VARCHAR(40),

    FOREIGN KEY (station_id)
    REFERENCES weather_station(station_id)
);
