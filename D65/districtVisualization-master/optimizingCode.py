# This script includes code for a Python technique called profiling.
# Profiling essentially analyzes the function calls within a specific function
# and produces an output showing a break down of the function calls within a function
# and the time it took to run those calls

########################################################
# This piece of code is necessary to profile a function
import cProfile, pstats, io

def profile(fnc):

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner
########################################################


# Then if I have a function like this one, I just put @profile above its definition,
# and just run the script/function as usual, and one output like this should appear:
#          3 function calls in 0.000 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000    0.000    0.000 C:/Users/Ayobami Bolaji/Documents/IEMS_D65_Research_SQ19/nextVersion/districtVisualization-master/optimizingCode.py:30(squareListEls)
#         1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

# Of course I only squared five list elements, so it should run very quickly and that's why it says
# zero seconds, because the time it took to do the computation was negligible

@profile
def squareListEls(givenList):
    for index in range(len(givenList)):
        givenList[index] = givenList[index] * givenList[index]

    return givenList

print(squareListEls([1, 2, 3, 4, 5]))

