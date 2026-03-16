def sqrt(n, epochs=20): 
    '''
    计算n的平方根
    '''
    root = n / 2 
    for i in range(epochs): 
        root = (root + n / root) / 2 
    return root  

class Fraction: 
    def __init__(self, top, bottom): 
        self.num = top 
        self.den = bottom 

    def show(self): 
        print(f'{self.num}/{self.den}') 

    def __str__(self): 
        return f'{self.num}/{self.den}'
    
    @staticmethod
    def gcd(m, n):
        while n: 
            m, n = n, m % n 
        return m 

    def __add__(self,other): 
        new_num = self.num * other.den + self.den * other.num 
        new_den = self.den * other.den 
        common = Fraction.gcd(new_num, new_den) 
        return Fraction(new_num // common, new_den // common) 

    def __eq__(self, other):
        return self.num * other.den == self.den * other.num

if __name__ == '__main__':
    print(sqrt(2))  # 1.414213562373095  
    f = Fraction(1, 2) 
    print(f.num) 
    print(f.den)
    f.show() 
    print(f) 
    g = f + Fraction(1, 4) 
    print(g) 
    print(f == g) 
    print(f == Fraction(1, 2)) 

