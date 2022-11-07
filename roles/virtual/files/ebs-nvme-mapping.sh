#!/bin/bash
# https://github.com/oogali/ebs-automatic-nvme-mapping/pull/3

if [[ -x /usr/sbin/nvme ]] && [[ -b ${1} ]]; then
  nvme_link=$( \
    /usr/sbin/nvme id-ctrl --raw-binary "${1}" | \
    /usr/bin/cut -c3073-3104 | \
    /bin/sed 's/^\/dev\///g'| \
    /bin/sed 's/^sd/xvd/'| \
    /usr/bin/tr -d '[:space:]' \
  );
  echo $nvme_link;
fi
