#!/bin/bash

main_path=/data/data/com.termux/files/home/storage/shared/notes
journal_org_file_path="${main_path}/notes/journal.org"
current_date_str=`date +"%Y-%m-%d"`
current_time_str=`date +"%H-%M"`
entry_file_path="${main_path}/entries/${current_date_str}-bryce-eryn-caine-journal-${current_time_str}.txt"

# Copy journal.org to new entry file
cp $journal_org_file_path $entry_file_path

# Clear contents of journal.org
truncate -s 0 $journal_org_file_path

# Enrich journal entry
# 
author="author: Bryce Caine"
entry_date="date: $current_date_str"
tags="tags: journal"
location=$(termux-location)
weather=$(curl http://wttr.in/?format=%C+%t+%h+humidity+%w+wind+%p+precip)
echo -e "---\n$author\n$entry_date\n$tags\n$location\n$weather\n---\n$(cat $entry_file_path)" > $entry_file_path

termux-open --choose $entry_file_path

# python .termux/tasker/create_journal_entry.py

