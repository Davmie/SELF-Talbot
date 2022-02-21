lib/libmath.so: src/library.c src/library.h
	$(CC) -fPIC -shared $< -o $@ -lm -lgsl -lgslcblas
