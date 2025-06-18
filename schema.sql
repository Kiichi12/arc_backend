create type roles as enum ('guest', 'student', 'faculty', 'admin');

create table users (
    id serial primary key,
    username varchar(100) unique not null,
    email varchar(100) unique not null,
    password_hash text not null,
    role roles not null default 'student',
    created_at timestamp default now()
);

create table folders (
    id serial primary key,
    name varchar(100) not null,
    parent_id integer references folders(id) on delete cascade,
    owner_id integer references users(id) on delete set null,
    created_at timestamp default now(),
    updated_at timestamp
);

create type status_type as enum ('Accepted', 'Rejected', 'Pending');

create table files (
    id serial primary key,
    name varchar(100) not null,
    file_url text not null,
    parent_id integer not null references folders(id) on delete cascade,
    owner_id integer references users(id) on delete set null,
    mime_type varchar(100) not null,
    size bigint,
    description text,
    open_count integer default 0,
    status status_type not null default 'Pending',
    created_at timestamp default now(),
    updated_at timestamp
);

create table file_ratings (
    user_id integer references users(id) on delete cascade,
    file_id integer references files(id) on delete cascade,
    rating integer not null default 0,
    primary key (user_id, file_id)
);

create table comments (
    id serial primary key,
    user_id integer references users(id) on delete cascade,
    file_id integer references files(id) on delete cascade,
    content text not null,
    commented_at timestamp default now()
);

create table user_reports (
    user_id integer references users(id) on delete cascade,
    file_id integer references files(id) on delete cascade,
    content text not null,
    primary key (user_id, file_id)
);

-- create table bookmarks (
--     user_id integer references users(id) on delete cascade,
--     file_id integer references files(id) on delete cascade,
--     primary key (user_id, file_id)
-- );

create table favourites (
    user_id integer references users(id) on delete cascade,
    file_id integer references files(id) on delete cascade,
    primary key (user_id, file_id)
);

create table tags (
    id serial primary key,
    name varchar(100) unique not null
);

create table file_tags_map (
    file_id integer references files(id) on delete cascade,
    tag_id integer references tags(id) on delete cascade,
    primary key (file_id, tag_id)
);

create table forums (
    id serial primary key,
    started_by integer references users(id) on delete cascade,
    started_at timestamp default now(),
    topic text not null
);

create table replies (
    id serial primary key,
    posted_by integer references users(id) on delete cascade,
    forum_id integer references forums(id) on delete cascade,
    content text not null,
    posted_at timestamp default now()
);

create type login_status as enum ('Failed', 'Success');

create table login_logs (
    id serial primary key,
    user_id integer references users(id) on delete cascade,
    status login_status not null,
    ip_address varchar(50),
    login_at timestamp default now()
);