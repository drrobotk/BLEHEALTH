clear
rm hr
touch hr
gnuplot liveplot.gnu &
sudo python -u watch$1_hrlive.py >> hr
