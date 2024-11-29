# Notes to be used for development
Look into using pipreqs for the apps requirements. It can make a text file that you can run with ```pip install -r requirements.txt``` and you will not need to setup and install all the needed apps like Flask.

Also look into using Github's Wiki pages for how to use the app and link it in the Readme just in case.

## Something like the following:
```
pip install pipreqs
pipreqs .
```
It will generate the following requirements.txt file:
```
requests==2.23.0
beautifulsoup4==4.9.1
```
which you can install with:
```
pip install -r requirements.txt
```
