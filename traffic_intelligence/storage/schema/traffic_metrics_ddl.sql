CREATE TABLE traffic_metrics (
    id SERIAL PRIMARY KEY,
    road_id TEXT,
    road_name TEXT,
    avg_speed FLOAT,
    avg_congestion FLOAT,
    event_count INT,
    metric_time TIMESTAMP
);