from datetime import datetime, timezone



print(datetime.fromtimestamp(int("1674939324"), timezone.utc).isoformat(sep=' '))