from datetime import datetime, timezone


def transform_traffic(raw_data, road):
    flow = raw_data["flowSegmentData"]

    current_speed = flow["currentSpeed"]
    free_flow_speed = flow["freeFlowSpeed"]

    congestion_index = (
        1 - (current_speed / free_flow_speed)
        if free_flow_speed > 0 else None
    )

    return {
        "road_id": road["id"],
        "road_name": road["name"],
        "lat": road["lat"],
        "lon": road["lon"],

        "event_time": datetime.now(timezone.utc).isoformat(),

        "current_speed": current_speed,
        "free_flow_speed": free_flow_speed,
        "current_travel_time": flow["currentTravelTime"],
        "free_flow_travel_time": flow["freeFlowTravelTime"],

        "confidence": flow.get("confidence", None),

        "congestion_index": round(congestion_index, 3)
        if congestion_index is not None else None,

        # raw preserved (VERY IMPORTANT in real systems)
        "raw": raw_data
    }
