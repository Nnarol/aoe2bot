# aoe2bot
Building a bot to reply with technology info (cost, effect, and time to research) to comments in the r/aoe2 subreddit

## Running

`main.py` is the entry point to all logic necessary for receiving, interpreting and answering Reddit comments.

Configuration - particularly Reddit credentials -, must be provided through environment variables however.
As these constitute sensitive information, none are included in the source repository, only an
infrastructure to ease the process of providing such data: `run.sh` runs the main program, configured
with the environment defined by `envconf.sh`.
Although `envconf.sh` is not filled out with useable credentials, a copy is provided with the source
code to serve as a template, including an explanation as to the role of each data item.
To define environment variables, uncomment the relevant lines and substitute appropriate values.
`envconf.sh` must be written Bash.
