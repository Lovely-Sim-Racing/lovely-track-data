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

* `{simId}` is the lowercase Simhub game id `DataCorePlugin.CurrentGame`
* `{trackId}` is the lowercase Simhub track id `DataCorePlugin.TrackId`

## File Format
Every file is formatted as follows:

``` 
# name          (String) - The full human readable track name
# country       (String) - (OPTIONAL) The track's country code (ISO 3166 Alpha 2)
# length        (Int)    - (OPTIONAL) Length of the track in meters
# year          (Int)    - (OPTIONAL) The track's active year
# turn                   - An array of all the Turn data
  # number      (Int)    - Turn Number
  # name        (String) - Turn Name
  # marker      (Int)    - The percentage point of the Apex
  # scale       (Int)    - (OPTIONAL) 1-6: Turn (Hairpin > Wide)
  # direction   (Int)    - (OPTIONAL) 0: Left, 1: Right
  # start       (Int)    - (OPTIONAL) The percentage point segment start
  # end         (Int)    - (OPTIONAL) The percentage point segment end
  # extra                - (OPTIONAL) An array of properties
    # keys      (?)      - Key:Value
# straight               - An array of all the Straight data
  # number      (Int)    - Straight Number
  # name        (String) - Straight Name
  # start       (Int)    - (OPTIONAL) The percentage point segment start
  # end         (Int)    - (OPTIONAL) The percentage point segment end
  # extra                - (OPTIONAL) An array of properties
    # keys      (?)      - Key:Value
# sector                 - An array of all the Sector data
  # number      (Int)    - Sector Number
  # name        (String) - Sector Name
  # marker      (Int)    - The percentage point of the Sector
  # extra                - (OPTIONAL) An array of properties
    # keys      (?)      - Key:Value
# time                   - (OPTIONAL) An array of estimated time delays
  # class       (String) - The car class (sim dependant)
    # name      (String) - Name of the time delay
    # time      (Int)    - Time delay in seconds
# extra                  - (OPTIONAL) An array of properties
  # keys        (?)      - Key:Value
```

### Example for `silverstone.json`

#### Simple Track Data Example
```JSON
{
  "name": "Silverstone",
  "turn": [
    { "number": 1, "name": "T1", "marker": 0.042 },
    { "number": 2, "name": "T2", "marker": 0.133 },
    { "number": 3, "name": "T3", "marker": 0.151 },
    { "number": 4, "name": "T4", "marker": 0.176 },
    { "number": 5, "name": "T5", "marker": 0.201 },
    { "number": 6, "name": "T6", "marker": 0.229 },
    { "number": 7, "name": "T7", "marker": 0.377 },
    { "number": 8, "name": "T8", "marker": 0.432 },
    { "number": 9, "name": "T9", "marker": 0.469 },
    { "number": 10, "name": "T10", "marker": 0.499 },
    { "number": 11, "name": "T11", "marker": 0.594 },
    { "number": 12, "name": "T12", "marker": 0.628 },
    { "number": 13, "name": "T13", "marker": 0.672 },
    { "number": 14, "name": "T14", "marker": 0.696 },
    { "number": 15, "name": "T15", "marker": 0.731 },
    { "number": 16, "name": "T16", "marker": 0.858 },
    { "number": 17, "name": "T17", "marker": 0.887 },
    { "number": 18, "name": "T18", "marker": 0.949}
number  ],
  "straight": [
    { "number": 1, "name": "Hangar Straight", "start": 0.235, "end": 0.355 },
    { "number": 2, "name": "Hamilton Straight", "start": 0.515, "end": 0.560},
    { "number": 3, "name": "Wellington Straight", "start": 0.760, "end": 0.810}
  ],
  "sector": [
    { "number": 1, "name": "1", "marker": 0.32 },
    { "number": 2, "name": "2", "marker": 0.709 },
    { "number": 3, "name": "3", "marker": 1 }
  ],
  "time": [{
    "gt3": [
      { "name": "sg30", "time": 72 },
      { "name": "dt", "time": 37 }
    ]}
  ]
}

```

