if [ -f .env ]; then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

# ================

# Check required environment variables
required_vars=(
  "BLENDER_EXECUTABLE_PATH"
  "BLENDER_ADDONS_PATH"
  "ANACONDA_PATH"
  "CONDA_ENV_NAME"
)
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "Error: Missing required environment variables:"
    printf '%s\n' "${missing_vars[@]}"
    exit 1
fi

echo ================================
echo "Using environment variables:"
echo "BLENDER_ADDONS_PATH: $BLENDER_ADDONS_PATH"
echo "ANACONDA_PATH: $ANACONDA_PATH"
echo "CONDA_ENV_NAME: $CONDA_ENV_NAME"

source "$ANACONDA_PATH"/etc/profile.d/conda.sh

conda activate "$CONDA_ENV_NAME"

rm -rf "$BLENDER_ADDONS_PATH/ufit"
mkdir "$BLENDER_ADDONS_PATH/ufit"
cp -R ufit/. "$BLENDER_ADDONS_PATH/ufit"

killall blender

echo ================================

$BLENDER_EXECUTABLE_PATH --python-use-system-env
