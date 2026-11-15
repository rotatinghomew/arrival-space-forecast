from datetime import datetime


def parse_time(value):
    return datetime.fromisoformat(value)


def operate(path, payload, release):
    if path != '/v1/asof':
        raise LookupError('时点接口不存在')
    at=payload['at']
    return {'occupancy':[row for row in release['tables']['occupancy'] if row['known_at']<=at], 'closures':[row for row in release['tables']['closures'] if row['known_at']<=at], 'revision':release['revision']}
