from pathlib import Path
import sys
import datetime
from frcm.weatherdata.client_met import METClient
from frcm.weatherdata.extractor_met import METExtractor
from frcm.datamodel.model import Location, WeatherData

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments provided! Please provide one reference to a CSV file with weatherdata to compute the fire risk")
        sys.exit(1)
    file = Path(sys.argv[1])
    print("Computing fire risk...")
    location = Location(latitude=60.383, longitude=5.3327)  # Bergen
    obs_delta = datetime.timedelta(days=2)
    time_now = datetime.datetime.now()
    start_time = time_now - obs_delta
    met_extractor = METExtractor()
    met_client = METClient(extractor=met_extractor)
    observations = met_client.fetch_observations(location, start=start_time, end=time_now)
    forecast = met_client.fetch_forecast(location)
    wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
    wd.write_csv(file)

