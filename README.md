<p align="center">
<img width="150" height="150" alt="Lovely Sim Racing" src="docs/images/lr-logo-small.png">
</p>

<h1 align="center">Lovely Track Data</h1>

<p align="center">
A comprehensive list of Track Data for Sim Racing games.
</p>

---

## How to
Fetch the data by retrieving the url:
`/data/{simId}/{trackId}.json`

## File Format
Every file is formatted as follows:

``` 
# name        - The full human readable track name
# turn        - An array of all the Turn data
  # name      - Turn Name
  # marker    - The percentage point of the Apex
  # start     - OPTIONAL The percentage point turn start
  # end       - OPTIONAL The percentage point turn end
# sector      - An array of all the track Sectors
  # name      - The name of the Sector
  # marker    - The percentage point of the Sector
# time        - OPTIONAL An array of estimated time delays
  # class     - The car class (sim dependant)
    # name    - Name of the time delay
    # time    - Time delay in seconds
```

### Example 
```JSON
{
  "name": "Barcelona",
  "turn": [
    {"name": "Elf", "marker": 0.185, "start": 0.155, "end": 0.220},
    {"name": 2, "marker": 0.209},
    {"name": "Renault", "marker": 0.281, "start": 0.230, "end": 0.320},
    {"name": "Repsol", "marker": 0.377, "start": 0.355, "end": 0.420},
    {"name": "Seat", "marker": 0.461, "start": 0.440, "end": 0.478},
    {"name": 6, "marker": 0.518},
    {"name": "Würth", "marker": 0.556, "start": 0.535, "end": 0.583},
    {"name": 8, "apex": 0.577},
    {"name": "Campsa", "marker": 0.633, "start": 0.600, "end": 0.655},
    {"name": "La Caixa", "marker": 0.758, "start": 0.725, "end": 0.770},
    {"name": 11, "marker": 0.785},
    {"name": "Banc Sabadell", "marker": 0.819, "start": 0.795, "end": 0.840},
    {"name": "Europcar", "marker": 0.869, "start": 0.850, "end": 0.875},
    {"name": 14, "marker": 0.895},
    {"name": "Chicane RACC", "marker": 0.908, "start": 0.885, "end": 0.908},
    {"name": "New Holland", "marker": 0.944, "start": 0.915, "end": 0.960}
  ],
  "sector": [
    {"name": 1, "marker": 0.350},
    {"name": 2, "marker": 0.733},
    {"name": 3, "marker": 1}
  ],
  "time": [
    { "gt3": [
      {"name": "sg30", "time": 77},
      {"name": "dt", "time": 42}
    ]}
  ]
}
```

### Contributing
