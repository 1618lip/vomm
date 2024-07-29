import vomm

# Take a string and convert each character to its ordinal value.
training_data = []
Dict = {}
train = "Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal."
for i, x in enumerate(train):
    training_data.append(i)
    Dict[i] = x
prefixes = []
keys = list(Dict.keys())
values = list(Dict.values())
for i in train:
    index = values.index(i)
    prefixes.append(keys[index])
    
#print(training_data)
my_model  = vomm.ppm()
my_model.fit(training_data, d=70)
t = ""
for x in my_model.generate_data(prefix=prefixes, length=50): 
    t += Dict[x]
print(t)