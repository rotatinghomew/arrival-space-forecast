from datetime import datetime


def parse_time(value):
    return datetime.fromisoformat(value)


def summarize(release):
    tables = release["tables"]
    cutoff = release["cutoff"]
    visible = [row for row in tables['occupancy'] if row['known_at'] <= cutoff]
    latest = {}
    for row in sorted(visible, key=lambda row: (row['event_at'], row['known_at'])):
        latest[row['site']] = row
    return {'sites': {site: {'free': row['capacity']-row['occupied'], 'event_at': row['event_at']} for site, row in latest.items()}, 'visible_records': len(visible), 'late_records': len(tables['occupancy'])-len(visible)}
