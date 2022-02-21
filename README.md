# Simple case tracker

This is a simple support ticket tracker CLI app for anyone working in an applicable field. This is still a work in progress, contributions are very welcome.


**DISCLAIMER:** The code can be buggy, do your own review before you start using it for business.

It aims to provide a help for complicated enterprise software that lack some very basic features, like listing due dates based on customer tiers and past interactions. It's intended to be used as an assistance for a more complex solution that is used in your business.

### Quickstart:

`git clone https://github.com/bcsabae/case-tracker` \
`cd case-tracker` \
`python3 case-tracker.py`

Make sure to create the library file, it won't be created for you automatically!

`touch lib.csv`

Note that at the moment only Python 3 is supported.


## How it works

A case or ticket has the following properties:
- ID number
- customer's name
- short title or description
- customer tier (or priority)
- last customer interaction
- status

Based on the status, on the last customer interaction, and on the customer tier, the next needed response's time is calculated. A CLI interface provides access to most of the real-world interactions. These are interactions like when the customer answers to a ticket, or if the user answered a ticket to the customer. Freezing and closing is also implemented. When calculating response deadlines, weekends are not included. For example if there is 2 days to respond, and it's Thursday, the deadline will be on next Monday.

## CLI commands

The main way to use the software is through it's simple CLI interface. A few good to know things:
- Dates are expected and printed in the default format "2022.01.01. 10:00". This can be modified in the source code.
- For commands that except a date and time, if none is specified, the current date and time is used.
- After every successful command, the local database is updated and automatically saved.

`list all/todo/today/tomorrow`

List tickets

**all:** list all tickets in library
**todo:** list tickets that need user interaction
**today:** list tickets that need user interaction until next working day's opening hours (hard-coded as 10:00 AM for now)
**tomorrow:** list tickets that need user interaction until next working day's midnight

`case num [num] update/answer/freeze/close [date:optional]`

Interact with existing tickets

**num:** ticket ID number (mandatory)
**update:** customer updated the ticket (date parameter is omitted)
**answer:** user updated the ticket at the time passed with the date parameter
**freeze:** ticket gets frozen (date parameter is omitted)
**close:** ticket gets closed and deleted from local database (date parameter is omitted)
**date:** date and time in the specified format, if not explicitly specified, commands that need a date and time use current time

`case new [number] [customer] [title] [tier] [opened_at:optional]`

Create new ticket

**number:** ID number of the new ticket
**customer:** name of the customer
**title:** short title or description of the ticket
**tier:** customer tier
**opened_at:** date and time of ticket opening, if not explicitly specified, use current date and time

`exit`

Exit the program.


## Configuration

A default `config.json` file is provided for reference. All supported parameters are in there. Wrong configuration errors are barely checked at the moment, so if you are seeing an odd behavior, it might be good to check your config file first.

Note that once the ticket library is built with a specific datetime format - like `"%Y.%m.%d %H:%M"`, changing this option will not make your ticket library backwards-compatible. You will get errors until you either revert your old settings or manually transfer to your new standard.


## Reporting bugs

If you think you found something that doesn't work as it's intended, please report as a bug using the issue reporter. Please include the following info in the description:
- short description of the bug
- what you exactly did before seeing this issue
- what do you think should happen instead
- if you have a hunch or you know what causes the error

If you feel you have the solution, feel free to fix it and commit to the develop branch. See how to contribute below.

### Feature requests

If you think there is a cool feature you would like to see, feel free to add an issue for this. Just please make sure it is cleat that this is not something that *should* work, but something that is not built in yet but would be nice to see. If there's alredy a request for the feature, drop a comment there to sign your interest.

## Contributing

If you want to contribute, you are very welcome to do so! A good place to start is to check the reported issues and feature requests and see if you can/want to do something. For every time, be an issue or feature, open an issue if there is none already. After writing the code, commit to a new branch containing the ID of the issue. After verifying, these get to develop branch which gets back to master. An example flow of a commit:

1. You discovered a bug or a feature you'd like to see
2. Open an issue describing what it is, e.g. *Issue #123: description*
3. Write your code
4. Commit to a new branch named *bugfix_123* or *feature_123*. The commit message should contain the ID of the issue, something like: *Resolved bug #123* or *Added feature 123*
5. After everything you wanted to do is done, open a pull request containing the developed issues (more if there are more)
6. This pull request gets merged to ***develop***
7. ***develop*** periodically gets merged to ***master***
8. Your commit is in the main code!
