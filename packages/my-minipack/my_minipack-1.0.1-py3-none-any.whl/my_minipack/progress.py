from time import sleep
from time import time

def ft_progress(listy):
	start1 = time()
	for n in listy:
		start2 = time()
		yield n
		diff1 = (time() - start2) * len(listy)
		diff2 = time() - start1
		l = 20
		d = "=" * round(n * l / len(listy)) + ">" + " " * round(l - (n * l / len(listy)))
		print("ETA: {:.2f}s [ {:.2f}%][{}] {}/{} | elapsed time {:.2f}s".format(diff1, n / (len(listy) / 100), d, n + 1, len(listy), diff2), end='\r')

