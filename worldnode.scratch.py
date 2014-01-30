for action in range(M):
            self.actions.append([])
            pabsorb = self.prob_absorb(N, action)
            nodes_left = action + 1
            while nodes_left > 0:
                picked = len(self.actions[action]) - (1 if pabsorb == 0.0 else 0)
                pnormal = (1 - pabsorb) / (self.N - 1 - picked)
                r = round(random.random(), 2)
                if r < pabsorb:
                    self.actions[action].append(absorber)
                    pabsorb = 0.0
                else:
                    print "not absorb"
                    if not self.find_target(action, pabsorb, pnormal, r):
                        continue # try again
                nodes_left -= 1

