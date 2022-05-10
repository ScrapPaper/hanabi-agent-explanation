cp -n hanabi_game.cc hanabi_game.cc.old
cp -n util.h util.h.old
cat hanabi_game.cc.old | tr "\n" "\r" | \
        sed -r  -e "s/(if \(num_players_ < 4\) \{\r\s*return)[^;]*([^r]*return)[^;]*/\1 2\2 2/g" \
                -e "s/(kInformationTokens =)[^;]*/\1 3/g" \
                -e "s/(kLifeTokens =)[^;]*/\1 1/g" | \
        tr "\r" "\n" > hanabi_game.cc
sed -r "s/(kMaxNumColors =)[^;]*/\1 2/g" util.h.old > util.h

cd ../../rlcc
cp -n r2d2_actor.cc r2d2_actor.cc.old
sed -r  -e "s/(b.size\(\) ==)[^)]*/\1 10/g" \
        -e "s/(c <)[^;]*/\1 2/g" \
        r2d2_actor.cc.old > r2d2_actor.cc
cd ..
