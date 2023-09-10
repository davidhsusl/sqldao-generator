create table t_sample
(
    id           bigint unsigned auto_increment comment "主鍵"
        primary key,
    col_var      varchar(100)  null comment "字串",
    col_text     text          null comment "長字串",
    col_tinyint  tinyint       null comment "微整數",
    col_int      int           null comment "整數",
    col_double   double(10, 2) null comment "浮點數",
    col_datetime datetime      null comment "時間"
);
