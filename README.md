# AutoLeague
An automatic league-runner for Rocket League bots ([RLBot](http://rlbot.org/))

# How to use:

 - To install, clone this repo and run `pip install -e .` in the directory containing `setup.py`.
 - This should giveyou access to the `autoleague` command line tool. try `autoleague --help`.
 - To run most commands, you'll need to specify a `--working_dir` flag or alternatively, you can set a `AUTOLEAGUE_WORKING_DIR` environment varable to save youself future typing.
 - To get a default list of bots to play try `autoleague download_bot_pack`. Bots are automatically discovered within the `working_dir/bots`, so you could add more if you'd like or remove ones you don't like.
 - To add to the match queue use `autoleague generate_matches`
 - To run the scheduled matches, use `autoleague run_matches`
 - To visually view the match results, you can spin up a local website using `autoleague history_dev_server`. This webserver can run while matches are running to pick up latest match results as soon as the matches complete.
 
