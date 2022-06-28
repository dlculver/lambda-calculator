import math

prime = 2

class monomial:
    ### defines monomials in Lambda algebra
    def __init__(self, const: int, lambdastr):
        self.constant = const
        if isinstance(lambdastr, str):
            temp = [int(x) for x in lambdastr[1:-1].split(',')]
        else:
            temp = lambdastr
        self.lambdas = temp
        ### constant refers to field scalar
        ### lambdas refers to a word in lambda generators
        ### just noticed that in our code, we haven't given the computer a way to handle strings like '(1,1,3)' since there is no constant term here. Need to add something which says that if the constant isn't present, then its 1.
        ### need to write something saying that if the constant is 0, then we convert the monomial to zero where zero is (0,[]).

    def __lt__(self, other):
        for i in range(min(len(self.lambdas), len(other.lambdas))):
            if self.lambdas[i] < other.lambdas[i]:
                return True
            if self.lambdas[i] >= other.lambdas[i]:
                return False
        return len(self.lambdas) < len(other.lambdas)

    def isadmissible(self):
        answer = True
        n = len(self.lambdas)
        for i in range(n-1):
            if 2*self.lambdas[i] < self.lambdas[i+1]:
                answer = False
        return answer

    def __mul__(self, other):
        constant = self.constant * other.constant % prime
        monom = self.lambdas + other.lambdas
        return monomial(constant, monom)



class polynomial:
    ### defines polynomial expressions in Lambda algebra
    def __init__(self, monoms: list):
        self.lambdastuff = monoms.copy()

    ## this method puts polynomials into lexicographic order
    def orderit(self):
        self.lambdastuff.sort()

    ## This method reduces the polynomial in that it adds coefficients of the same monomial appears more than once and reduces the coefficients mod p
    def reduce(self):
        self.orderit()
        lambda_instances  = self.lambdastuff
        for i in range(len(lambda_instances)):
            lambda_instances[i].constant = lambda_instances[i].constant % prime
        i=0
        while i < len(lambda_instances)-1:
            j = i+1
            while j < len(lambda_instances) and lambda_instances[i].lambdas == lambda_instances[j].lambdas:
                lambda_instances[i].constant = (lambda_instances[i].constant + lambda_instances[j].constant) % prime
                lambda_instances[j].constant = 0
                j += 1
            i = j ## starting where you stopped
                #lambda_instances.pop(i+1)
        new_lambda_instances = [monom for monom in lambda_instances if monom.constant != 0]
        self.lambdastuff = new_lambda_instances
        # for i in range(len(lambda_instances)):
        #     if lambda_instances[i].constant == 0:
        #         lambda_instances.pop(i)

    ## This method defines addition for polynomials in the characteristic
    def __add__(self, other):
        monoms = self.lambdastuff + other.lambdastuff
        poly = polynomial(monoms)
        poly.reduce()
        return poly

    def __mul__(self, other):
        L = []
        for i in range(len(self.lambdastuff)):
            for j in range(len(other.lambdastuff)):
                L.append(self.lambdastuff[i]*other.lambdastuff[j])
        return polynomial(L)

def parsing(lambdastring: str) -> polynomial:
    answer = []
    monoms = lambdastring.split('+')
    for mono in monoms:
        if mono.split('(')[0] == '':
            constant = 1
        else:
            constant = int(mono.split('(')[0])
        answer.append(monomial(constant, '('+mono.split('(')[1]))
    poly = polynomial(answer)
    poly.reduce()
    return poly

def admissmono(mono:monomial)-> polynomial:
        L = mono.lambdas
        l = len(L)
        if l <= 1:
            return polynomial([mono])
        elif mono.isadmissible():
            return polynomial([mono])
        else:
            for k in range(l-1):
                if 2*L[k] < L[k+1]:
                    i = L[k]
                    n = L[k+1]-2*L[k]-1
                    temp = []
                    M = monomial(mono.constant,L[:k])
                    N = monomial(1,L[k+2:])
                    for m in range(math.ceil(n-1/2)): # this for loop produces the lists
                        temp += [M*monomial(math.comb(n-m-1,m)%prime, [i+n-m,2*i+1+m])*N]
                    p = polynomial([])
                    for r in range(len(temp)):
                        p += admissmono(temp[r])
                    return p

