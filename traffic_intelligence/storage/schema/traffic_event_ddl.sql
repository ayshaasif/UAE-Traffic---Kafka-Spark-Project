CREATE TABLE IF NOT EXISTS traffic_events (

    id SERIAL PRIMARY KEY,

    road_id VARCHAR(50),
    road_name VARCHAR(255),

    current_speed FLOAT,
    free_flow_speed FLOAT,

    congestion_index FLOAT,

    event_time TIMESTAMP,

    raw_event JSONB
);

