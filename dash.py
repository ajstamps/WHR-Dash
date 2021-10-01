# This is used exclusively for testing. It calculates how long functions take to process.
import cProfile
import main
import pstats

cProfile.run('main.main()', 'file')
p = pstats.Stats('file')
p.sort_stats('time').print_stats(10)
