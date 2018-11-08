# How to use Flask-Migrate

## Creating A Migration

..* $ flask db migrate --message "Your Comments Here"

## Updating Head To Newest Migration

..* $ flask db upgrade

## Moving Head To Specific Migration

..* $ flask db upgrade <revision>   //Where <revision> is the revision number

## Display Information For A Specific Revision

..* $ flask db current   //For the current revision

..* $ flask db history   //For a list of all revision numbers

..* $ flask db history --verbose    //For a list of all revision numbers and their full information