#!/bin/bash

DEBUG=0

SEAT_FILENAME=testseat.txt
STDT_FILENAME=teststudent.csv
MAX_NUM_SEATS=500
ITERATIONS=500

ALGORITHMS=(randomassign chunkincrease consecdivide)
LENGTH=${#ALGORITHMS[@]}
STATS=(0 0 0)

function clean() {
	echo "FORCE EXITING..."
	rm $SEAT_FILENAME $STDT_FILENAME
	exit 1
}
trap clean INT

# EVALUATE
for i in $(seq 1 $ITERATIONS); do
	if [[ $DEBUG -eq 0 ]]; then
		echo -ne "\033[1K"
		echo -ne "\rRunning test $i..."
	fi
	NUM_SEATS=$((1 + $RANDOM % MAX_NUM_SEATS))
	NUM_STDTS=$((1 + $RANDOM % NUM_SEATS))

	python3 gen_seats.py $NUM_SEATS --add_flags --filename $SEAT_FILENAME
	python3 gen_students.py $NUM_STDTS --add_flags --filename $STDT_FILENAME

	if [[ $DEBUG -eq 1 ]]; then
		echo Seats: $NUM_SEATS
		echo Students: $NUM_STDTS
	fi

	for alg in ${!ALGORITHMS[@]}; do 
		RESULT=$(../lupseat $STDT_FILENAME $SEAT_FILENAME --eval --nosave --algorithm ${ALGORITHMS[$alg]})
		STATS[$alg]=$(echo "${STATS[$alg]} $RESULT" | awk '{print $1 + $2}')

		if [[ $DEBUG -eq 1 ]]; then
			echo Algorithm: ${ALGORITHMS[$alg]}: $RESULT
		fi
	done
done

# PRINT RESULTS
echo "Results over ${ITERATIONS} iterations:"
for alg in ${!ALGORITHMS[@]}; do 
	echo ${ALGORITHMS[$alg]}: $(echo "${STATS[$alg]} $ITERATIONS" | awk '{print $1 / $2}')
done


# CLEAN
rm $SEAT_FILENAME $STDT_FILENAME
