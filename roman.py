class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        sum = 0  
        for index in range(len(s)): 
            if s[index] == 'I': 
                 sum += 1 
            elif s[index] == 'V': 
                 sum += 5  
            elif s[index] == 'X': 
                 sum += 10 
            elif s[index] == 'L': 
                 sum += 50  
            elif s[index] == 'C': 
                 sum += 100  
            elif s[index] == 'D': 
                sum += 500 
            elif s[index] == 'M': 
                 sum += 1000  
        for index in range(len(s)-1): 
            if s[index] == 'I' and s[index+1] != 'I': 
                if s[index+1] == 'V': 
                    sum = 5 - (sum+1)  
                elif s[index+1] == 'X': 
                     sum = 10 - (sum+1) 
                elif s[index+1] == 'L': 
                     sum = 50 - (sum+1) 
                elif s[index+1] == 'C': 
                     sum = 100 - (sum+1) 
                elif s[index+1] == 'D': 
                     sum = 500 - (sum+1) 
                elif s[index+1] == 'M': 
                     sum = 1000 - (sum+1) 
            elif s[index] == 'V' and s[index+1] != 'V': 
                if s[index+1] == 'X': 
                     sum = 10 - (sum+5) 
                elif s[index+1] == 'L': 
                     sum = 50 - (sum+5) 
                elif s[index+1] == 'C': 
                     sum = 100 - (sum+5) 
                elif s[index+1] == 'D': 
                     sum = 500 - (sum+5) 
                elif s[index+1] == 'M': 
                     sum = 1000 - (sum+5) 
            elif s[index] == 'X' and s[index+1] != 'X': 
                if s[index+1] == 'L': 
                     sum = 50 - (sum+10) 
                elif s[index+1] == 'C': 
                     sum = 100 - (sum+10) 
                elif s[index+1] == 'D': 
                     sum = 500 - (sum+10) 
                elif s[index+1] == 'M': 
                     sum = 1000 - (sum+10) 
            elif s[index] == 'L' and s[index+1] != 'L': 
                if s[index+1] == 'C': 
                     sum = 100 - (sum+50) 
                elif s[index+1] == 'D': 
                     sum = 500 - (sum+50) 
                elif s[index+1] == 'M': 
                     sum = 1000 - (sum+50) 
            elif s[index] == 'C' and s[index+1] != 'C':
                if s[index+1] == 'D': 
                     sum = 500 - (sum+100) 
                elif s[index+1] == 'M': 
                     sum = 1000 - (sum+100) 
            elif s[index] == 'D' and s[index+1] != 'D':
                if s[index+1] == 'M': 
                     sum = 1000 - (sum+500) 
            #if blah[index] == 'M' and blah[index+1] != 'M': 

        return sum