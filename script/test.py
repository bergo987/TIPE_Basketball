for t in range(tmax):
    if t % T/2 : 
        print("gauche \n")
    elif t % T :
        print("droite\n")
    else: 
        print("ni gauche ni droite")