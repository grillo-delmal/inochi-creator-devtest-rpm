#!/usr/bin/bash

sed -i "s/%define inochi_creator_ver .*/%define inochi_creator_ver $1/" inochi-creator-nightly.spec
sed -i "s/%define inochi_creator_dist .*/%define inochi_creator_dist $2/" inochi-creator-nightly.spec
sed -i "s/%define inochi_creator_short .*/%define inochi_creator_short $3/" inochi-creator-nightly.spec
