#!/bin/bash

wget -c http://images.cocodataset.org/zips/train2014.zip
unzip train2014.zip
rm train2014.zip

wget -c http://images.cocodataset.org/annotations/annotations_trainval2014.zip
unzip annotations_trainval2014.zip
rm annotations_trainval2014.zip

mkdir coco_small

echo '#!/bin/bash

# https://stackoverflow.com/questions/71211999/grab-random-files-from-a-directory-using-just-bash

shopt -s failglob

n=${1:?} glob=${2:?} source=${3:?} dest=${4:?}
declare -i rand
IFS=

[[ -d "$source" ]]
[[ -d "$dest" && -w "$dest" ]]

cd "$dest"
dest=$PWD
cd "$OLDPWD"
cd "$source"

printf '%s\0' $glob |
shuf -zn "$n" |
xargs -0 cp -t "$dest"' > cp_rand.sh

chmod 755 cp_rand.sh

# randomly copy 500 images from the coco dataset
./cp_rand.sh 500 '*.jpg' train2014 coco_small

# make the json readable
cat annotations/captions_train2014.json | python -m json.tool > captions.json

# find captions for the 500 images
python find_captions.py coco_small