def admisspoly(poly: polynomial) -> polynomial:
    monos = poly.lambdastuff
    admissiblemonos = [admissmono(mono) for mono in monos]
    p = polynomial([])
    for i in range(len(admissiblemonos)):
        p += admissiblemonos[i]
    return p

def diff(poly:polynomial) -> polynomial:
    p = polynomial([monomial(1,[-1])])
    q = admisspoly(p*poly)
    return q

# # def admissmono(mono: monomial) -> polynomial:
# #     L = mono.lambdas
# #     if len(L) <= 1:
# #         return polynomial([mono])
# #     elif 2*L[0] < L[1]:
# #         M = monomial(mono.constant, L[2:]) ## the tail end of the monomial, used for the recursion...
# #         i = L[0]
# #         n = L[1]-2*L[0]-1
# #         temp = []
# #         for j in range(int(n-1/2)): # this for loop produces the lists
# #             temp += [monomial(math.comb(n-j-1,j)%prime, [i+n-j,2*i+1+j])*M]
# #         p = polynomial([])
# #         for j in range(len(temp)):
# #             p += admissmono(temp[j])
# #         return p
# #     else: ## for when the admissibility condition is held
# #         return polynomial([monomial(mono.constant, [L[0]])])*admissmono(monomial(1, L[1:]))
#
# # def admissmono(mono: monomial) -> polynomial:
# #     L = mono.lambdas
# #     if len(L) <= 1:
# #         return polynomial([mono])
# #     elif 2*L[0] < L[1]:
# #         M = monomial(mono.constant, L[2:]) ## the tail end of the monomial, used for the recursion...
# #         i = L[0]
# #         n = L[1]-2*L[0]-1
# #         initiallambda = [] #lambda terms on the left hand most side in the return
# #         inductivemonomials = [] #monomials of length one less showing up in the return
# #         for j in range(int(n-1/2)): # this for loop produces the lists
# #             initiallambda += [polynomial([monomial(math.comb(n-j-1,j)%prime, [i+n-j])])]
# #             inductivemonomials += [monomial(1, [2*i+1+j])*M]
# #         p = polynomial([])
# #         for j in range(len(initiallambda)):
# #             p += initiallambda[j]*admissmono(inductivemonomials[j])
# #         return p
# #     else: ## for when the admissibility condition is held
# #         return polynomial([monomial(mono.constant, [L[0]])])*admissmono(monomial(1, L[1:]))
#
#
#
#
# p1= polynomial([monomial(1,[1,1,6])])
# p2 = polynomial([monomial(1, [1,1,6])])
#
# q = p1
#
# r = admisspoly(q)
#
# L = r.lambdastuff
#
# monos = [mono.lambdas for mono in L]
# print(monos)
#
# # p = monomial(1,[2,9,17])
# #
# # q = admissmono(p)
# #
# # L  = q.lambdastuff
# #
# # monos = [mono.lambdas for mono in L]
# # consts = [mono.constant for mono in L]
# # print(monos)
# # print(consts)
#
#
# # def admissify(poly: polynomial) -> polynomial:
#
#
#
#
#
#
# # p1 = parsing('(1)+(2)')
# # p2 = parsing('(3)+(4)')
# # p3 = p1 * p2
# #
# # L = p3.lambdastuff
# # monomials = [monom.lambdas for monom in L]
# # print(monomials)
#
#
# # p = p1
# # L = p.lambdastuff
# # constants = [monom.constant for monom in L]
# # monomials = [monom.lambdas for monom in L]
# # print(constants)
# # print(monomials)
# #
# # # print(poly1.constant)
# # # print(poly1.lambdastuff)
# # # print(poly2.constant)
# # # print(poly2.lambdastuff)
# #
# #
# #
# # # monomial1 = parsing('(1,1,3)')
# # # monomial2 = parsing('(1,2,2)')
# # #
# # # sum = monomial1 + monomial2
# # # monoms_of_sum = sum.lambdastuff
# # # lambdalist = [y.lambdas for y in monoms_of_sum]
# # # print(lambdalist)
# #
# # # monomial = monomial(1,'(1,1,3)')
# # # print(monomial.lambdas)
# # # print(monomial.isadmissible())
# #
# #
# # # lambdastring = '5(3,1,1)+7(2,1,3)+2(1,1,5)+3(1,2,3)'
# # # x = parsing(lambdastring)
# # # #x.orderit()
# # # print(type(x))
# # # lambdalist = [y.lambdas for y in x.lambdastuff]
# # # print(lambdalist)
