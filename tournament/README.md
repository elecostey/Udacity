
PROJECT - TOURNAMENT RESULTS

GENERAL USAGE NOTES - HOW TO USE THE VM IN GIT BASH
-------------------------------------------------------------------------------
- To run VM use command:
```
$ vagrant up
```

- To login to the web server:
```
$ vagrant ssh
```

- Go to the tournament directory:
```
$ cd /tournament
```

- Run the command:
```
$ psql
```

- create your database:
```
=> CREATE DATABASE tournament;
```

- connect to the database created:
```
=> \c tournament
```

- run the sql file:
```
=> \i tournament.sql
```


-  to test tournament.py  with the test cases in tournament_test.py:
```
$ python tournament_test.py
```

REQUIREMENTS
-------------------------------------------------------------------------------
- This software requires Python Interpreter 2.X.X to run.
- This software was built using Python 2.7.12
- PostgreSQL

CONTACT
-------------------------------------------------------------------------------
Author: Elodie Lecostey
E-mail: elodie_lecostey@hotmail.com
Github: https://github.com/elecostey/Udacity/tree/master/my-blog




