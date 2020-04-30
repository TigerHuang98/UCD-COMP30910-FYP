NRUNS=15
BASEPOWER=230

for N in 36864
do
  for g in 1 2
  do
    #4 8 12 16
    for tsub in 4 8 12 16 20 24 28 32 36 40 44 48
    do
      DUMMYTOTALENERGY=`cat  N${N}.dummy.energy.res | awk '{ sum += $4 } END { if (NR > 0) print sum / NR }'`
      DUMMYETIME=`cat  N${N}.dummy.time.res | awk '{ sum += $7 } END { if (NR > 0) print sum / NR }'`

      ETIME=`grep "N " N${N}.G${g}.Tsub${tsub}.time.res | awk '{ sum += $7 } END { if (NR > 0) print sum / NR }'`
      TENERGYALL=`cat N${N}.G${g}.Tsub${tsub}.energy.res | awk '{ print $4 }'`
      TENERGY=`echo "$TENERGYALL / $NRUNS" | bc -l`
      DIFFE=`awk '{print ($1-$2)}' <<< "$TENERGY $DUMMYTOTALENERGY"`
      DIFFT=`awk '{print ($1-$2)}' <<< "$ETIME $DUMMYETIME"`
      DENERGY=`echo "$DIFFE - $BASEPOWER * $DIFFT" | bc`
      echo "N=$N, G=$g, T=$tsub, DummyTotalEnergy(J)=$DUMMYTOTALENERGY, Time(s)=$DIFFT, TotalEnergy(J)=$TENERGY, DynamicEnergy(J)=$DENERGY"
    done
  done
done