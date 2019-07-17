#!/bin/bash

count='ls -1 *.zip *. 2>/dev/null | wc -l'
if [[ ${count} != 0 ]]; then
    rm *.zip
fi

retrieval_date=$(date +%Y%m%d)
retrieval_day=$(date +%d)
retrieval_month=$(date +%m)
retrieval_year=$(date +%Y)

#These variables are received from AWS_Database_Start.py
hostname=$1
DBPort=$2
MasterUsername=$3
Temp_DBName=$4

attempts=0

url="https://aact.ctti-clinicaltrials.org/static/static_db_copies/daily/${retrieval_date}_clinical_trials.zip"
response=$(curl -sL -w "%{http_code}" -I ${url} -o /dev/null)

echo "Searching for most recent data..."
while true; do
    if [[ ${response} != '200' ]]; then
        attempts=$(($attempts + 1))
        if [[ ${retrieval_day} == "01" ]]; then
            if [[ ${retrieval_month} == "01" ]]; then
                retrieval_year=$(($retrieval_year - 1))
                retrieval_month=13
            fi
            retrieval_day=32
            retrieval_month=$((10#$retrieval_month - 1))
            if !(( 10#${retrieval_month} >= 10 )); then
                retrieval_month="0$retrieval_month"
            fi
        fi
        retrieval_day=$((10#$retrieval_day - 1))
        if !(( 10#${retrieval_day} >= 10 )); then
            retrieval_day="0$retrieval_day"
        fi
        retrieval_date=$(date +${retrieval_year}${retrieval_month}${retrieval_day})
        url="https://aact.ctti-clinicaltrials.org/static/static_db_copies/daily/${retrieval_date}_clinical_trials.zip"
        response=$(curl -sL -w "%{http_code}" -I ${url} -o /dev/null)
        if (( ${attempts} >= 100 )); then
            echo "Could not find suitable retrieval link within the past 100 days."
            break
        fi
        continue
    else
        echo "Most recent data found for ${retrieval_date}."
        results=$(curl ${url} -O)
        break
    fi
done

mkdir zip_extract_contents
unzip -o ${retrieval_date}_clinical_trials.zip -d zip_extract_contents

pg_restore -e -v -O -x -h ${hostname} -p ${DBPort} --username ${MasterUsername} --dbname ${Temp_DBName} --no-owner --clean --if-exists --create zip_extract_contents/postgres_data.dmp


parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd ${parent_path}

python3 ../create_categorical_tables.py
