  #RandomStrat(ENVIRON,
              #Dirichlet(ENVIRON), COLORS['red']),

  #UnembodiedStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['black']),

  #BossStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #5, COLORS['red']),

  #LTAVIStrat(ENVIRON,
              #ChineseRProcess(ENVIRON),
              #COLORS['purple3']),


    # Experiments
    MIN_T  = -1.0
    MAX_T  = -3.01
    STEP_T =  0.2

    MIN_A  = -0.5
    MAX_A  =  0.51 # Don't move above 1.0 o/w we have prob(prev state) = 0
    STEP_A =  0.1

    #for a in numpy.arange(0.01 , 1.0, 0.05):#numpy.arange(0.01, 1.0, 0.1):
        #arr.append(
            #PigVIStrat(ENVIRON,
                #Dirichlet(ENVIRON, a),
                #COLORS['green'], PLUS=0, EXPLORER=False))

    for t in numpy.arange(MIN_T, MAX_T, STEP_T):
        for a in list(numpy.arange(MIN_A, MAX_A, STEP_A)):
        #for a in list(numpy.arange(MIN_A, MAX_A, STEP_A)) + [0.99]:
            max_k = 4 + 1 # Hacky... (Plus one for hypothetical new state)
            if a < 0.0 and not t + max_k * a > 0.0:
                continue
            if a >= 0.0 and not t > -a:
                continue
            if a > 1.0:
                continue
            if t == 0.0:
                continue

            #for i in xrange(60,61,1):
            #for i in xrange(60,150,1):
                #im = ChineseRProcess(ENVIRON, t, a)
                #arr.append(DyStrat(ENVIRON, im,
                                   #PigVIStrat(ENVIRON, im, PLUS=0, EXPLORER=False),
                                   #BossSAStrat(ENVIRON, im, -1), i))
            arr.append(
                PigVIStrat(ENVIRON,
                    ChineseRProcess(ENVIRON, t, a),
                    COLORS['red'], PLUS=0, EXPLORER=False))

    #for i in xrange(80,111,1):
    #for i in xrange(65,135,1):
    #for i in [2,3,5,8,15,25,50,100,500,5000,100000]:
        #im = ChineseRProcess(ENVIRON, 0.25, 0.0, i + 0.0)
        #arr.append(PigVIStrat(ENVIRON, im, PLUS=0, EXPLORER=False))
        #arr.append(DyStrat(ENVIRON, im,
                    #PigVIStrat(ENVIRON, im, PLUS=0, EXPLORER=False),
                    #BossSAStrat(ENVIRON, im, -1), i))
        #arr.append(ChainStrat(ENVIRON, im))


  #LTAStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['yellow']),

  # FIXME if needed
  #PigGreedyStrat(ENVIRON,
              #Dirichlet(ENVIRON),
              #COLORS['blue']),
  #PigGreedyStrat(ENVIRON,
              #ChineseRProcess(ENVIRON, THETA, ALPHA),
              #COLORS['grue2']),

