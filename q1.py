# write a python program to 
# 1) convert the sentence to lower case and split it into words 
# 2) count the frequency of each word using a dictionary
# 3) print the frequency dictionary as an output

word = input("Enter the Sentence: ")
words = word.lower().split()
 
frequency = {}
for word in words:
    if word in frequency:
        frequency[word] += 1
    else:
        frequency[word] = 1 
print(frequency)
