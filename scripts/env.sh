#!/usr/bin/env bash
#
# env.sh
# Reads from .env.ini and writes out .env with only KEY= (blank value).
#

TEMPLATE_FILE=".env.ini"
TARGET_FILE=".env"

# 1) Make sure the template file exists
if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "Template file '$TEMPLATE_FILE' not found!"
  exit 1
fi

# 2) If .env already exists, warn and exit
if [ -f "$TARGET_FILE" ]; then
  echo "Error: '$TARGET_FILE' already exists. Aborting to avoid overwriting."
  echo "Please remove or rename '$TARGET_FILE' before running this script."
  exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
  # 1. Remove Windows \r if present
  line="$(echo "$line" | tr -d '\r')"

  # 2. Skip empty lines or lines starting with '#'
  if [[ -z "$line" || "$line" =~ ^# ]]; then
    continue
  fi

  # 3. Split on '=', ignoring extra spaces
  #    cut -d'=' takes the part before '=', then xargs strips whitespace
  key="$(echo "$line" | cut -d'=' -f1 | xargs)"

  # 4. Skip if key is empty
  [ -z "$key" ] && continue

  # 5. Write "KEY=" to .env
  echo "${key}=" >> "$TARGET_FILE"

done < "$TEMPLATE_FILE"

echo "Generated '$TARGET_FILE' from '$TEMPLATE_FILE'."
echo "Contents of '$TARGET_FILE':"
echo "---------------------------------"
cat "$TARGET_FILE"
echo "---------------------------------"
