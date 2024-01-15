# api-sports-io-nfl
An unofficial Python API wrapper for [api-sports.io's NFL feeds](https://api-sports.io/documentation/nfl/v1).

## Installation
```bash
pip install api-sports-io-nfl
```

## Usage
```python
from api_sports_io_nfl import ApiNfl

# Initialize the API wrapper with your API key
api = ApiNfl(api_key='YOUR_API_KEY')

# Make your calls!
teams = api.teams(league=api.Leagues.NFL)
```
