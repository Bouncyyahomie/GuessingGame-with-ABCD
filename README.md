# GuessingGame-with-ABCD

                "_id" : 666,
                "Question" : ['', '', '', ''],
                "Answer" : ['', '', '', ''],
                "Count" : -1,
                "Win" : False
                
Database course homework using Flask and MongoDB

Jakkrathorn Srisawad 6210545432


## Usage

Building project in container using command:

```
docker-compose up -d 
```

game is running in **https://localhost/**

Display web server log using command:

```
docker-compose logs -f --tail 10 web
```

Stop project in container using command:

```
docker-compose down -v 
```

## How to play
1. click the alphabet button to create and question.
2. guess the letter one by one.
3. count show how many times do your guessing wrong.
4. answer show what do you guess right.
5. after you guess all letters play again button will appear.
