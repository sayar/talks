#! /usr/bin/env sh

pandoc -t slidy -s junit_mockito_tutorial.md -o junit_mockito_tutorial.html
pandoc -t slidy -s swing_tutorial.md -o swing_tutorial.html
pandoc -t slidy -s git_tutorial.md -o git_tutorial.html
pandoc -t slidy -s ant_maven_tutorial.md -o ant_maven_tutorial.html
pandoc -t slidy -s sql_tutorial.md -o sql_tutorial.html

