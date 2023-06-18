# /bin/bash
echo "starting spyder laucher..."
sleep 5
python3 ./0_spyder/main_laucher.py
echo "spyder finished!"
sleep 5

echo "start merging..."
sleep 5
python3 ./1_merger/1_merge_news.py
echo "merge finished!"
sleep 5

echo "start picking sample..."
sleep 5
python3 ./2_modeler/0_pick_sample.py
echo "sample generated!"
sleep 5

echo "modelling and checking..."
sleep 5
python3 ./2_modeler/1_ldamodeling.py
sleep 5

echo "comparing..."
sleep 5
python3 ./3_checker/0_model_compare.py