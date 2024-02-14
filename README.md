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
# name          - The full human readable track name
# country       - (OPTIONAL) The track's country code (ISO 3166 Alpha 2)
# length        - (OPTIONAL) Length of the track in meters
# segments      - An array of all the Segment data
  # type        - Segment Type 0: Turn, 1: Straight
  # name        - Segment or Turn Name
  # marker      - The percentage point of the Apex
  # scale       - (OPTIONAL) 1-6: Turn (Hairpin > Wide)
  # direction   - (OPTIONAL) 0: Left, 1: Right
  # start       - (OPTIONAL) The percentage point segment start
  # end         - (OPTIONAL) The percentage point segment end
# sector        - An array of all the track Sectors
  # name        - The Sector number
  # marker      - The percentage point of the Sector
# time          - OPTIONAL An array of estimated time delays
  # class       - The car class (sim dependant)
    # name      - Name of the time delay
    # time      - Time delay in seconds
```

### Example for `silverstone.json`

#### Simple Track Data Example
```JSON
{
  "name": "Silverstone",
  "segment": [
    { "type": 0, "name": "T1", "marker": 0.042 },
    { "type": 0, "name": "T2", "marker": 0.133 },
    { "type": 0, "name": "T3", "marker": 0.151 },
    { "type": 0, "name": "T4", "marker": 0.176 },
    { "type": 0, "name": "T5", "marker": 0.201 },
    { "type": 0, "name": "T6", "marker": 0.229 },
    { "type": 1, "name": "Hangar Straight", "start": 0.235, "end": 0.355 },
    { "type": 0, "name": "T7", "marker": 0.377 },
    { "type": 0, "name": "T8", "marker": 0.432 },
    { "type": 0, "name": "T9", "marker": 0.469 },
    { "type": 0, "name": "T10", "marker": 0.499 },
    { "type": 1, "name": "Hamilton Straight", "start": 0.515, "end": 0.560},
    { "type": 0, "name": "T11", "marker": 0.594 },
    { "type": 0, "name": "T12", "marker": 0.628 },
    { "type": 0, "name": "T13", "marker": 0.672 },
    { "type": 0, "name": "T14", "marker": 0.696 },
    { "type": 0, "name": "T15", "marker": 0.731 },
    { "type": 1, "name": "Wellington Straight", "start": 0.760, "end": 0.810},
    { "type": 0, "name": "T16", "marker": 0.858 },
    { "type": 0, "name": "T17", "marker": 0.887 },
    { "type": 0, "name": "T18", "marker": 0.949 }
  ],
  "sector": [
    { "name": "1", "marker": 0.32 },
    { "name": "2", "marker": 0.709 },
    { "name": "3", "marker": 1 }
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
  "segment": [
    { "type": 0, "name": "Copse", "marker": 0.042, "scale": 4, "direction": 1, "start": 0.024, "end": 0.045 },
    { "type": 0, "name": "T2", "marker": 0.133, "scale": 5, "direction": 0 },
    { "type": 0, "name": "Maggots", "marker": 0.151, "scale": 3, "direction": 1 },
    { "type": 0, "name": "T4", "marker": 0.176, "scale": 3, "direction": 0 },
    { "type": 0, "name": "Becketts", "marker": 0.201, "scale": 3, "direction": 1 },
    { "type": 0, "name": "Chapel", "marker": 0.229, "scale": 5, "direction": 0, "start": 0.210, "end": 0.238 },
    { "type": 1, "name": "Hangar Straight", "scale": 0, "start": 0.235, "end": 0.355 },
    { "type": 0, "name": "Stowe", "marker": 0.377, "scale": 4, "direction": 1, "start": 0.350, "end": 0.385 },
    { "type": 0, "name": "Vale", "marker": 0.432, "scale": 1, "direction": 0, "start": 0.400, "end": 0.440 },
    { "type": 0, "name": "Club", "marker": 0.469, "scale": 3, "direction": 1, "start": 0.445, "end": 0.500 },
    { "type": 0, "name": "T10", "marker": 0.499, "scale": 5, "direction": 1 },
    { "type": 1, "name": "Hamilton Straight", "scale": 0, "start": 0.515, "end": 0.560},
    { "type": 0, "name": "Abbey", "marker": 0.594, "scale": 4, "direction": 1, "start": 0.570, "end": 0.595 },
    { "type": 0, "name": "Farm", "marker": 0.628, "scale": 6, "direction": 0, "start": 0.610, "end": 0.635 },
    { "type": 0, "name": "Village", "marker": 0.672, "scale": 1, "direction": 1, "start": 0.650, "end": 0.680 },
    { "type": 0, "name": "Loop", "marker": 0.696, "scale": 1, "direction": 0, "start": 0.680, "end": 0.705 },
    { "type": 0, "name": "Aintree", "marker": 0.731, "scale": 2, "direction": 0, "start": 0.717, "end": 0.738 },
    { "type": 1, "name": "Wellington Straight", "scale": 0, "start": 0.760, "end": 0.810},
    { "type": 0, "name": "Brooklands", "marker": 0.858, "scale": 2, "direction": 0, "start": 0.825, "end": 0.865 },
    { "type": 0, "name": "Luffield", "marker": 0.887, "scale": 1, "direction": 1, "start": 0.870, "end": 0.910 },
    { "type": 0, "name": "Woodcote", "marker": 0.949, "scale": 6, "direction": 1, "start": 0.930, "end": 0.960 }
  ],
  "sector": [
    { "name": "1", "marker": 0.320 },
    { "name": "2", "marker": 0.709 },
    { "name": "3", "marker": 1 }
  ],
  "time": [{
    "gt3": [
      { "name": "sg30", "time": 72 },
      { "name": "dt", "time": 37 }
    ]}
  ]
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
