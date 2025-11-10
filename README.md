<p align="center">
<img width="150" height="150" alt="Lovely Sim Racing" src="docs/images/lr-logo-small.png">
</p>

<h1 align="center">Lovely Track Data</h1>

<p align="center">
A comprehensive list of Track Data for Sim Racing games.<br>
<strong>File Format v2.0.0 Beta</strong>
</p>

---

## How to
Fetch the data by retrieving the url:
`/data/{simId}/{trackId}.json`

* `{simId}` is the Simhub game id `DataCorePlugin.CurrentGame`
* `{trackId}` is the Simhub track id `DataCorePlugin.TrackId`

### Name Format

Both `{SimId}` and `{trackId}` must adhere to the following naming format:

1. Lowercase
2. Replace accented chars with standard equivalent
3. Replace spaces with hyphen
4. Remove special characters

### Example name formatting

* `F12024 / Baku (Azerbaijan)` -> `f12024/baku-azerbaijan.json`
* `F12024 / Abu Dhabi` -> `f12024/abu-dhabi.json`
* `F12024 / Portimão` -> `f12024/portimao.json`
* `iRacing / Imola GP` -> `iracing/imola-gp.json`

### Example code

```
function nameCleaner($cleanName)
{
    // Convert to lowercase
    $cleanName = mb_strtolower($cleanName, 'UTF-8');

    // Replace accented character with standard
    $cleanName = iconv('UTF-8', 'ASCII//TRANSLIT', $cleanName);
    
    // Replace spaces with hyphen
    $cleanName = preg_replace('/\s+/', '-', $cleanName);
    
    // Replace special characters with hyphen
    $cleanName = preg_replace('/[^a-z0-9]/i', '-', $cleanName);
    
    // Replace multiple hyphens with single
    $cleanName = preg_replace('/-+/', '-', $cleanName);
    
    // Clean leading and trailign hyphens
    $cleanName = trim($cleanName, '-');
    
    return $cleanName;
}   
```

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

---

© 2025 by [Lovely Sim Racing](https://lsr.gg) is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)