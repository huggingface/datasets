#!/bin/bash
# Generate the archives in test_data/archives.

ROOT=`dirname $0`
PWD=`pwd`
ABSROOT="${PWD}/${ROOT}"
DEST="archives"
F1="6pixels.png"
F2="foo.csv"

cd "${ROOT}/test_data"
tar -cvf "${DEST}/arch1.tar"  ${F1} ${F2}
tar -zcvf "${DEST}/arch1.tar.gz" ${F1} ${F2}
zip "${DEST}/arch1.zip" ${F1} ${F2}
gzip -cv ${F2}  > "${DEST}/foo.csv.gz"

# Archive with absolute link.
# PWD needs to be at / for this to work.
cp -L "${F2}" "/tmp/${F2}"
cd /
tar --hard-dereference --absolute-names -cvf "${ABSROOT}/test_data/${DEST}/absolute_path.tar" "/tmp/${F2}"
