from annuities_certain import annuities_certain as ac

a1 = ac.Annuities_Certain(interest_rate=2, m=2)
r1 = a1.aan(2)
print(r1)
r1 = a1.an(2)
print(r1)



a1 = ac.Annuities_Certain(interest_rate=2, m=2)
r1 = a1.Iman(terms=2, payment=1, increase=1)
print(r1)


a2 = ac.Annuities_Certain(interest_rate=5, m=4)
r2 = a2.Iman(terms=10, payment=1, increase=1)
print(r2)

a3 = ac.Annuities_Certain(interest_rate=3.3, m=12)
r3 = a3.Iman(terms=8, payment=25 * 12, increase=2 * 12)
print(r3)


print()
a4 = ac.Annuities_Certain(interest_rate=5, m=12)
r4 = a4.Ian(terms=20, payment=2000 * 12, increase=400 * 12)
print(r4)

print()
a5 = ac.Annuities_Certain(interest_rate=2, m=2)
r5 = a5.Ian(terms=2, payment=1, increase=1)
print(r5)

r6 = a5.Iaan(terms=2, payment=1, increase=1)
print(r6)

r7 = a5.an(terms=-1)
print(r7)


'''
'''
''' cenas com crescimento geométrico ano-a-ano'''
print()
print()
a7= ac.Annuities_Certain(interest_rate=2, m=2)
r8 = a7.Gman(terms=2, payment=1, grow=1)
print(r8)



''' cenas com crescimento igual à taxa de juro'''
a7= ac.Annuities_Certain(interest_rate=2, m=2)
r8 = a7.Gan(terms=2, payment=1, grow=2)
print(r8)

r9 = a7.Gman(terms=2, payment=1, grow=1)
print(r9)


''' cenas com taxa de juro negativa'''
a8 = ac.Annuities_Certain(interest_rate=-2, m=2)
a9 = ac.Annuities_Certain(interest_rate=2, m=-2)

a1 = ac.Annuities_Certain(interest_rate=2, m=2)
r1 = a1.aan(2.1)
print(r1)
r1 = a1.aan(2)
print(r1)