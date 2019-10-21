for index1 in range(4):
    for index2 in range(4):
        for index3 in range(4):
            for index4 in range(4):
                combination = [multiObjInputs[index1], multiObjInputs[index2],
                               multiObjInputs[index3], multiObjInputs[index4]]
                combination = map(str, combination)
                multiObjInputCombinations.append("".join(combination))
                if