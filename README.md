# Số Đề
crawler lottery result from [xoso](http://xoso.com.vn), after that, we can analysis the
result to find the best number to play.

the result will be saved in `*.database.json` file

## Install
```sh
pip3 install -r requirements.txt
```
or using pipenv
```sh
pipenv sync
```

## Run
```shell
python3 sode.py
```

you can also crawl the result of a specific day
```shell
python3 sode.py --from-date 01-01-2019 --to-date 10-01-2019
```
