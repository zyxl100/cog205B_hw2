set -euo pipefail
ZIP_URL="https://raw.githubusercontent.com/joachimvandekerckhove/cogs205b-s26/main/modules/02-version-control/files/data.zip"
TODAY="$(date +%F)"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="${REPO_ROOT}/data/${TODAY}"

# create temporally directory
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT
# download and unzip the data 
curl -L "${ZIP_URL}" -o "${TEMP_DIR}/data.zip"
unzip -q "${TEMP_DIR}/data.zip" -d "${TEMP_DIR}/unzipped"


mkdir -p "${DATA_DIR}"
# copy root csv
find "${TEMP_DIR}/unzipped" -maxdepth 1 -type f -name "*.csv" -exec cp {} "${DATA_DIR}/" \;


cd "${REPO_ROOT}"
git add scripts/fetch-csvs.sh data/${TODAY}
git commit -m "Add CSV files for ${TODAY}"
git push