#### Full Track Data Example
```JSON
{
  "name": "Silverstone",
  "country": "GB",
  "length": 5890,
  "year": 2022,
  "turn": [
    { "number": 1, "name": "Copse", "marker": 0.042, "scale": 4, "direction": 1, "start": 0.024, "end": 0.045 },
    { "number": 2, "name": "T2", "marker": 0.133, "scale": 5, "direction": 0 },
    { "number": 3, "name": "Maggots", "marker": 0.151, "scale": 3, "direction": 1 },
    { "number": 4, "name": "T4", "marker": 0.176, "scale": 3, "direction": 0 },
    { "number": 5, "name": "Becketts", "marker": 0.201, "scale": 3, "direction": 1 },
    { "number": 6, "name": "Chapel", "marker": 0.229, "scale": 5, "direction": 0, "start": 0.210, "end": 0.238 },
    { "number": 7, "name": "Stowe", "marker": 0.377, "scale": 4, "direction": 1, "start": 0.350, "end": 0.385 },
    { "number": 8, "name": "Vale", "marker": 0.432, "scale": 1, "direction": 0, "start": 0.400, "end": 0.440 },
    { "number": 9, "name": "Club", "marker": 0.469, "scale": 3, "direction": 1, "start": 0.445, "end": 0.500 },
    { "number": 10, "name": "T10", "marker": 0.499, "scale": 5, "direction": 1 },
    { "number": 11, "name": "Abbey", "marker": 0.594, "scale": 4, "direction": 1, "start": 0.570, "end": 0.595 },
    { "number": 12, "name": "Farm", "marker": 0.628, "scale": 6, "direction": 0, "start": 0.610, "end": 0.635 },
    { "number": 13, "name": "Village", "marker": 0.672, "scale": 1, "direction": 1, "start": 0.650, "end": 0.680 },
    { "number": 14, "name": "Loop", "marker": 0.696, "scale": 1, "direction": 0, "start": 0.680, "end": 0.705 },
    { "number": 15, "name": "Aintree", "marker": 0.731, "scale": 2, "direction": 0, "start": 0.717, "end": 0.738 },
    { "number": 16, "name": "Brooklands", "marker": 0.858, "scale": 2, "direction": 0, "start": 0.825, "end": 0.865 },
    { "number": 17, "name": "Luffield", "marker": 0.887, "scale": 1, "direction": 1, "start": 0.870, "end": 0.910 },
    { "number": 18, "name": "Woodcote", "marker": 0.949, "scale": 6, "direction": 1, "start": 0.930, "end": 0.960 }
  ],
  "straight": [
    { "number": 1, "name": "Hangar Straight", "scale": 0, "start": 0.235, "end": 0.355 },
    { "number": 2, "name": "Hamilton Straight", "scale": 0, "start": 0.515, "end": 0.560},
    { "number": 3, "name": "Wellington Straight", "scale": 0, "start": 0.760, "end": 0.810}
  ],
  "sector": [
    { "number": 1, "name": "1", "marker": 0.320 },
    { "number": 2, "name": "2", "marker": 0.709 },
    { "number": 3, "name": "3", "marker": 1 }
  ],
  "time": [{
    "gt3": [
      { "name": "sg30", "time": 72 },
      { "name": "dt", "time": 37 }
    ]}
  ]
}

```

