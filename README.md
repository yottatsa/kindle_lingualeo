## LinguaLeo API

Implementation from https://raw.githubusercontent.com/relaxart/LeoPort/a2592025284d5d179168e096e4aa1fc259c6b905/service.py

### URLs:

    https://api.lingualeo.com/api/login
    https://api.lingualeo.com/addword
    https://lingualeo.com/userdict/json?page=
    https://api.lingualeo.com/gettranslates?word=

## Kindle Schema

    "SELECT * "
    "FROM lookups "
    "INNER JOIN words ON words.id = lookups.word_key "
    "INNER JOIN book_info ON book_info.id = lookups.book_key "
    "WHERE words.lang = 'en'")

0. CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F:272634:13
1. en:Vanderbilt
0. CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F
0. B0053VMNY2
0. 272634
0. And when someone asked him why he went and bought himself such a dinky little yacht, he just looked at the guy and said, ‘What do you think I am, a Vanderbilt?'
0. 1450695976915
0. en:Vanderbilt
0. Vanderbilt
0. Vanderbilt
0. en
0. 0
0. 1450695976901
0. empty
0. CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F
0. B000FBJCJE
0. CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F
0. en
0. Snow Crash (Bantam Spectra Book)
0. Stephenson, Neal


### Lookups

    CREATE TABLE LOOKUPS (
        id TEXT PRIMARY KEY NOT NULL, # CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F:272634:13
        word_key TEXT, # en:Vanderbilt
        book_key TEXT, # CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F
        dict_key TEXT, # B0053VMNY2
        pos TEXT, # 272634
        usage TEXT, # And when someone asked him why he went and bought himself such a dinky little yacht, he just looked at the guy and said, ‘What do you think I am, a Vanderbilt?'
        timestamp INTEGER DEFAULT 0 # 1450695976915
    );

### Words

    CREATE TABLE WORDS (
        id TEXT PRIMARY KEY NOT NULL, # en:Vanderbilt
        word TEXT, # Vanderbilt
        stem TEXT, # Vanderbilt
        lang TEXT, # en
        category INTEGER DEFAULT 0, # 0 is new, 100 is mastered
        timestamp INTEGER DEFAULT 0, # 1450695976901
        profileid TEXT
    );
    
### Book info

    CREATE TABLE BOOK_INFO (
        id TEXT PRIMARY KEY NOT NULL,
        asin TEXT,
        guid TEXT,
        lang TEXT,
        title TEXT,
        authors TEXT
    );
    CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F|B000FBJCJE|CR!D6DH2Q917N5WQ2784ZJPRGQ3Q7WJ:C8F6A18F|en|Snow Crash (Bantam Spectra Book)|Stephenson, Neal

### Dict info
    
    CREATE TABLE DICT_INFO (
        id TEXT PRIMARY KEY NOT NULL,
        asin TEXT,
        langin TEXT,
        langout TEXT
    );
    B0053VMNY2|B0053VMNY2|en|en

### Metadata

    CREATE TABLE METADATA (
        id TEXT PRIMARY KEY NOT NULL,
        dsname TEXT,
        sscnt INTEGER,
        profileid TEXT
    );
    BOOK_INFO|BOOK_INFO|700|
    DICT_INFO|DICT_INFO|10|
    WORDS|WORDS|704|
    LOOKUPS|LOOKUPS|708|

### Version

    CREATE TABLE VERSION (
        id TEXT PRIMARY KEY NOT NULL,
       dsname TEXT,
       value INTEGER
    );
    WORDS|WORDS|1
    LOOKUPS|LOOKUPS|0
    DICT_INFO|DICT_INFO|0
    BOOK_INFO|BOOK_INFO|0
    METADATA|METADATA|1
    
### Glossary

#### ASINs
Amazon Standard Identification Numbers (ASINs)
https://www.amazon.com/gp/seller/asin-upc-isbn-info.html