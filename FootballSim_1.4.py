# FootballSim Version 1.3
# Made by Logan Nyquist
# All code is my own original work
# Version history
# Future plans: coach mode, difficulty, versus mode, only offense, stats by position, custom difficulty, ncaa/nfl overtime, timeouts
# 1.4: Balance changes, separate conditions for run and pass, added hail mary and fumbles (12/2023)
# 1.3: Reworked code for displaying score and time, switched to Python (11/2023)
# 1.2: Added main menu and settings menu, debug mode, sim speed (12/2022)
# 1.1: Teams have to kick for extra point, can go on 4th down in certain situations (11/2020)
# 1.0: Original (10/27/2020)

# allows user to view/change settings
def SettingMenu(settings):
    exit = "false"
    while (exit == "false"):
        print("\nCurrent settings:")

        print("Debug mode: ")
        if (settings["debug"] == 0):
            print("Off")
        elif (settings["debug"] == 1):
            print("On")
        else: print("invalid setting")

        print("Play mode: ")
        if (settings["mode"] == 0):
            print("Sim")
        elif (settings["mode"] == 1):
            print("Coach")
        else: print("invalid setting")

        print("Difficulty: ")
        if (settings["difficulty"] == 0):
            print("Easy")
        elif(settings["difficulty"] == 1):
            print("Medium")
        elif (settings["difficulty"] == 2):
            print("Hard")
        #add harder in the future
        else: print("invalid setting")

        print("Sim speed: ")
        if (settings["speed"] == 0):
            print("Play-by-play")
        elif (settings["speed"] == 1):
            print("Whole game")
        elif (settings["speed"] == 2):
            print("Every score/quarter")
        else: print("invalid setting")

        print("\n1: Edit settings\n2: View description of each setting\n0: Exit setting menu")
        choice = int(input("\nEnter an option: "))
        if (choice == 1):
            print("Debug Mode (D=on, X=off)\nPlay mode (S=sim, C=coach)\nDifficulty(E=easy, M=medium, H=hard)")
            print("Sim speed (P=play-by-play, Q=score/quarter, W=whole game)")
            put = input("\nEnter an option: ")
            option = put.upper()
            if   (option == 'D'): settings["debug"] = 1
            elif (option == 'X'): settings["debug"] = 0
            elif (option == "S"): settings["mode"] = 0
            elif (option == 'C'): settings["mode"] = 1
            elif (option == 'E'): settings["difficulty"] = 0
            elif (option == 'M'): settings["difficulty"] = 1
            elif (option == 'H'): settings["difficulty"] = 2
            elif (option == 'P'): settings["speed"] = 0
            elif (option == 'W'): settings["speed"] = 1
            elif (option == 'Q'): settings["speed"] = 2
            else: print("Invalid option")

        elif (choice == 2):
            print("Debug mode: If on, automatically sims a game with all stats at 50")
            print("\nPlay mode: Coach mode means you choose the plays for one team, sim mode has both teams simulated")
            print("\nDifficulty: Decides strength of the opponent in coach mode")
            print("\nSim speed: How often the sim will pause for you to manually continue. Whole game sims the whole game with no pauses.")
        elif (choice == 0):
                exit = "true"
        else: print("Invalid option")
# end SettingMenu

#returns adjective suffix of given number
def Suffix(num):
    num = abs(num)
    if   (num == 1): 
        return "st"
    elif (num == 2): 
        return "nd"
    elif (num == 3): 
        return "rd"
    else: 
        return "th"
# end Suffix

#returns time in mm:ss
def Time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"

# end Time

# executes kickoff, returns yards to goal (toGoal)
def Kickoff(adv, possession):
    import random
    if (random.random() > 0.25):
        print("\n" + possession + " gets a touchback.")
        return 75
    else:
        gained = int(random.triangular(1, 100, 25+adv/4))
        print("\n" + possession + " returns for " + str(gained) + " yards.")
        return 100 - gained
# end Kickoff

