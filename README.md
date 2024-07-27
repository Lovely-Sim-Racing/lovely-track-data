<p align="center">
<img width="150" height="150" alt="Lovely Sim Racing" src="docs/images/lr-logo-small.png">
</p>

<h1 align="center">Lovely Track Data</h1>

<p align="center">
A comprehensive list of Track Data for Sim Racing games.<br>
<strong>File Format v1.1.0 Beta</strong>
</p>

---

## How to
Fetch the data by retrieving the url:
`/data/{simId}/{trackId}.json`

* `{simId}` is the lowercase Simhub game id `DataCorePlugin.CurrentGame`
* `{trackId}` is the lowercase Simhub track id `DataCorePlugin.TrackId`

## Changelog
Read the [changelog](changelog.md) to keep track of the format updates.

## File Format
Every file is formatted as follows:

``` 
# name          (String) - The full human readable track name
# country       (String) - (OPTIONAL) The track's country code (ISO 3166 Alpha 2)
# year          (Int)    - (OPTIONAL) The track's active year
# length        (Int)    - (OPTIONAL) Length of the track in meters
# pitentry      (Int)    - (OPTIONAL) The percentage point of the pit entry
# pitexit       (Int)    - (OPTIONAL) The percentage point of the pit exit
# turn                   - An array of all the Turn data
  # name        (String) - (OPTIONAL if number is present) Turn Name
  # number      (Int)    - (OPTIONAL if nane is present) Turn Number
  # marker      (Int)    - (OPTIONAL) The percentage point of the Apex
  # scale       (Int)    - (OPTIONAL) 1-6: Turn (Hairpin > Wide)
  # direction   (Int)    - (OPTIONAL) 0: Left, 1: Right
  # start       (Int)    - The percentage point of turn start
  # end         (Int)    - The percentage point of turn end
  # extra                - (OPTIONAL) An array of properties
    # keys      (Mixed)  - Key:Value
# straight               - (OPTIONAL) An array of all the Straight data
  # name        (String) - Straight Name
  # start       (Int)    - The percentage point of straight start
  # end         (Int)    - The percentage point of straight end
  # extra                - (OPTIONAL) An array of properties
    # keys      (Mixed)  - Key:Value
# sector                 - An array of all the Sector data
  # name        (String) - Sector Name
  # marker      (Int)    - The percentage point of the Sector
  # extra                - (OPTIONAL) An array of properties
    # keys      (Mixed)  - Key:Value
# time                   - (OPTIONAL) An array of estimated time delays
  # class       (String) - The car class (sim dependant)
    # name      (String) - Name of the time delay
    # time      (Int)    - Time delay in seconds
# companion              - (OPTIONAL) Optimal display of the Track Map on the Lovely Dashboard Companion
  # top         (Int)    - Distance to top
  # left        (Int)    - Distance to left
  # rotation    (Int)    - Rotation
  # scale       (Int)    - Auto Size Scale
# extra                  - (OPTIONAL) An array of properties
  # keys        (Mixed)  - Key:Value
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
