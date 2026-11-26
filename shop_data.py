from pathlib import Path

import pandas as pd


DATA = Path("data")


def read_orders():
    months = sorted(DATA.glob("orders_2024_*.csv"))
    return pd.concat(
        [pd.read_csv(path, parse_dates=["order_datetime"]) for path in months],
        ignore_index=True,
    )


def read_events():
    columns = ["event_id", "user_id", "event_time", "event_type", "page"]
    records = pd.read_json(DATA / "events_records.json", convert_dates=False)
    # В первом файле каждое из пяти полей записано отдельной строкой.
    records = records.T.set_axis(columns, axis="columns")
    lines = pd.read_json(DATA / "events_lines.json", lines=True, convert_dates=False)
    events = pd.concat([records, lines], ignore_index=True)
    events = events.astype({"event_id": "int64", "user_id": "int64"})
    events["event_time"] = pd.to_datetime(events["event_time"])
    return events
