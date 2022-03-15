cp -n belief_model.py belief_model.py.old
cp -n create.py create.py.old
cp -n eval.py eval.py.old
cp -n selfplay.py selfplay.py.old
cp -n train_belief.py train_belief.py.old
cp -n utils.py utils.py.old
mv legacy_agent.py legacy_agent.py.old
sed -r  -e "s/25/10/g" \
        -e "s/35/17/g" \
        -e "s/(hand_size =) 5/\1 2/g" \
        belief_model.py.old > belief_model.py
sed -r "s/(hand_size=)./\12/g" create.py.old > create.py
sed -r "s/(if s ==)[^]]*/\1 10/g" eval.py.old > eval.py
sed -r  -e "s/(agent = r2d2\.R2D2Agent)/print(\"feature_size:\", games[0].feature_size(args.sad))\n    \1/g" \
        -e "s/^( *)5/\12/g" \
        selfplay.py.old > selfplay.py
sed -r  -e "s/^( *)5/\12/g" \
        -e "s/^( *)25/\110/g" \
        train_belief.py.old > train_belief.py
sed -r  -e "s/(\"hand_size\",)[^)]*/\1 2/g" \
        -e "s/(agent = r2d2\.R2D2Agent)/print(\"feature_size:\", game.feature_size(cfg[\"sad\"]))\n    \1/g" \
        utils.py.old > utils.py
