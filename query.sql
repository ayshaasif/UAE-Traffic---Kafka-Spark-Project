SELECT road_id, road_name, current_speed, free_flow_speed, congestion_index, event_time FROM traffic_events WHERE road_id = 'szr_downtown' ORDER BY event_time DESC  LIMIT 100;


SELECT * FROM traffic_metrics WHERE road_id = 'szr_downtown' ORDER BY metric_time DESC LIMIT 100;