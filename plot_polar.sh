#!/bin/bash

DATE=`date -u +"%F %H:%MZ"`


#FFT_SIZE=1024

while getopts fc:sF: option
do
 case "${option}"
 in
# f) FTT_SIZE=${OPTARG};;
# c) FFT_COUNT=${OPTARG};;
# s) SATELLITE=${OPTARG};;
 F) FILE=$OPTARG;;
 esac
done

rm $FILE
rm $FILE.angles
rm $FILE.final

for i in `seq 0 71`;
        do
                ((ANGLE= $i * 5))
                echo $ANGLE
		echo -n $ANGLE>>$FILE.angles; echo " ">>$FILE.angles
		python set_angle_and_measure.py -F $FILE -a $ANGLE 
        done    


#./fft_raw2asc $FFT_FILE  36
python float_converter.py -i $FILE -o $FILE.asc
paste $FILE.angles $FILE.asc > $FILE.final
#
echo "Plotting results..."
gnuplot <<EOF

set angles degrees
set polar
set grid polar 15. 
unset border
unset param
set title "Antenna Pattern" 
set style data line
set rrange [-100:0]
unset xtics
set term pngcairo background rgb 'white'
set output "$FILE_$DATE.png"
plot "$FILE.final" 

EOF
echo "Done"
