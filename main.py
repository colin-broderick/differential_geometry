from forms import *

dx1 = Form("x1")
dx2 = Form(2)
dx3 = Form(3, 5)

print(dx1)
print(dx2)

print(3*(2*dx2 ^ 3*dx1)+dx1)
