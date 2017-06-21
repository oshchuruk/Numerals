#import numeral, analysis, cro_numeral, table_transformation

num = input('input num - ')

ordinary, adj, zbirn = numeral.make_numeral(num)

print('ord -', ordinary)
print('adj -', adj)
print('zbirn -', zbirn)

#print(table_transformation.make_table(ordinary))

#print(analysis.analyze_form(num, analysis.numeral_to_digits(num)))