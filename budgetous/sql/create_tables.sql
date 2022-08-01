create table account (
    id integer primary key,
    name text,
    beginning_balance decimal (11,3),
    kind varchar(100)  -- +/- or debit/credit
);

create table vendor (
    id integer primary key,
    name text
    -- location_id integer foreign key (location_id) references location (id),
);

create table tx (
    id integer primary key,
    amount decimal(11,3),
    vendor text,
    dt datetime,
    category text,
    tags text,
    account_id integer,
    seq_no integer,
    -- location_id integer foreign key (location_id) references location (id),  -- maybe later, or should location be attached to vendor?
    entry text,
    notes text,
    file_path text,
    bank_status text,  -- unreconciled, pending, cleared, reconciled, void
    foreign key (account_id) references account (id)
);

create table tag (
    id integer primary key,
    name text
);

create table tx_tag (
    id integer primary key,
    tx_id integer,
    tag_id integer,
    amount decimal(11,3),
    foreign key (tx_id) references tx (id),
    foreign key (tag_id) references tag (id)
);

