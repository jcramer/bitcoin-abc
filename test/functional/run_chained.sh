
echo 10
python3 chained_transactions.py 10 1 > test10
cat test10 | grep GetBlkT
cat test10 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 25
python3 chained_transactions.py 25 1 > test25
cat test25 | grep GetBlkT
cat test25 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 30
python3 chained_transactions.py 30 1 > test30
cat test30 | grep GetBlkT
cat test30 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 35
python3 chained_transactions.py 35 1 > test35
cat test35 | grep GetBlkT
cat test35 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 45
python3 chained_transactions.py 45 1 > test45
cat test45 | grep GetBlkT
cat test45 | grep CreateNewBlock | grep -v '0 updated descendants' | grep -v ' 0 fees'

echo 50
python3 chained_transactions.py 50 1 > test50
cat test50 | grep GetBlkT
cat test50 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 75
python3 chained_transactions.py 75 1 > test75
cat test75 | grep GetBlkT
cat test75 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 100
python3 chained_transactions.py 100 1 > test100
cat test100 | grep GetBlkT
cat test100 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 200
python3 chained_transactions.py 200 1 > test200
cat test200 | grep GetBlkT
cat test200 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 300
python3 chained_transactions.py 300 1 > test300
cat test300 | grep GetBlkT
cat test300 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 400
python3 chained_transactions.py 400 1 > test400
cat test400 | grep GetBlkT
cat test400 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 500
python3 chained_transactions.py 500 1 > test500
cat test500 | grep GetBlkT
cat test500 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v ' 0 fees'

echo 600
python3 chained_transactions.py 600 1 > test600
cat test600 | grep GetBlkT
cat test600 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v '0 fees'

echo 700
python3 chained_transactions.py 700 1 > test700
cat test700 | grep GetBlkT
cat test700 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v '0 fees'

echo 800
python3 chained_transactions.py 800 1 > test800
cat test800 | grep GetBlkT
cat test800 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v '0 fees'

echo 900
python3 chained_transactions.py 900 1 > test900
cat test900 | grep GetBlkT
cat test900 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v '0 fees'

echo 1000
python3 chained_transactions.py 1000 1 > test1000
cat test1000 | grep GetBlkT
cat test1000 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v '0 fees'

echo 1500
python3 chained_transactions.py 1500 1 > test1500
cat test1500 | grep GetBlkT
cat test1500 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v '0 fees'

echo 2000
python3 chained_transactions.py 2000 1 > test2000
cat test2000 | grep GetBlkT
cat test2000 | grep CreateNewBlock | grep -v ' 0 updated descendants' | grep -v '0 fees'
