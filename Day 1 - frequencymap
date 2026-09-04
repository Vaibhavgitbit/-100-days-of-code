#run in py --- Approach 1: Brute Force Nested Loops (Slow - O(N^2))
L1 = [2,3,4,5,6,6,7,6,5,4,4,3,3,8]
L2 = [2,3,4,5,5,7,6,5,3,3,3,2,3,5]
for num in L1:
    count = 0
    for x in L2:
        if x == num:
            count += 1
    # print(count) # Commending this out to keep terminal clean

# ---- Approach 2: Optimized Frequency Map using Hashing/with Dictionary (Fast - O(N))
num = [2,3,4,5,6,6,7,6,5,4,4,3,3,2]
freq_map = {}
for i in range(len(num)):
    # .get() looks up the number; if it doesn't exist, it defaults to 0 or what you want as default
    freq_map[num[i]] = freq_map.get(num[i], 0) + 1

# print("Optimized Frequency Map:", freq_map)
# "if you test it please remove # from print lines"
