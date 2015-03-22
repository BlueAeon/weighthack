# use calc.sh to generate moving averages
reset

# wxt
#set terminal wxt size 350,262 enhanced font 'Verdana,10' persist
set terminal wxt enhanced font 'Verdana,10' persist

set xdata time
set grid
set border linewidth 1.5
set pointsize 1.5
set style data linespoints
set timefmt "%Y-%m-%d"
set ylabel "lbs"
set ytics nomirror
set yrange [190:200]
set y2range [1200:3900]
set y2label "kcal"
set y2tics nomirror
set xtics nomirror
plot [:][:] 'final_data' using 1:2 axes x1y1 title "Weight (lbs)" with lines, 'final_data' using 1:4 axes x1y2 title "Intake (kcal)" with lines, 'final_data' using 1:3 axes x1y1 title "Average Weight (lbs)", 'final_data' using 1:6 axes x1y2 title "TDEE (kcal)"

