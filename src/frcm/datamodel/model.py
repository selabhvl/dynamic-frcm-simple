from pathlib import Path
import datetime

from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float


class WeatherDataPoint(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    timestamp: datetime.datetime

    @classmethod
    def csv_header(cls) -> str:
        return "timestamp,temperature,humidity,wind_speed"

    def csv_line(self) -> str:
        return f"{self.timestamp.isoformat()},{self.temperature},{self.humidity},{self.wind_speed}"


class Observations(BaseModel):
    # source: str
    # location: Location
    data: list[WeatherDataPoint]


    def write_csv(self, target: Path):
        handle = open(target, "w+")
        handle.write(WeatherDataPoint.csv_header())
        handle.write('\n')
        for d in self.data:
            handle.write(d.csv_line())
            handle.write('\n')
        handle.close()


class Forecast(BaseModel):

    # location: Location
    data: list[WeatherDataPoint]

    def __str__(self):
        format_str = f'Forecast @ Location: {self.location}\n'

        # Join all data points using '\n' as a separator
        data_strings = '\n'.join(map(str, self.data))

        return format_str + data_strings + '\n'


class WeatherData(BaseModel):
    # created: datetime.datetime
    observations: Observations
    forecast: Forecast

    def to_json(self):
        return self.model_dump_json()

    def write_csv(self, target: Path):
        handle = open(target, "w+")
        handle.write(WeatherDataPoint.csv_header())
        handle.write('\n')
        for d in self.observations.data:
            handle.write(d.csv_line())
            handle.write('\n')
        for d in self.forecast.data:
            handle.write(d.csv_line())
            handle.write('\n')
        handle.close()



class FireRisk(BaseModel):
    timestamp: datetime.datetime
    ttf: float

    @classmethod
    def csv_header(cls) -> str:
        return "timestamp,ttf"

    def csv_line(self) -> str:
        return f"{self.timestamp.isoformat()},{self.ttf}"



class FireRiskPrediction(BaseModel):
    # location: Location
    firerisks: list[FireRisk]

    def __str__(self) -> str:
        return "\n".join([FireRisk.csv_header()] + [r.csv_line() for r in self.firerisks])

    def write_csv(self, target: Path):
        handle = open(target, "w+")
        handle.write(FireRisk.csv_header())
        handle.write('\n')
        for r in self.firerisks:
            handle.write(r.csv_line())
            handle.write('\n')
        handle.close()

