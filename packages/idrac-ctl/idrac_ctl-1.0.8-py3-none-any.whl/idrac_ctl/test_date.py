import json
from datetime import datetime


def validate_future_job(start_date: str, start_time: str):
    """Validate future job time
   :param start_date: start date for a job YYYY-MM-DD
   :param start_time: a start time for a job HH:MM:SS
   :raise: MissingMandatoryArguments if mandatory args missing.
   """
    if start_date is None or len(start_date) == 0:
        raise ValueError(
            "A maintenance job requires a start date.")
    if start_time is None or len(start_time) == 0:
        raise ValueError(
            "A maintenance job requires a start time.")
    try:
        local_timestamp = datetime.now()
        ts = f'{start_date}T{start_time}.000001'
        start_timestamp = datetime.fromisoformat(ts)
        if start_timestamp < local_timestamp:
            raise ValueError(f"Start time is in the past local time "
                             f"{str(local_timestamp)} {str(start_timestamp)}")
        return json.dumps(start_timestamp.isoformat())
    except ValueError as ve:
        print(f"Error: {str(ve)}")
    except TypeError as te:
        print(f"Error: {str(te)}")


ts = validate_future_job("2023-02-08", "01:01:01")
print(ts)