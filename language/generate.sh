echo "MUST BE RUN ON A FRESH REV!"
(
cd ../data/monsters
sed -i 's/genMonster(\"\([^"]*\)\"/genMonster\(_\(\"\1\"\)/g' */*.py */*/*.py */*/*/*.py */*/*/*/*.py */*/*/*/*/*.py 
sed -i 's/genMonster(\(.*\), \"\([^"]*\)\"/genMonster(\1, _(\"\2\")/g' */*.py */*/*.py */*/*/*.py */*/*/*/*.py */*/*/*/*/*.py 
)
xgettext -k_l:2 -k_lp:2,3 -o en_EN.po ../*.py ../*/*.py ../*/*/*.py ../*/*/*/*.py ../*/*/*/*/*.py

(
cd ../data/monsters
hg revert .
)

# Append item stuff
python2 generate_items.py >> en_EN.po

# Important, otherwise non-English characters will display as fucked up in non-English translations. This can, for no reason be anything other than UTF9 in any translation.
sed -i 's/CHARSET/UTF-8/' en_EN.po
