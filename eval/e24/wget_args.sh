#! /bin/bash
# Print out all long and short valued and unvalued args of wget

echo "===Valued long options==="
man wget | col -b | egrep '^\W{7}--[a-zA-Z0-9_-]+=\w+' | sed 's/^[ \s\t]*//g' | sed 's/=.*//g' | sed -E 's/^[-]+//g'

echo "===Value-less long options==="
man wget | col -b | egrep '^\W{7}--[a-zA-Z0-9_-]+$' | sed 's/^[ \s\t]*//g' | sed -E 's/^[-]+//g'

echo "===Valued short options==="
man wget | col -b | egrep '^\W{7}-\w+$' | sed 's/^[ \s\t]*//g' | tr -d '-'

echo "===Value-less short options==="
man wget | col -b | egrep '^\W{7}-\w+ \w+' | sed 's/^[ \s\t]*//g' | sed 's/ .*//g' | tr -d '-'
