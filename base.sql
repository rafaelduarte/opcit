create table opcit(
    dbversion       integer(3) );

insert into opcit values (2);

create table tags (
    tag	     	    varchar(50) not null unique primary key
);

create table tags_ref (
    uid integer primary key autoincrement,
    tag varchar (50) references tags(tag),
    citekey varchar(30) references ref(citekey)
);

create  table ref (
    citekey         varchar(30) not null unique primary key,
    type            varchar(20),
    title           varchar(200),
    journal         varchar(100),
    language        varchar(50),
    citens          integer,
    issn            varchar(20),
    publisher       varchar(100),
    abstract        text,
    cited           integer,
    pages           varchar(15),    /*ISI's bp and ep will fail with discontinuous page ranges*/
    journabbrev     varchar(100),
    series          varchar(200),
    year            integer,
    month           varchar(10),
    volume          integer,
    number           varchar(10),    /*could be `spring', etc.*/
    address         varchar(200),
    url             varchar(200),
    jabb            varchar(32),
    booktitle       varchar(200),
    chapter         varchar(200),
    toc             varchar(4000),
    copyright       varchar(200),
    edition         varchar(20),
    howpublished    varchar(200),
    isbn            varchar(20),
    lccn            varchar(31),
    location        varchar(100),
    mrnumber        integer,
    organization    varchar(200),
    price           varchar(20),     /*may include currency sign...*/
    school          varchar(100)
    );

-- the integer should be replaced with serial for postgresql
-- for the uid field    
create  table author(
    uid             integer primary key autoincrement,
    citekey         varchar(30) not null references ref,
    name            varchar(100),
    number           integer,
    role            varchar(22),
    corresponding   char(1) default 'n' check(corresponding in ('n', 'y')),
    affiliation     varchar(200),
    address         varchar(200)
    );
    

CREATE VIEW refview AS
    SELECT ref.citekey, 
    ref."year", 
    author.name, 
    ref.title, 
    ref.journal
    FROM ref, author
    WHERE (((ref.citekey) = (author.citekey)) AND (author.number = 0));

-- anything below here are leftovers from Anton's design and not
-- used at all at the moment.


create  table note(
    uid             serial primary key,
    citekey         varchar(30) not null references ref,
    note            text,
    type            varchar(23)
    );

create  table keyword(
    uid             serial primary key,    
    note_key        integer references note(uid),
    keyword         varchar(40)
    );


create  table project_note(
    uid             serial primary key,
    citekey         varchar(30) not null references ref,
    note            varchar(4000),
    type            varchar(23)
    );

create  table project(    
    uid             serial primary key,
    project_note_key        integer references project_note(uid),
    keyword         varchar(40)
    );
    
create table journal_loc(
    uid             serial primary key,
    journal         varchar(100),
    start_vol       integer,
    end_vol         integer,
    library         varchar(100),
    lccn            varchar(200)
    );

create table resource_loc(
    uid             serial primary key,
    citekey         varchar(30) references ref,
    location        varchar(200)
    );
    
create table kw_node(
    keyword         varchar(40) primary key
    );
create table kw_link(
    uid             serial primary key,
    contained       varchar(40) references kw_node(keyword),
    container       varchar(40) references kw_node(keyword)
    );