# displays the time, ball position, current down, and score
# result is what to display: s = just score, p = just position/time, o = overtime
def Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, result, awayScore, homeScore):
    
    #print score
    if (result == 's' or result == 'o'):
        print("The score is " + awayTeam + " " + str(awayScore) + ", " + homeTeam + " " + str(homeScore) + ".")
        if (result == 'o' or settings["speed"] != 1):
            cont = input("Press enter to continue: ")
            if (cont == 'p'):
                settings["speed"] = 0
            elif (cont == 'g'):
                settings["speed"] = 1
            elif (cont == 's'):
                settings["speed"] = 2
    
    #print position
    if (result == 'p' or result == 'a'):
        if (toGoal <= toFirst):
            display = "goal"
        else:
            display = str(toFirst)
            
        play = "\n" + str(down) + Suffix(down) + " and " + display + ", " + possession + "'s ball on "

        if (toGoal < 50):
            if (possession == homeTeam):
                    play += awayTeam + "'s " + str(toGoal)
            else:
                play += homeTeam + "'s " + str(toGoal)
        else:
            if (possession == awayTeam):
                play += awayTeam + "'s " + str(100 - toGoal)
            else:
                play += homeTeam + "'s " + str(100 - toGoal)
        print(play)

        #print time
        time = Time(int(clock)) + " left in "
        if (q > 4):
            time = time + "overtime"
        else:
            time = time + "the " + str(q) + Suffix(q) + " quarter."
        print(time)
        if (settings["speed"] == 0):
            cont = input("Press enter to continue: ")
            if (cont == 'p'):
                settings["speed"] = 0
            elif (cont == 'g'):
                settings["speed"] = 1
            elif (cont == 's'):
                settings["speed"] = 2
                
    
    return 0
# end Display

#returns the score difference
def ScoreDiff(possession, homeTeam, homeScore, awayScore):
    if (possession == homeTeam):
        return homeScore - awayScore
    else: return awayScore - homeScore

