create table t_sample
(
    id               bigint unsigned auto_increment comment 'ID'
        primary key,
    column_char      char(32)      null comment 'CHAR',
    column_varchar   varchar(32)   null comment 'VARCHAR',
    column_text      text          null comment 'TEXT',
    column_json      json          null comment 'JSON',
    column_tinyint   tinyint       null comment 'TINYINT',
    column_int       int           null comment 'INT',
    column_double    double(20, 8) null comment 'DOUBLE',
    column_datetime  datetime      null comment 'DATETIME',
    column_timestamp timestamp     null comment 'TIMESTAMP'
)
    comment 'TEST';