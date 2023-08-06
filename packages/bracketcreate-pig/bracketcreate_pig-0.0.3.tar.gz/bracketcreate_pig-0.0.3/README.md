# Overview
bracketcreate_pig is a python library made to programatically create brackets on challonge.com 
returns URL of tournament

## Install
`pip install bracketcreate_pig`

Need chrome installed for library to work

## Usage
```
from bracketcreate_pig import cb

print(cb.create_bracket(participants,username,password,tournament_name,stage_bool,format,time))
```

### Format Choices

Single Elimination

Double Elimination

Round Robin

Swiss

### Stage Bool

False --> One stage

True --> Two stage

### Example Options
participants = [["lim", "ecal"],["pig","doogie"]]

username = "USER"

password = "PASS"

tournament_name = "test_tournament"

stage_bool = False

format = "Single Elimination"

time = "2023/02/11 5:00 PM"