# sim mode - neither side is user controlled
def PlaySim (settings):

    # enter stats
    if (settings["debug"] == 1):
        awayTeam = "apple"
        homeTeam = "banana"
        awayOff = 50
        awayDef = 50
        homeOff = 60
        homeDef = 60
    else:
        awayTeam = input("\nAway team name: ")
        homeTeam = input("Home team name: ")
        print("\nEnter stats between 0-100.")
        awayOff = int(input(awayTeam + " offense: "))
        awayDef = int(input(awayTeam + " defense: "))
        homeOff = int(input(homeTeam + " offense: "))
        homeDef = int(input(homeTeam + " defense: "))

    awayAdv = awayOff - homeDef
    homeAdv = homeOff - awayDef

    # coin flip
    import random
    if (random.random() > 0.5):
        print(homeTeam + " wins the coin toss!")
        if (random.random() > 0.5):
            print("They choose to receive.")
            possession = homeTeam
            adv = homeAdv
            halfReturn = awayTeam
        else:
            print("They choose to kick.")
            possession = awayTeam
            adv = awayAdv
            halfReturn = homeTeam
    else:
        print(awayTeam + " wins the coin toss!")
        if (random.random() > 0.5):
            print("They choose to kick.")
            possession = homeTeam
            adv = homeAdv
            halfReturn = awayTeam
        else:
            print("They choose to receive.")
            possession = awayTeam
            adv = awayAdv
            halfReturn = homeTeam

    cont = input("Press enter to continue: ")
    if (cont == 'p'):
            settings["speed"] = 0
    elif (cont == 'g'):
        settings["speed"] = 1
    elif (cont == 's'):
        settings["speed"] = 2

    numPlays = 0
    homeScore = 0
    awayScore = 0
    down = 1
    toFirst = 10
    toGoal = Kickoff(adv, possession)
    q = 1
    YPS = 3 #yards per second

    # game loop
    while ((q <= 4) or (homeScore == awayScore)):

        # quarter loop
        clock = 900
        while (clock > 0):
            
            Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, 'p', awayScore, homeScore)
            numPlays += 1

            r = random.gauss(3, 20) + (adv / 3.75) #std changed from 18, adv divisor changed from 4
            # next play

            #decide between run, pass, and hail mary
            if (clock < 30 and q >= 4 and ScoreDiff(possession, homeTeam, homeScore, awayScore) < 0):
                play = "hailmary"
            elif (down == 4 and (toGoal >= 5 or toFirst >= 3)):
                if (toGoal <= 30):
                    play = "fieldgoal"
                else: play = "punt"
            elif (down < 3 or toFirst < 3):
                if (random.randint(1,3) == 1):
                    play = "pass"
                else: play = "run"
            elif (random.randint(1,3) == 1):
                    play = "run"
            else: play = "pass"

            # field goal
            if (play == "fieldgoal"):

                print("\n" + possession + " will try for a " + str(toGoal + 18) + " yard field goal.")
                print("\nThe kick is...")
                if (random.randint(1,100) >= toGoal + 18):
                    print("Good!")
                    if (possession == homeTeam):
                        homeScore += 3
                        possession = awayTeam
                        adv = awayAdv
                    else:
                        awayScore += 3
                        possession = homeTeam
                        adv = homeAdv
                else:
                    print("no good.")
                    if (possession == homeTeam):
                        possession = awayTeam
                        adv = awayAdv
                    else:
                        possession = homeTeam
                        adv = homeAdv
                        
                clock -= random.randint(20, 25)
                if (clock > 0):
                        Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, 's', awayScore, homeScore)
                        toGoal = 100 - toGoal
                        down = 1
                        toFirst = 10
                        toGoal = Kickoff(adv, possession)
                elif (q > 4):
                    clock = 0
                    break
            
            # punt
            elif (play == "punt"):

                punt = random.randint(30, 50)
                print("\n" + possession + " punts the ball " + str(punt) + " yards.")
                if (possession == homeTeam):
                    possession = awayTeam
                    adv = awayAdv
                else:
                    possession = homeTeam
                    adv = homeAdv
                down = 1
                toFirst = 10
                toGoal = 100 - toGoal + punt
                if (toGoal > 99):
                    toGoal = 75
                clock -= (random.randint(0,20) + punt/YPS)
                if (clock <= 0):
                    break

            # run
            elif (play == "run"):
                
                # fumble
                if (r <= -40):
                    print("\nThe ball comes loose!")
                    if (random.randint(1,2) == 1):
                        if (possession == homeTeam):
                            possession = awayTeam
                            adv = awayAdv
                        else:
                            possession = homeTeam
                            adv = homeAdv
                        print("\n" + possession + " recovers the fumble!")
                        gained = random.randint(int(r/7), int(abs(r/2)))
                        down = 1
                        toFirst = 10
                        toGoal = 100 - toGoal - gained
                        clock -= (random.randint(5, 15) + gained)
                    else:
                        print("\n" + possession + " recovers the fumble.")
                        gained = random.randint(-3, 0)
                        toGoal -= gained
                        toFirst -= gained
                        down += 1
                        clock -= (random.randint(20,40) + abs(gained/YPS))

                # short run
                elif ((r > -40) and (r <= 40)):
                    gained = int(random.triangular(-5, 20, r/8))
                    if (gained > toGoal):
                        gained = toGoal
                    print("\n" + possession + " ran the ball for " + str(gained) + " yards.")
                    toGoal -= gained
                    toFirst -= gained
                    down += 1
                    clock -= (random.randint(20,40) + gained/YPS)

                # long run
                else:
                    gained = int(random.triangular(r-20, r+30, r/2))
                    if (gained > toGoal):
                        gained = toGoal
                    print("\n" + possession + " breaks through the defense and runs the ball " + str(gained) + " yards!")
                    toGoal -= gained
                    toFirst -= gained
                    down += 1
                    clock -= (random.randint(20,40) + gained/YPS)
                    
            # pass
            elif (play == "pass"):

                # interception
                if (r <= -35):
                    if (possession == homeTeam):
                        possession = awayTeam
                        adv = awayAdv
                    else:
                        possession = homeTeam
                        adv = homeAdv
                    print("\nPass is intercepted!\n" + possession + " now has the ball.")
                    gained = random.randint(-1, abs(int(r)))
                    down = 1
                    toFirst = 10
                    toGoal = 100 - toGoal - gained
                    clock -= (random.randint(5, 15) + gained/YPS)

                # strip sack
                elif (r > -35 and r <= -30):
                    print("\nStrip sack! The ball comes loose!")
                    if (random.randint(1,2) == 1):
                        if (possession == homeTeam):
                            possession = awayTeam
                            adv = awayAdv
                        else:
                            possession = homeTeam
                            adv = homeAdv
                        print("\n" + possession + " recovers the fumble!")
                        gained = random.randint(int(r/7), int(abs(r/2)))
                        down = 1
                        toFirst = 10
                        toGoal = 100 - toGoal - gained
                        clock -= (random.randint(15,30) + gained/YPS)
                    else:
                        print("\n" + possession + " recovers the fumble.")
                        gained = random.randint(-5, 0)
                        toGoal -= gained
                        toFirst -= gained
                        down += 1
                        clock -= (random.randint(20,40) + gained/YPS)

                # sack
                elif ((r > -30) and (r <= -25)):
                    lost = random.randint(1, 10)
                    print("\nSacked! A " + str(lost) + " yard loss for " + possession + ".")
                    toGoal += lost
                    toFirst += lost
                    down += 1
                    clock -= random.randint(30, 50)

                # incomplete
                elif ((r > -25) and (r <= 0)):
                    print("\nPass is incomplete.")
                    down += 1
                    clock -= random.randint(5, 15)

                # short pass
                elif ((r > 0) and (r <= 30)):
                    gained = int(random.triangular(r-5, r, r/3))
                    if (gained > toGoal):
                        gained = toGoal
                    print("\nPass is caught. " + possession + " gained " + str(gained) + " yards.")
                    toGoal -= gained
                    toFirst -= gained
                    down += 1
                    clock -= (random.randint(20,40) + gained/YPS)

                # long pass
                else:
                    gained = int(random.triangular(r-20, r+30, r/2))
                    if (gained > toGoal):
                        gained = toGoal
                    print("\nPass is caught wide open! " + possession + " gained " + str(gained) + " yards.")
                    toGoal -= gained
                    toFirst -= gained
                    down += 1
                    clock -= (random.randint(20,40) + gained/YPS)

            # hail mary
            elif (play == "hailmary"):
                print("\n" + possession + " is attempting a hail mary.")
                if (random.randint(1,10) == 1): #hail marys have about 10% completion according to ESPN
                    gained = int(random.triangular(50, 75, ))
                    if (gained > toGoal):
                        gained = toGoal
                    print("\nPass is caught! " + possession + " gained " + str(gained) + " yards.")
                    toGoal -= gained
                    toFirst -= gained
                    down += 1
                    clock -= (random.randint(15,30) + gained/YPS) 
                else:
                    print("\nPass is incomplete.")
                    down += 1
                    clock -= (random.randint(5, 15) + toGoal/YPS)
            
            # play result

            # safety
            if (toGoal > 100):
                print("\nSafety!")
                if (possession == homeTeam):
                    awayScore += 2
                    possession = awayTeam
                    adv = awayAdv
                else:
                    homeScore += 2
                    possession = homeTeam
                    adv = homeAdv
                down = 1
                toFirst = 10
                toGoal = 75
                Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, 's', awayScore, homeScore)
                

            # touchdown
            elif (toGoal <= 0):
                print("\nTOUCHDOWN!!")
                if (possession == homeTeam):
                    homeScore += 6
                    possession = awayTeam
                    adv = awayAdv
                    if (awayScore - homeScore == 2):
                        go = 2
                    else:
                        go = 1
                else:
                    awayScore += 6
                    possession = homeTeam
                    adv = homeAdv
                    if (homeScore - awayScore == 2):
                        go = 2
                    else:
                        go = 1
                # point(s) after attempt
                if (go == 1):
                    print("\nThe extra point is...")
                    if (random.randint(1, 7) == 1):
                        print("no good.")
                    else:
                        print("Good!")
                        if (possession == homeTeam):
                            awayScore += 1
                        else:
                            homeScore += 1
                else:
                    print("They will go for 2...")
                    if (random.gauss(adv/4, 10) < 12):
                        print("but don't make it.")
                    else:
                        print("and make it in!")
                        if (possession == homeTeam):
                            awayScore += 2
                        else:
                            homeScore += 2
                Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, 's', awayScore, homeScore)
                down = 1
                toFirst = 10
                toGoal = Kickoff(adv, possession)
                

            # first down
            elif (toFirst <= 0):
                    down = 1
                    print("First down.")
                    if (toFirst >= toGoal):
                        toFirst = toGoal
                    else:
                        toFirst = 10
            elif (down > 4):
                    if (possession == homeTeam):
                        possession = awayTeam
                        adv = awayAdv
                    else:
                        possession = homeTeam
                        adv = homeAdv
                    print("\nTurnover on downs. " + possession + " now has possession.")
                    toGoal = 100 - toGoal
                    toFirst = 10
                    down = 1

        # end of quarter
        q += 1
        clock = 900
        if (q <= 4):
            if (q == 3):
                print ("\nIt is now halftime. ")
                if (halfReturn == homeTeam):
                        possession = homeTeam
                        adv = homeAdv
                        halfReturn = awayTeam
                else:
                        possession = awayTeam
                        adv = awayAdv
                        halfReturn = homeTeam
                print(possession + " will receive the kickoff.")
                Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, 's', awayScore, homeScore)
                down = 1
                toFirst = 10
                toGoal = Kickoff(adv, possession)
            else: 
                print("\nIt is now Quarter " + str(q) + ".")
                Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, 's', awayScore, homeScore)
        elif (awayScore == homeScore):
            print("\nOvertime!")
            if (halfReturn == homeTeam):
                possession = homeTeam
                adv = homeAdv
                halfReturn = awayTeam
            else:
                possession = awayTeam
                adv = awayAdv
                halfReturn = homeTeam
            print(possession + " will receive the kickoff.")
            down = 1
            toFirst = 10
            toGoal = Kickoff(adv, possession)
            Display(toGoal, toFirst, down, possession, homeTeam, awayTeam, clock, q, 'o', awayScore, homeScore)

    # end q loop
    print("\nAnd that's the end of the game.")
    print("\nThe final score is " + awayTeam + " " + str(awayScore) + ", " + homeTeam + " " + str(homeScore) + ".")
    #print("Number of plays: " + str(numPlays))
    cont = input("Press enter to return to menu: ")
# end PlaySim

# debug mode off/on (0/1)
# mode sim/coach (0/1)
# player mode difficulty easy/med/hard (0/1/2)
# sim speed play/game/score (0/1/2)
settings = {"debug":0, 
            "mode":0, 
            "difficulty":1, 
            "speed":2
            }
exit = "false"
while (exit == "false"):
    print("\n*Welcome to FootballSim v1.3*")
    print("1: Start a game\n2: View/edit settings\n0: Exit program")
    choice = int(input("Enter an option: "))

    if (choice == 1):
        if (settings["mode"] == 0):
            PlaySim(settings)
        elif (settings["mode"] == 1):
            print("coming soon") #PlayCoach
        else:
            print("\nInvalid setting for mode")
    elif (choice == 2):
        SettingMenu(settings)
    elif (choice == 0):
        exit = "true"
    else:
        print("\nPlease choose a valid number")

print("\n*Thank you for using FootballSim.")
