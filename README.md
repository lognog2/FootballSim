# FootballSim v1.4
*How to navigate the program*
-
- Upon starting the program, you will be given the choice to start a game, adjust the settings, or exit the progran.
- When starting the game, you will be prompted to enter both teams' names, as well as their offense and defense ratings as ints. From there, the game can begin!
- Below is a description of the settings:
    - Debug mode: When on, automatically sets team names and stats on game start.
    - Play mode: WIP
    - Difficulty: WIP
    - Sim speed: How often the program will pause for user input.
      - Play-by-play: Game will pause on each play. Shortcut: p
      - Score/quarter: Game will pause after a team scores and at the end of each quarter. Shortcut: q
      - Whole game: The game will be fully simulated with no pauses, except for overtime. Shortcut: g
- Settings with a shortcut can be changed in the middle of a game by entering the letter at a pause for input. 

*How it works*
-
- Basic plays are divided into three types: run, pass, and hail mary.
  - If the team with possession is less than 3 yards to a first down, they will run 2/3 of the time and pass 1/3 of the time.
  - If they are more than 3 yards to a first down, they will pass 2/3 of the time and run 1/3 of the time.
  - They will attempt a hail mary if they are losing with less than 30 seconds left in the game.
- For each play, a random number r is generated from a normal distribution, with a mean of 3 and standard deviation of 20, then the advantage (team's offense - other team's defense) / 3.75 is added.
- The value of r affects the outcome of run and pass plays:
  - Run play:
    - r <= -40: fumble, with a 50/50 chance of recovering the ball and losing 0-3 yards, or losing it to the other team, who will run the ball between r/7 and |r/2| yards
    - -40 < r <= 40: short run, between -5 and 20 yards, average of r/8*
    - r > 40: long run, between r-20,and r+30 yards, average of r/2*
  - Pass play:
    - r <= -35: interception, with the other team running the ball back between -1 and |r| yards
    - -35 < r <= -30: strip sack fumble, with a 50/50 chance of recovering the ball and losing 0-5 yards, or losing it to the other team, who will run the ball between r/7 and |r/2| yards
    - -30 < r <= -25: sack, loss of 1-10 yards
    - -25 < r <= 0: incomplete pass
    - 0 < r <= 30: short pass, between r-5 and r yards, average of r/3*
    - r > 30: long pass, between r-20 and r+30 yards, average of r/2*
  - Hail Mary:
      - Has a 1 in 10 chance of completion
      - 50-75 yards gained on completion
- On 4th down, the team with possesstion can either punt, attempt a field goal, or go for first down.
    - If they are either <= 5 yards from the goal line or <= 3 yards from a first down, they will go for it.
        - The basic play code will continue as normal
    - If they are <= 30 yards from the goal line, they will attempt a field goal.
        - Distance to the uprights is distance to goal + 18. If a random number picked from 1-100 is >= distance, the field goal is good.
    - Otherwise they will punt the ball 30-50 yards.
        - Every punt is a fair catch for now
 

*Uses triangular distribution
