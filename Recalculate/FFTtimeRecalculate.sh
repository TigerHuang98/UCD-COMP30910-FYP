NRUNS=15
BASEPOWER=230

for N in 20480 #35840
do
  for g in 1 2 3 4 6 8 12 16 24 48
  do
    #4 8 12 16
#    for tsub in 5 6 #3 #8 #12 #16 #20 24 #28 32 36 40 44 48
    for (( tsub=1 ; tsub <= 48/g ; tsub+=1));
    do
      DUMMYTOTALENERGYALL=`cat N${N}.dummy.energy.res | awk '{ print $4 }'`
      DUMMYTOTALENERGY=`echo "$DUMMYTOTALENERGYALL / $NRUNS" | bc -l`
      ETIME=`cat N${N}.G${g}.Tsub${tsub}.time.res | grep 'time' | awk '{print $3}' | sed 's/time(sec)=//' | sed 's/,//' | awk '{ sum += $1 } END { if (NR > 0) print sum / NR }'`
      TENERGYALL=`cat N${N}.G${g}.Tsub${tsub}.energy.res | awk '{ print $4 }'`
      TENERGY=`echo "$TENERGYALL / $NRUNS" | bc -l`

      DIFFE=`awk '{print ($1-$2)}' <<< "$TENERGY $DUMMYTOTALENERGY"`
      DENERGY=`echo "$DIFFE - $BASEPOWER * $ETIME" | bc`

      echo "N=$N, G=$g, T=$tsub, DummyTotalEnergy(J)=$DUMMYTOTALENERGY, Time(s)=$ETIME, TotalEnergy(J)=$TENERGY, DynamicEnergy(J)=$DENERGY"

    done
  done
done
