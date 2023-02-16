# # no se necesita conocer el valor de a ni de b para hallar la respuesta
# a = int(input('Ingrese a: '))
# b = int(input('Ingrese b: '))
# n = a
# x = b

# if ( (True and x % 2 == 0) or None ):
#     x += 1
#     print('x es impar', x)
# print('primer if', x)

# if ( (None and False) or ( n + 1 ) % 2  ==  0 ):
#     n += 1
#     print('n es par', n)
# print('2do if', n)

# if (n % 2 == 0 and x % 2 == 0) or (n % 2 != 0 and x % 2 != 0):
#     n += x
# else:
#     n += 1

# if (not None):
#     print('\'!Hola!\'' )

# if (n % 2 == 0):
#   print( 'Soy par' )
# elif (n % 2 == 1):
#   print('Soy impar' )



nombres=['Alexander', 'Michelle','Paolo',
           'Diego', 'Macarena', 'Alana', 
           'Joaquin', 'Sabrina']

ships= []
i = -1
for name in nombres:
  ships.append(name[:len(name)//2]+
     name)
  i -= 1

print(ships[:len(ships)//2])
print(ships[len(ships)//2:])
print(len(ships), len(nombres))
