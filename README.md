# gitlab-migration-tools

## get_participants.py 

Returns the Github user names of contributors and commenters of a github project

```console
$ python3 ./get_participants.py
Repo owner [tango-controls] ? 
Repo name [pytango] ? jtango

getting contributors (page 1): 7
getting commenters (page(1): 100
getting commenters (page(2): 100
getting commenters (page(3): 22

Unique users for github.com/tango-controls/jtango:
@Ingvord, @KrystianKedron, @Pascal-Verdier, @altavir, @bourtemb, @gwen-soleil, @jc17609, @jkotan, @ma-neumann, @reszelaz, @sergirubio, @t-b, @tre3k

```

## add_moved_branch.sh

Helper script to add a `moved-to-gitlab` branch to the old repository. So, the day of the migration, do:

1. archive the GH project
2. import it as `https://gitlab.com/tango-controls/<projectname>` using the @tango-controls-bot account, and check it.
3. momentarily unarchive the GH project 
4. run `add_moved_branch.sh <projectname>` 
4. In GH, change the default branch of the project to `moved-to-gitlab` and change the project description to "Moved to gitlab"
5. Archive the project in GH again.
6. Notify the tango community about the migration (send an email to info@tango-controls.org) and add a comment in [this migration issue](https://github.com/tango-controls/TangoTickets/issues/47)
