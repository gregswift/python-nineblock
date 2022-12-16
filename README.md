# nineblock

This is a visualization tool for the 9blocking exercise.

# Known issues
* relies on current DATADIR to exist at same level as app.py
  * Would like to see the dataset be selectable based on directory names
* On main view if you select a person, for some reason its defaulting to empty          
  groupby, which will then show n-number of entries, with the user's name on all.
  I think its a bit of a dataset state issue where its showing the Whote Team's
  info too. This started after making the controls a dynamically added part of
  the sidebar rather than just at the top of the page.
* Really I just don't like the visualization of hte controls

# Future steps
* Be the survey tool as well
  * needs identity support with teams and permissions
* Support visualizing the change in your scoring over time
* Better controls