#### Full Track Data with Extra Data Example (GT7)
```JSON
{
  "name": "Silverstone",
  "country": "GB",
  "length": 5890,
  "year": 2022,
  "turn": [
    { "number": 1, "name": "Copse", "marker": 0.042, "scale": 4, "direction": 1, "start": 0.024, "end": 0.045 },
    { "number": 2, "name": "T2", "marker": 0.133, "scale": 5, "direction": 0 },
    { "number": 3, "name": "Maggots", "marker": 0.151, "scale": 3, "direction": 1 },
    { "number": 4, "name": "T4", "marker": 0.176, "scale": 3, "direction": 0 },
    { "number": 5, "name": "Becketts", "marker": 0.201, "scale": 3, "direction": 1 },
    { "number": 6, "name": "Chapel", "marker": 0.229, "scale": 5, "direction": 0, "start": 0.210, "end": 0.238 },
    { "number": 7, "name": "Stowe", "marker": 0.377, "scale": 4, "direction": 1, "start": 0.350, "end": 0.385 },
    { "number": 8, "name": "Vale", "marker": 0.432, "scale": 1, "direction": 0, "start": 0.400, "end": 0.440 },
    { "number": 9, "name": "Club", "marker": 0.469, "scale": 3, "direction": 1, "start": 0.445, "end": 0.500 },
    { "number": 10, "name": "T10", "marker": 0.499, "scale": 5, "direction": 1 },
    { "number": 11, "name": "Abbey", "marker": 0.594, "scale": 4, "direction": 1, "start": 0.570, "end": 0.595 },
    { "number": 12, "name": "Farm", "marker": 0.628, "scale": 6, "direction": 0, "start": 0.610, "end": 0.635 },
    { "number": 13, "name": "Village", "marker": 0.672, "scale": 1, "direction": 1, "start": 0.650, "end": 0.680 },
    { "number": 14, "name": "Loop", "marker": 0.696, "scale": 1, "direction": 0, "start": 0.680, "end": 0.705 },
    { "number": 15, "name": "Aintree", "marker": 0.731, "scale": 2, "direction": 0, "start": 0.717, "end": 0.738 },
    { "number": 16, "name": "Brooklands", "marker": 0.858, "scale": 2, "direction": 0, "start": 0.825, "end": 0.865 },
    { "number": 17, "name": "Luffield", "marker": 0.887, "scale": 1, "direction": 1, "start": 0.870, "end": 0.910 },
    { "number": 18, "name": "Woodcote", "marker": 0.949, "scale": 6, "direction": 1, "start": 0.930, "end": 0.960 }
  ],
  "straight": [
    { "number": 1, "name": "Hangar Straight", "scale": 0, "start": 0.235, "end": 0.355 },
    { "number": 2, "name": "Hamilton Straight", "scale": 0, "start": 0.515, "end": 0.560},
    { "number": 3, "name": "Wellington Straight", "scale": 0, "start": 0.760, "end": 0.810}
  ],
  "sector": [
    { "number": 1, "name": "1", "marker": 0.320 },
    { "number": 2, "name": "2", "marker": 0.709 },
    { "number": 3, "name": "3", "marker": 1 }
  ],
  "time": [{
    "gt3": [
      { "name": "sg30", "time": 72 },
      { "name": "dt", "time": 37 }
    ]}
  ],
  "extra": {
    "israinpossible": 1,
    "reversetrackid": -1,
    "coordinatebox_x": 330.51,
    "coordinatebox_y": -27.919,
    "coordinatebox_z": 313.279,
    "coordinateboxexit_x": 115.89,
    "coordinateboxexit_y": -11.299,
    "coordinateboxexit_z": 351.091,
    "startlineunitvector_x": -0.9652885098,
    "startlineunitvector_y": -0.2611859353
  }
}

```

## Contributing
To maintain properly formatted files, I've implemented - and require - a `pre-commit` script, that will prettify the JSON files and thus properly track changes to them.

### 1. Install Pre-Commit Hook
Before you can run hooks, you need to have the pre-commit package manager installed. You can do so by following the instructions on the [official pre-commit website](https://pre-commit.com/#installation), or just install it using the following command:

```
brew install pre-commit
```

Homebrew not your thing? Read more on the [official pre-commit website](https://pre-commit.com/#installation).


### 2. Install Git Hook Scripts

Once installed, run `pre-commit install` to set up the git hook scripts

```
pre-commit install
```

### 3. Test & Finish
You're all set as far as tooling is concerned. Every time you make a commit, the `pre-commit` script will make sure the files are properly formatted and are prettified. 

It's usually a good idea to run the hooks against all of the files when adding new hooks (usually pre-commit will only run on the changed files during git hooks). Running `pre-commit run --all-files` will have a pass at everythig, and if all is well, you should see somthing like the below. 

```
$ pre-commit run --all-files
check json...............................................................Passed
pretty format json.......................................................Passed
```

## Credits
Corner and Straights names are from [Racing Circuits](https://www.racingcircuits.info). Big thanks to Nicolas of [Simhub](https://www.simhubdash.com) and Joerg Behrens for sharing feedback on the File Format.
