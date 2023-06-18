#echo "sleeping..."
#sleep 5
#echo "merging..."
#python3 ./1_merger/1_merge_news.py
#sleep 5
#echo "picking sample..."
#python3 ./2_modeler/0_pick_sample.py
##sleep 5
#echo "modelling and checking..."
python3 ./2_modeler/1_ldamodeling.py
#sleep 5
#echo "comparing..."
#python3 ./3_checker/0_model_compare.py